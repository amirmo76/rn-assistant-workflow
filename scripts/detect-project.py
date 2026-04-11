#!/usr/bin/env python3
"""
detect-project.py — Detect project type, package manager, and stack.

Usage:
  python detect-project.py [--project-dir PATH]

Output:
  JSON object printed to stdout.

  Fields:
    platform        : "react-native" | "web" | null
    package_manager : "npm" | "yarn" | "pnpm" | "bun" | null
    stack           : "expo" | "react-native-cli" | "next" | "vite" |
                      "cra" | "remix" | "gatsby" | "astro" | "react" | null
    typescript      : true | false
    confidence      : "high" | "medium" | "low" | "none"
    warnings        : list of human-readable warning strings
    error           : error message string | null

Exit codes:
  0  Detection successful and confident
  1  Detection incomplete or low confidence (partial result still printed)
  2  Fatal error (no package.json, unreadable file, etc.)
"""

import argparse
import json
import sys
from pathlib import Path

# Priority order for lock file → package manager mapping.
_LOCK_FILES: list[tuple[str, str]] = [
    ("bun.lockb", "bun"),
    ("yarn.lock", "yarn"),
    ("pnpm-lock.yaml", "pnpm"),
    ("package-lock.json", "npm"),
]

# Ordered list of (dependency_name, stack_name) pairs for web stack detection.
_WEB_STACKS: list[tuple[str, str]] = [
    ("next", "next"),
    ("vite", "vite"),
    ("react-scripts", "cra"),
    ("@remix-run/react", "remix"),
    ("@remix-run/dev", "remix"),
    ("gatsby", "gatsby"),
    ("astro", "astro"),
    ("@astrojs/react", "astro"),
]


def _all_deps(pkg: dict) -> dict:
    return {
        **pkg.get("dependencies", {}),
        **pkg.get("devDependencies", {}),
    }


def _detect_package_manager(
    project_dir: Path, pkg: dict
) -> tuple[str | None, list[str]]:
    """Return (package_manager, warnings)."""
    warnings: list[str] = []

    # 1. Explicit `packageManager` field in package.json (corepack standard).
    pm_field = pkg.get("packageManager", "")
    if isinstance(pm_field, str) and pm_field:
        for pm_name in ("bun", "pnpm", "yarn", "npm"):
            if pm_field.startswith(pm_name):
                return pm_name, warnings

    # 2. Lock files — collect all present, then pick by priority.
    found: list[str] = [
        pm for fname, pm in _LOCK_FILES if (project_dir / fname).exists()
    ]

    if len(found) == 1:
        return found[0], warnings

    if len(found) > 1:
        warnings.append(
            f"Multiple lock files found ({', '.join(found)}); "
            f"assuming '{found[0]}' by priority order"
        )
        return found[0], warnings

    warnings.append(
        "No lock file or 'packageManager' field found; "
        "package manager could not be detected"
    )
    return None, warnings


def _detect_platform_stack(
    pkg: dict,
) -> tuple[str | None, str | None, str]:
    """Return (platform, stack, confidence)."""
    deps = _all_deps(pkg)

    has_expo = "expo" in deps
    has_rn = "react-native" in deps
    has_react = "react" in deps

    # React Native / Expo takes priority over anything else.
    if has_expo or has_rn:
        stack = "expo" if has_expo else "react-native-cli"
        return "react-native", stack, "high"

    # Web framework sniffing.
    for dep, stack_name in _WEB_STACKS:
        if dep in deps:
            confidence = "high" if has_react else "medium"
            return "web", stack_name, confidence

    # Plain React without a recognised framework.
    if has_react:
        return "web", "react", "medium"

    return None, None, "low"


def _detect_typescript(project_dir: Path, pkg: dict) -> bool:
    deps = _all_deps(pkg)
    return (
        "typescript" in deps
        or (project_dir / "tsconfig.json").exists()
        or (project_dir / "tsconfig.base.json").exists()
    )


def detect(project_dir: Path) -> tuple[dict, int]:
    """Run detection and return (result_dict, exit_code)."""
    pkg_path = project_dir / "package.json"

    if not pkg_path.exists():
        return (
            {
                "platform": None,
                "package_manager": None,
                "stack": None,
                "typescript": None,
                "confidence": "none",
                "warnings": [],
                "error": f"No package.json found in {project_dir}",
            },
            2,
        )

    try:
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return (
            {
                "platform": None,
                "package_manager": None,
                "stack": None,
                "typescript": None,
                "confidence": "none",
                "warnings": [],
                "error": f"package.json is not valid JSON: {exc}",
            },
            2,
        )
    except OSError as exc:
        return (
            {
                "platform": None,
                "package_manager": None,
                "stack": None,
                "typescript": None,
                "confidence": "none",
                "warnings": [],
                "error": f"Could not read package.json: {exc}",
            },
            2,
        )

    warnings: list[str] = []

    pm, pm_warnings = _detect_package_manager(project_dir, pkg)
    warnings.extend(pm_warnings)

    platform, stack, confidence = _detect_platform_stack(pkg)

    if platform is None:
        warnings.append(
            "Could not detect platform; no recognised framework dependency found"
        )

    typescript = _detect_typescript(project_dir, pkg)

    exit_code = 0
    if platform is None or confidence in ("low", "medium", "none"):
        exit_code = 1

    return (
        {
            "platform": platform,
            "package_manager": pm,
            "stack": stack,
            "typescript": typescript,
            "confidence": confidence,
            "warnings": warnings,
            "error": None,
        },
        exit_code,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect project type, package manager, and stack."
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Path to the project root (default: current directory)",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    result, exit_code = detect(project_dir)
    print(json.dumps(result, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
