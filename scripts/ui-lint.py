#!/usr/bin/env python3
"""
ui-lint.py — Structural linter for component tree YAML files.

Usage:
    python ui-lint.py --file tree.yaml

Checks performed:
  1. YAML parse validity — the file must be valid YAML.
  2. Collapsed scalar detection — a string or key containing " - " where both
     sides are component-like names is the symptom of a missing ":" on a
     component entry that has children.  YAML folds the child lines into a
     single plain scalar when the parent key has no colon.
  3. Single root per document — every document (after the optional _Context_
     front-matter block) must have exactly one top-level key.
  4. Valid value types — every value in the tree must be a list, dict, or null
     (leaf component).  Bare scalars other than string annotations are an error.

Exit codes:
    0  No errors found.
    1  One or more structural errors found.
    2  File not found or unreadable.
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

# A "collapsed scalar" matches two or more PascalCase tokens separated by " - ".
# Each token must start with an uppercase letter so that plain lowercase strings
# (e.g. context descriptions) are not flagged.  This is the symptom produced
# when a component with children is written without a trailing colon: YAML folds
# the child list items into one plain scalar by joining them with " - ".
_COLLAPSED_RE = re.compile(
    r"^[A-Z][A-Za-z0-9]*(?:\s-\s[A-Z][A-Za-z0-9]*)+$"
)

# @context annotation prefix
_CONTEXT_ANNO_RE = re.compile(r"^@context:", re.IGNORECASE)


def _is_context_anno(s: str) -> bool:
    return bool(_CONTEXT_ANNO_RE.match(s.strip()))


def _looks_collapsed(s: str) -> bool:
    """Return True when *s* looks like multiple component names joined by ' - '."""
    return bool(_COLLAPSED_RE.match(s.strip()))


# ---------------------------------------------------------------------------
# Error type
# ---------------------------------------------------------------------------


class LintError:
    """A single lint finding."""

    def __init__(self, doc_root: str, path: str, message: str) -> None:
        self.doc_root = doc_root
        self.path = path
        self.message = message

    def __str__(self) -> str:
        location = f"[doc:{self.doc_root}]"
        if self.path:
            location += f" {self.path}"
        return f"ERROR {location}: {self.message}"

    def __repr__(self) -> str:  # pragma: no cover
        return f"LintError(doc_root={self.doc_root!r}, path={self.path!r}, message={self.message!r})"


# ---------------------------------------------------------------------------
# Recursive node linter
# ---------------------------------------------------------------------------


def _lint_node(node: object, doc_root: str, path: str, errors: list) -> None:
    """Recursively lint a parsed YAML node, appending LintError objects to *errors*."""
    if isinstance(node, str):
        s = node.strip()
        if not _is_context_anno(s) and _looks_collapsed(s):
            errors.append(LintError(
                doc_root,
                path,
                f'string looks like multiple components merged (missing ":"?): "{s}"',
            ))

    elif isinstance(node, list):
        for i, item in enumerate(node):
            _lint_node(item, doc_root, f"{path}[{i}]" if path else f"[{i}]", errors)

    elif isinstance(node, dict):
        for key, value in node.items():
            s_key = str(key)
            child_path = f"{path} > {s_key}" if path else s_key
            if not _is_context_anno(s_key) and _looks_collapsed(s_key):
                errors.append(LintError(
                    doc_root,
                    path,
                    f'key looks like multiple components merged (missing ":"?): "{s_key}"',
                ))
            if value is not None and not isinstance(value, (list, dict)):
                errors.append(LintError(
                    doc_root,
                    child_path,
                    f"unexpected value type {type(value).__name__!r}: {value!r}",
                ))
            elif value is not None:
                _lint_node(value, doc_root, child_path, errors)

    elif node is not None:
        # Unexpected scalar at list level (int, bool, float, etc.)
        errors.append(LintError(
            doc_root,
            path,
            f"unexpected value type {type(node).__name__!r}: {node!r}",
        ))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def lint(path: Path) -> list:
    """Lint the YAML file at *path*.  Returns a (possibly empty) list of LintError."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [LintError("<file>", "", f"cannot read file: {exc}")]

    # 1. YAML parse validity
    try:
        docs = list(yaml.safe_load_all(content))
    except yaml.YAMLError as exc:
        return [LintError("<yaml>", "", f"YAML parse error: {exc}")]

    docs = [d for d in docs if isinstance(d, dict)]

    errors: list = []

    for doc in docs:
        # _Context_ front-matter block — skip structural checks
        if "_Context_" in doc:
            continue

        # 2. Single root per document
        if len(doc) != 1:
            keys = list(doc.keys())
            errors.append(LintError(
                str(keys[0]) if keys else "<empty>",
                "",
                f"document has {len(doc)} top-level key(s) (expected exactly 1): {keys}",
            ))
            continue

        root_key = next(iter(doc))
        root_value = doc[root_key]
        doc_root = str(root_key)

        # Collapsed root key
        if _looks_collapsed(doc_root):
            errors.append(LintError(
                doc_root,
                "",
                f'root key looks like multiple components merged (missing ":"?): "{doc_root}"',
            ))

        # 3. Recursively lint the subtree
        if root_value is not None:
            _lint_node(root_value, doc_root, "", errors)

    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint a component tree YAML file for structural errors.",
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        metavar="YAML",
        help="Path to the component tree YAML file.",
    )
    args = parser.parse_args()
    path = Path(args.file)

    if not path.exists():
        print(f"ERROR: File not found: '{path}'", file=sys.stderr)
        sys.exit(2)

    errors = lint(path)

    if not errors:
        print(f"OK: No errors found in '{path}'.")
        sys.exit(0)
    else:
        for err in errors:
            print(err)
        print(f"\n{len(errors)} error(s) found in '{path}'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
