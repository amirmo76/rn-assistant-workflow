#!/usr/bin/env python3
"""
ui-architect.py — Component tree YAML parser for architectural queries.

Usage:
    python ui-architect.py --file tree.yaml --list-components
    python ui-architect.py --file tree.yaml --deps LoginCard
    python ui-architect.py --file tree.yaml --context Button

Three modes:
  --list-components       Print every unique component name found in the file.
  --deps COMPONENT        Print the direct dependencies of COMPONENT (all unique
                          components that are imported and used by it, as declared
                          in its composition block).
  --context COMPONENT     Print all context for COMPONENT: global description from
                          the optional _Context_ front-matter block, and every
                          instance-level @context annotation with its path trace.

YAML format rules:
  • The optional first document may be a global front-matter block whose single
    top-level key is `_Context_`. Its value is a mapping of component name to a
    plain-text description of the component's role.
  • Each subsequent YAML document (separated by ---) contains exactly one
    top-level key, which is the root component of that block.
  • Every component listed anywhere in that block (at any nesting depth) is a
    direct dependency of the root component, not of intermediate nodes.
  • A `@context: ...` string inside a component's children list is an
    instance-level annotation for that component and is NOT a component name.
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

# Matches @context annotations, e.g. "@context: variant=primary, size=lg"
_CONTEXT_ANNO_RE = re.compile(r"^@context:\s*(.*)", re.IGNORECASE)


def _strip_parens(name: str) -> str:
    """Remove trailing parenthetical annotation and whitespace from a name."""
    return _PAREN_RE.sub("", name).strip()


def _is_context_anno(s: str) -> bool:
    """Return True if the string is a @context annotation."""
    return bool(_CONTEXT_ANNO_RE.match(s.strip()))


def _extract_context_value(s: str) -> str:
    """Extract the value part from a @context annotation string."""
    m = _CONTEXT_ANNO_RE.match(s.strip())
    return m.group(1).strip() if m else ""


def _get_instance_context(children: object) -> "str | None":
    """Return the @context annotation value from a children list, or None."""
    if not isinstance(children, list):
        return None
    for item in children:
        if isinstance(item, str) and _is_context_anno(item):
            return _extract_context_value(item)
    return None


def _collect(node: object, result: set) -> None:
    """Recursively collect all component names from a parsed YAML node.

    Skips @context annotation strings so they are never treated as names.
    """
    if isinstance(node, str):
        if _is_context_anno(node):
            return
        name = _strip_parens(node)
        if name:
            result.add(name)
    elif isinstance(node, list):
        for item in node:
            _collect(item, result)
    elif isinstance(node, dict):
        for key, value in node.items():
            s_key = str(key)
            if _is_context_anno(s_key):
                continue
            name = _strip_parens(s_key)
            if name:
                result.add(name)
            if value is not None:
                _collect(value, result)


def _collect_instances(
    node: object,
    target: str,
    path: list,
    instances: list,
) -> None:
    """Recursively find all instances of `target` with their path and context.

    Each entry appended to `instances` is a dict:
        {"path": [str, ...], "context": str | None}

    `path` is the list of ancestor component names leading to (but not yet
    including) the current node.
    """
    if isinstance(node, str):
        if _is_context_anno(node):
            return
        name = _strip_parens(node)
        if name == target:
            instances.append({"path": path + [name], "context": None})
    elif isinstance(node, list):
        for item in node:
            _collect_instances(item, target, path, instances)
    elif isinstance(node, dict):
        for key, value in node.items():
            s_key = str(key)
            if _is_context_anno(s_key):
                continue
            name = _strip_parens(s_key)
            if not name:
                continue
            ctx = _get_instance_context(value)
            if name == target:
                instances.append({"path": path + [name], "context": ctx})
            if value is not None:
                _collect_instances(value, target, path + [name], instances)


def _load_docs(path: Path) -> "tuple[dict, list]":
    """Load all YAML documents, separating the optional _Context_ front matter.

    Returns:
        (global_context, component_docs)
        global_context  — dict of component_name -> description (empty when absent)
        component_docs  — list of component tree dicts
    """
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

    docs = [d for d in docs if isinstance(d, dict)]

    global_context: dict = {}
    component_docs: list = []

    for doc in docs:
        if "_Context_" in doc:
            ctx_value = doc["_Context_"]
            if isinstance(ctx_value, dict):
                global_context = {str(k): str(v) for k, v in ctx_value.items()}
        else:
            component_docs.append(doc)

    return global_context, component_docs


def list_components(path: Path) -> list:
    """Return a sorted list of every unique component name in the file."""
    _, docs = _load_docs(path)
    result: set = set()
    for doc in docs:
        for root_key, value in doc.items():
            root_name = _strip_parens(str(root_key))
            if root_name:
                result.add(root_name)
            if value is not None:
                _collect(value, result)
    return sorted(result)


def list_deps(path: Path, component: str) -> list:
    """Return a sorted list of direct dependencies of the given component.

    A component's dependencies are all unique components found anywhere
    inside its composition block (the entire subtree under its top-level key).
    Returns an empty list when the component has no block defined.
    """
    _, docs = _load_docs(path)
    for doc in docs:
        for root_key, value in doc.items():
            if _strip_parens(str(root_key)) == component:
                if value is None:
                    return []
                deps: set = set()
                _collect(value, deps)
                return sorted(deps)
    return []


def get_context(path: Path, component: str) -> dict:
    """Return all context information for a component.

    Returns a dict:
        {
            "global": str | None,        # description from _Context_ block
            "instances": [               # instances found in other components' trees
                {"path": [...], "context": str | None},
                ...
            ]
        }

    Only instances found inside OTHER components' composition blocks are included.
    The component's own definition block is not an "instance".
    """
    global_ctx, docs = _load_docs(path)

    global_entry = global_ctx.get(component)
    instances: list = []

    for doc in docs:
        for root_key, value in doc.items():
            root_name = _strip_parens(str(root_key))
            # Only search inside OTHER components' trees
            if root_name != component and value is not None:
                _collect_instances(value, component, [root_name], instances)

    return {"global": global_entry, "instances": instances}


def print_context(path: Path, component: str) -> None:
    """Print formatted context for a component to stdout."""
    result = get_context(path, component)

    global_entry = result["global"]
    annotated_instances = [i for i in result["instances"] if i["context"] is not None]

    if global_entry is None and not annotated_instances:
        print(f"No context found for '{component}'.")
        return

    if global_entry is not None:
        print("=== Global Context ===")
        print(f"{component}: {global_entry}")

    if annotated_instances:
        if global_entry is not None:
            print()
        print("=== Instance Contexts ===")
        for inst in annotated_instances:
            path_str = " > ".join(inst["path"])
            print(path_str)
            print(f"  @context: {inst['context']}")


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
    group.add_argument(
        "--context", "-c",
        metavar="COMPONENT",
        help=(
            "Print all context for a component: global description from the "
            "_Context_ front-matter block and every @context instance annotation "
            "with its full path trace."
        ),
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
    elif args.deps:
        deps = list_deps(path, args.deps)
        for name in deps:
            print(name)
    else:
        print_context(path, args.context)


if __name__ == "__main__":
    main()
