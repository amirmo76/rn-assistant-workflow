#!/usr/bin/env python3
"""Install this workflow into the user's ~/.copilot directory."""

import json
import os
import platform
import re
import shutil
import sys
import tempfile
from pathlib import Path

FOLDER_MAP = {
    "agents": "agents",
    "references": "references",
    "workflows": "workflows",
    "skills": "skills",
    "scripts": "scripts",
}

MANAGED_ENTRIES = {
    "agents": {
        "rn-assistant.agent.md",
        "rn-architect.agent.md",
        "rn-explore.agent.md",
        "rn-initializer.agent.md",
        "rn-planner.agent.md",
        "rn-spec-writer.agent.md",
        "rn-tasker.agent.md",
        "rn-worker.agent.md",
        "rn-researcher.agent.md",
        "rn-reviewer.agent.md",
        "rn-review.agent.md",
    },
    "references": {
        "component-spec.md",
        "objective-spec.md",
        "plan.md",
        "task-list.md",
        "agent-report.md",
        "rn-changelog.md"
    },
    "workflows": {"ui-assistant.workflow.md"},
    "scripts": {"rn-architect.py", "detect-project.py", "tests"},
    "skills": {
        "rn-tree-decomposition",
        "rn-testing-setup",
        "rn-storybook-setup",
        "rn-tree-decomposition.skill.md",
        "rn-testing-setup.skill.md",
        "rn-storybook-setup.skill.md",
    },
}

AVAILABLE_MODELS = {
    "1": "GPT-5.4",
    "2": "Claude Sonnet 4.6",
    "3": "GPT-5 mini",
    "4": "Claude Haiku 4.5",
    "5": "Raptor mini",
}

MODEL_PRESETS = {
    "1": ("Premium orchestrator", "GPT-5.4"),
    "2": ("Claude orchestrator", "Claude Sonnet 4.6"),
    "3": ("Budget", "GPT-5 mini"),
    "4": ("Default", None),
    "5": ("Custom", None),
}

MODEL_LINE_RE = re.compile(r"^(model:\s*)(.+)$", re.MULTILINE)
ORCHESTRATOR_AGENT = "rn-assistant"


def get_source_dir() -> Path:
    return Path(__file__).resolve().parent


def detect_os() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return "linux"


def get_dest_root() -> Path:
    override = os.environ.get("COPILOT_HOME")
    if override:
        return Path(override)

    current_os = detect_os()
    if current_os == "windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / ".copilot"
        return Path.home() / "AppData" / "Roaming" / ".copilot"

    return Path.home() / ".copilot"


def get_vscode_settings_path() -> Path:
    current_os = detect_os()
    if current_os == "windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Code" / "User" / "settings.json"
        return Path.home() / "AppData" / "Roaming" / "Code" / "User" / "settings.json"
    if current_os == "macos":
        return Path.home() / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    return Path.home() / ".config" / "Code" / "User" / "settings.json"


def patch_vscode_settings(dest_root: Path, dry_run: bool = False) -> None:
    settings_path = get_vscode_settings_path()
    agents_path = str(dest_root / "agents")

    required = {
        "chat.agent.enabled": True,
    }
    location_settings = {
        "chat.agent.locations": {agents_path: True},
    }

    if not settings_path.exists():
        print(f"VS Code settings not found at {settings_path}")
        if dry_run:
            print("  Would create settings.json with the agent path")
            return
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings = {}
    else:
        try:
            raw = settings_path.read_text(encoding="utf-8")
            settings = json.loads(raw) if raw.strip() else {}
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  WARN  Could not parse {settings_path}: {exc}")
            print("  Skipping VS Code settings patch.")
            return

    changed = False

    for key, value in required.items():
        if settings.get(key) != value:
            print(f"  SET    {key} = {value}")
            settings[key] = value
            changed = True

    for key, entries in location_settings.items():
        existing = settings.get(key, {})
        if not isinstance(existing, dict):
            existing = {}
        for path, enabled in entries.items():
            if existing.get(path) != enabled:
                print(f"  ADD    {key} += {path}")
                existing[path] = enabled
                changed = True
        settings[key] = existing

    if not changed:
        print("  VS Code settings already configured.")
        return

    if dry_run:
        print(f"  Would write updated settings to {settings_path}")
        return

    settings_path.write_text(
        json.dumps(settings, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  Updated {settings_path}")


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def copy_entry(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copy2(source, target)


def discover_agents(src_root: Path) -> dict[str, tuple[Path, str]]:
    agents_dir = src_root / "agents"
    if not agents_dir.is_dir():
        return {}

    result: dict[str, tuple[Path, str]] = {}
    for file in sorted(agents_dir.iterdir()):
        if not file.is_file() or not file.name.endswith(".agent.md"):
            continue
        content = file.read_text(encoding="utf-8")
        match = MODEL_LINE_RE.search(content)
        if match:
            agent_name = file.stem.replace(".agent", "")
            result[agent_name] = (file, match.group(2).strip())
    return result


def prompt_model_selection(agents: dict[str, tuple[Path, str]]) -> dict[str, str]:
    print("=" * 60)
    print("  MODEL CONFIGURATION")
    print("=" * 60)
    print()
    print("Current agent models:")
    for name, (_path, model) in agents.items():
        role = "orchestrator" if name == ORCHESTRATOR_AGENT else "worker"
        print(f"  {name:<30} {model:<20} ({role})")
    print()

    print("Choose a configuration:")
    for key, (label, _model) in MODEL_PRESETS.items():
        print(f"  [{key}] {label}")
    print()

    choice = input("Select preset [4]: ").strip() or "4"
    if choice not in MODEL_PRESETS:
        print(f"Invalid choice '{choice}', using default.")
        choice = "4"

    _label, preset_model = MODEL_PRESETS[choice]
    overrides: dict[str, str] = {}

    if choice == "4":
        print("\nKeeping current model defaults.\n")
        return overrides

    if choice == "5":
        print("\nChoose a model for each agent:")
        print("  [1] GPT-5.4  [2] Claude Sonnet 4.6  [3] GPT-5 mini  [4] Claude Haiku 4.5  [5] Raptor mini  [Enter] keep\n")
        for name, (_path, current) in agents.items():
            pick = input(f"  {name:<30} [{current}]: ").strip()
            if pick in AVAILABLE_MODELS:
                chosen = AVAILABLE_MODELS[pick]
                if chosen != current:
                    overrides[name] = chosen
            elif pick and pick not in AVAILABLE_MODELS:
                print(f"    Invalid input '{pick}', keeping {current}")
        return overrides

    for name, (_path, current) in agents.items():
        if name == ORCHESTRATOR_AGENT:
            if current != preset_model:
                overrides[name] = preset_model
        elif choice == "3" and current != "GPT-5 mini":
            overrides[name] = "GPT-5 mini"

    if overrides:
        print("\nModel changes to apply:")
        for name, model in overrides.items():
            print(f"  {name:<30} {agents[name][1]}  ->  {model}")
        print()
    else:
        print("\nNo model changes needed.\n")

    return overrides


def apply_model_overrides(
    src_root: Path,
    agents: dict[str, tuple[Path, str]],
    overrides: dict[str, str],
) -> Path | None:
    if not overrides:
        return None

    tmp_dir = Path(tempfile.mkdtemp(prefix="sdd-install-"))
    for folder in FOLDER_MAP:
        src_folder = src_root / folder
        if src_folder.is_dir():
            shutil.copytree(src_folder, tmp_dir / folder)

    for agent_name, new_model in overrides.items():
        if agent_name not in agents:
            continue
        original_path = agents[agent_name][0]
        tmp_path = tmp_dir / "agents" / original_path.name
        if not tmp_path.exists():
            continue
        content = tmp_path.read_text(encoding="utf-8")
        content = MODEL_LINE_RE.sub(rf"\g<1>{new_model}", content, count=1)
        tmp_path.write_text(content, encoding="utf-8")
        print(f"  PATCH  {original_path.name}  model -> {new_model}")

    return tmp_dir


def install(dry_run: bool = False) -> None:
    src_root = get_source_dir()
    dest_root = get_dest_root()

    print(f"OS detected : {detect_os()} ({platform.system()} {platform.release()})")
    print(f"Source      : {src_root}")
    print(f"Destination : {dest_root}")
    print()

    agents = discover_agents(src_root)
    overrides: dict[str, str] = {}
    tmp_dir: Path | None = None

    if agents:
        overrides = prompt_model_selection(agents)
        if overrides and not dry_run:
            tmp_dir = apply_model_overrides(src_root, agents, overrides)

    effective_src = tmp_dir if tmp_dir else src_root

    if not dest_root.exists():
        print(f"Creating {dest_root}")
        if not dry_run:
            dest_root.mkdir(parents=True, exist_ok=True)

    copied = 0

    for src_folder, dest_folder in FOLDER_MAP.items():
        src_path = effective_src / src_folder
        dest_path = dest_root / dest_folder

        if not src_path.is_dir():
            print(f"  SKIP    {src_folder}/ (not found in source)")
            continue

        if not dest_path.exists():
            print(f"  CREATE  {dest_path}")
            if not dry_run:
                dest_path.mkdir(parents=True, exist_ok=True)

        source_entries = {entry.name for entry in src_path.iterdir()}
        managed_entries = MANAGED_ENTRIES.get(src_folder, set())

        for stale_name in sorted(managed_entries - source_entries):
            stale_path = dest_path / stale_name
            if stale_path.exists():
                print(f"  REMOVE  {stale_name}  ->  {dest_path.relative_to(dest_root)}/")
                if not dry_run:
                    remove_path(stale_path)

        for entry in sorted(src_path.iterdir()):
            target = dest_path / entry.name
            action = "SYNC" if target.exists() else "COPY"
            print(f"  {action:<6} {entry.name}  ->  {dest_path.relative_to(dest_root)}/")
            if not dry_run:
                if target.exists():
                    remove_path(target)
                copy_entry(entry, target)
            copied += 1

    if tmp_dir and tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    print()
    if dry_run:
        print(f"Dry run complete - {copied} entries would be installed to {dest_root}")
    else:
        print(f"Done - {copied} entries installed to {dest_root}")

    print("\nConfiguring VS Code settings ...")
    patch_vscode_settings(dest_root, dry_run=dry_run)


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    if dry:
        print("=== DRY RUN (no files will be written) ===\n")
    install(dry_run=dry)