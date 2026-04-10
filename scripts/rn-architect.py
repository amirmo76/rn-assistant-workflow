#!/usr/bin/env python3
"""
rn-architect.py — Component tree YAML parser for architectural queries.

Usage:
  python rn-architect.py --file tree.yaml --list-components
  python rn-architect.py --file tree.yaml --deps LoginCard

Two modes:
  --list-components   Print every unique component name found anywhere in the file.
  --deps COMPONENT    Print the direct dependencies of COMPONENT (all unique
                      components that are imported and used by it, as declared
                      in its composition block).

YAML format rules:
  • Each YAML document (separated by ---) contains exactly one top-level key,
    which is the root component of that block.
  • Every component listed anywhere in that block (at any nesting depth) is a
    direct dependency of the root component, not of intermediate nodes.
  • Parentheses after a component name are contextual annotations and do not
    change the component identity.
  • If a component appears multiple times it is still one dependency.
  • Components that appear only as children of another block (never as a
    top-level key) have no defined dependencies.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Matches trailing parenthetical context, e.g. ' (variant="primary", size="lg")'
_PAREN_RE = re.compile(r"\s*\([^)]*\)\s*$")


def _strip_parens(name: str) -> str:
    """Remove trailing parenthetical annotation and whitespace from a name."""
    return _PAREN_RE.sub("", name).strip()


def _collect(node: object, result: set[str]) -> None:
    """Recursively collect all component names from a parsed YAML node."""
    if isinstance(node, str):
        name = _strip_parens(node)
        if name:
            result.add(name)
    elif isinstance(node, list):
        for item in node:
            _collect(item, result)
    elif isinstance(node, dict):
        for key, value in node.items():
            name = _strip_parens(str(key))
            if name:
                result.add(name)
            if value is not None:
                _collect(value, result)


def _load_docs(path: Path) -> list[dict]:
    """Load and return all YAML documents from a file."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Cannot read file '{path}': {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        docs = list(yaml.safe_load_all(content))
    except yaml.YAMLError as exc:
        print(f"ERROR: Invalid YAML in '{path}': {exc}", file=sys.stderr)
        sys.exit(1)

    return [d for d in docs if isinstance(d, dict)]


def list_components(path: Path) -> list[str]:
    """Return a sorted list of every unique component name in the file."""
    docs = _load_docs(path)
    result: set[str] = set()
    for doc in docs:
        for root_key, value in doc.items():
            root_name = _strip_parens(str(root_key))
            if root_name:
                result.add(root_name)
            if value is not None:
                _collect(value, result)
    return sorted(result)


def list_deps(path: Path, component: str) -> list[str]:
    """Return a sorted list of direct dependencies of the given component.

    A component's dependencies are all unique components found anywhere
    inside its composition block (the entire subtree under its top-level key).
    Returns an empty list when the component has no block defined.
    """
    docs = _load_docs(path)
    for doc in docs:
        for root_key, value in doc.items():
            if _strip_parens(str(root_key)) == component:
                if value is None:
                    return []
                deps: set[str] = set()
                _collect(value, deps)
                return sorted(deps)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a component tree YAML and answer architectural questions.",
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        metavar="YAML",
        help="Path to the component tree YAML file.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list-components", "-l",
        action="store_true",
        help="List every unique component in the file.",
    )
    group.add_argument(
        "--deps", "-d",
        metavar="COMPONENT",
        help="List all direct dependencies of the given component.",
    )

    args = parser.parse_args()
    path = Path(args.file)

    if not path.exists():
        print(f"ERROR: File not found: '{path}'", file=sys.stderr)
        sys.exit(1)

    if args.list_components:
        components = list_components(path)
        for name in components:
            print(name)
    else:
        deps = list_deps(path, args.deps)
        for name in deps:
            print(name)


if __name__ == "__main__":
    main()
