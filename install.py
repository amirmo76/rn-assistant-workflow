#!/usr/bin/env python3
"""Install UI agents files into the user's ~/.copilot folder.

Supports Windows, macOS, and Linux — auto-detects the correct path.
Also patches VS Code settings.json so Copilot discovers the installed
agents and prompts automatically.
"""

import json
import os
import platform
import re
import shutil
import sys
import tempfile
from pathlib import Path

# Folders to copy and their destination subdirectories inside .copilot
FOLDER_MAP = {
    "agents": "agents",
    "references": "references",
    "workflows": "workflows",
    "prompts": "prompts",
    "skills": "skills",
}

# Legacy and current SDD-managed files that may need pruning when they no longer
# exist in the source repository. This avoids leaving outdated agents and
# references installed across upgrades while preserving unrelated user files.
MANAGED_FILES = {
    "agents": {
        "explore.agent.md",
        "ui-architect.agent.md",
        "ui-researcher.agent.md",
        "ui-spec-writer.agent.md",
        "ui-assistant.agent.md",
    },
    "references": set(),
    "workflows": {"ui-assistant.workflow.md"},
    "prompts": set(),
    "skills": {"rn-tree-decomposition.skill.md"},
}

# Available models for agent configuration
AVAILABLE_MODELS = {
    "1": "GPT-5.4",
    "2": "Claude Sonnet 4.6",
    "3": "GPT-5 mini",
    "4": "Claude Haiku 4.5",
    "5": "Raptor mini",
}

MODEL_PRESETS = {
    "1": ("Premium orchestrator (GPT-5.4 orchestrator, GPT-5 mini workers)", "GPT-5.4"),
    "2": ("Claude orchestrator (Claude Sonnet 4.6 orchestrator, GPT-5 mini workers)", "Claude Sonnet 4.6"),
    "3": ("Budget (all GPT-5 mini — not recommended for orchestrator)", "GPT-5 mini"),
    "4": ("Default (keep current per-agent defaults)", None),
    "5": ("Custom (choose per agent)", None),
}

# Pattern to match the model line in agent YAML frontmatter
MODEL_LINE_RE = re.compile(r"^(model:\s*)(.+)$", re.MULTILINE)

# The orchestrator agent file
ORCHESTRATOR_AGENT = "sdd"


def get_source_dir() -> Path:
    """Return the directory where this script lives."""
    return Path(__file__).resolve().parent


def detect_os() -> str:
    """Return normalised OS name: 'windows', 'macos', or 'linux'."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return "linux"


def get_dest_root() -> Path:
    """Return the .copilot directory for the current OS."""
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
    """Return the VS Code user settings.json path for the current OS."""
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
    """Add agent and prompt paths to VS Code settings.json if not already present."""
    settings_path = get_vscode_settings_path()

    agents_path = str(dest_root / "agents")
    prompts_path = str(dest_root / "prompts")

    required = {
        "chat.agent.enabled": True,
        "chat.promptFiles": True,
    }
    location_settings = {
        "chat.agent.locations": {agents_path: True},
        "chat.promptFiles.locations": {prompts_path: True},
    }

    if not settings_path.exists():
        print(f"VS Code settings not found at {settings_path}")
        if dry_run:
            print("  Would create settings.json with agent/prompt paths")
            return
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings = {}
    else:
        try:
            raw = settings_path.read_text(encoding="utf-8")
            settings = json.loads(raw) if raw.strip() else {}
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  WARN  Could not parse {settings_path}: {exc}")
            print("  Skipping VS Code settings patch — fix the file manually.")
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
            if path not in existing:
                print(f"  ADD    {key} += {path}")
                existing[path] = enabled
                changed = True
        settings[key] = existing

    if not changed:
        print("  VS Code settings already configured — no changes needed.")
        return

    if dry_run:
        print("  Would write updated settings to", settings_path)
        return

    settings_path.write_text(
        json.dumps(settings, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  Updated {settings_path}")


def discover_agents(src_root: Path) -> dict[str, tuple[Path, str]]:
    """Scan agent files and return {agent_name: (path, current_model)}."""
    agents_dir = src_root / "agents"
    if not agents_dir.is_dir():
        return {}
    result = {}
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
    """Interactively ask the user which model to use for each agent."""
    print("=" * 60)
    print("  SDD MODEL CONFIGURATION")
    print("=" * 60)
    print()
    print("  Architecture:")
    print("    Orchestrator (smart model) → handles all reasoning")
    print("    Workers (GPT-5 mini)       → execute focused tasks")
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
            role = " (orchestrator)" if name == ORCHESTRATOR_AGENT else ""
            pick = input(f"  {name}{role:<20} [{current}]: ").strip()
            if pick in AVAILABLE_MODELS:
                chosen = AVAILABLE_MODELS[pick]
                if chosen != current:
                    overrides[name] = chosen
            elif pick == "":
                pass
            else:
                print(f"    Invalid input '{pick}', keeping {current}")
    else:
        # Presets 1-3: set orchestrator to preset_model, keep workers as GPT-5 mini
        for name, (_path, current) in agents.items():
            if name == ORCHESTRATOR_AGENT:
                if current != preset_model:
                    overrides[name] = preset_model
            else:
                # Workers stay GPT-5 mini (or force them if not already)
                if current != "GPT-5 mini" and choice != "3":
                    pass  # Keep worker defaults (already GPT-5 mini)

    if overrides:
        print("\nModel changes to apply:")
        for name, model in overrides.items():
            original = agents[name][1]
            print(f"  {name:<30} {original}  →  {model}")
    else:
        print("\nNo model changes needed.")
    print()

    return overrides


def apply_model_overrides(
    src_root: Path,
    agents: dict[str, tuple[Path, str]],
    overrides: dict[str, str],
) -> Path | None:
    """Create a temp copy with model overrides applied."""
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
        print(f"  PATCH  {original_path.name}  model → {new_model}")

    return tmp_dir


def install(dry_run: bool = False) -> None:
    current_os = detect_os()
    src_root = get_source_dir()
    dest_root = get_dest_root()

    print(f"OS detected : {current_os} ({platform.system()} {platform.release()})")
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
            print(f"  SKIP  {src_folder}/ (not found in source)")
            continue

        if not dest_path.exists():
            print(f"  CREATE {dest_path}")
            if not dry_run:
                dest_path.mkdir(parents=True, exist_ok=True)

        source_files = {
            file.name for file in sorted(src_path.iterdir()) if file.is_file()
        }
        managed_names = MANAGED_FILES.get(src_folder, set())

        for stale_name in sorted(managed_names - source_files):
            stale_path = dest_path / stale_name
            if stale_path.exists():
                print(f"  REMOVE     {stale_name}  ->  {dest_path.relative_to(dest_root)}/")
                if not dry_run:
                    stale_path.unlink()

        for file in sorted(src_path.iterdir()):
            if not file.is_file():
                continue
            target = dest_path / file.name
            action = "OVERWRITE" if target.exists() else "COPY"
            print(f"  {action:>9}  {file.name}  ->  {dest_path.relative_to(dest_root)}/")
            if not dry_run:
                shutil.copy2(file, target)
            copied += 1

    if tmp_dir and tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    print()
    if dry_run:
        print(f"Dry run complete — {copied} file(s) would be copied to {dest_root}")
    else:
        print(f"Done — {copied} file(s) installed to {dest_root}")

    print("\nConfiguring VS Code settings …")
    patch_vscode_settings(dest_root, dry_run=dry_run)


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    if dry:
        print("=== DRY RUN (no files will be written) ===\n")
    install(dry_run=dry)

