#!/usr/bin/env python3
"""Tests for ui-architect.py — covers the new _Context_ front-matter and @context
instance annotation syntax, as well as the original list_components / list_deps
behaviour."""

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

_SCRIPT = Path(__file__).resolve().parent.parent / "ui-architect.py"
_spec = importlib.util.spec_from_file_location("ui_architect", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

list_components = _mod.list_components
list_deps = _mod.list_deps
get_context = _mod.get_context
_is_context_anno = _mod._is_context_anno
_extract_context_value = _mod._extract_context_value
_get_instance_context = _mod._get_instance_context

# ---------------------------------------------------------------------------
# Shared YAML fixtures (written to tmp_path in each fixture)
# ---------------------------------------------------------------------------

# No front matter, no @context annotations — baseline
TREE_PLAIN = """\
LoginCard:
  - Card:
      - CardHeader:
          - CardTitle
          - CardSubtitle
      - CardFooter:
          - Button
---
Button:
  - Icon
"""

# No front matter, but has @context instance annotations
TREE_WITH_INSTANCE_CONTEXT = """\
LoginCard:
  - Card:
      - CardHeader:
          - CardTitle
          - CardSubtitle
      - CardFooter:
          - Button:
              - "@context: variant=primary, size=lg"
---
Button:
  - Icon
"""

# Has both _Context_ front matter AND @context instance annotations
TREE_FULL = """\
_Context_:
    Card: "A shell container"
    Button: "A pressable element"
---
LoginCard:
  - Card:
      - CardFooter:
          - Button:
              - "@context: variant=primary, size=lg"
---
Button:
  - Icon
"""

# _Context_ front matter only — no @context annotations in any tree
TREE_GLOBAL_CONTEXT_ONLY = """\
_Context_:
    Card: "A shell container"
    Button: "A pressable element"
---
LoginCard:
  - Card:
      - Button
---
Button:
  - Icon
"""

# Two instances of the same component in one tree, each with a different @context
TREE_MULTIPLE_INSTANCES = """\
_Context_:
    Button: "A pressable element"
---
Form:
  - Field:
      - Button:
          - "@context: variant=primary"
      - Button:
          - "@context: variant=ghost"
---
Button:
  - Icon
"""

# Matches the real tree.yaml structure — deep nesting, multiple @context sites
TREE_DEEP = """\
_Context_:
    Card: "Just a shell container"
    CardHeader: "Just a layout wrapper which positions its children"
    InputGroupInput: "The interactive input element used within an InputGroup"
    InputGroupAddon: "Additional element at start/end of InputGroup, renders children"
---
LoginCard:
  - Card:
      - CardHeader:
          - CardTitle
          - CardSubtitle
      - CardContent:
          - Field:
              - Label:
                  - "@context: NO_CHANGE"
              - InputGroup:
                  - InputGroupInput
                  - InputGroupAddon:
                      - Icon
          - Field:
              - Label
              - InputGroup:
                  - InputGroupInput
                  - InputGroupAddon:
                      - Button:
                          - "@context: variant=ghost, size=icon-sm, icon=eye-closed"
      - CardFooter:
          - Button:
              - "@context: variant=primary, size=lg"
---
Button:
  - Icon
"""


def _write(tmp_path: Path, content: str) -> Path:
    f = tmp_path / "tree.yaml"
    f.write_text(content, encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# Unit helpers
# ---------------------------------------------------------------------------


class TestIsContextAnno:
    def test_valid(self):
        assert _is_context_anno("@context: variant=primary")

    def test_valid_no_value(self):
        assert _is_context_anno("@context:")

    def test_case_insensitive(self):
        assert _is_context_anno("@Context: foo")

    def test_plain_component_name(self):
        assert not _is_context_anno("Button")

    def test_empty_string(self):
        assert not _is_context_anno("")


class TestExtractContextValue:
    def test_simple(self):
        assert _extract_context_value("@context: variant=primary, size=lg") == "variant=primary, size=lg"

    def test_trims_whitespace(self):
        assert _extract_context_value("@context:   size=sm  ") == "size=sm"

    def test_empty_value(self):
        assert _extract_context_value("@context:") == ""

    def test_no_annotation(self):
        assert _extract_context_value("Button") == ""


class TestGetInstanceContext:
    def test_finds_context(self):
        children = ["@context: variant=primary"]
        assert _get_instance_context(children) == "variant=primary"

    def test_returns_none_when_absent(self):
        children = ["Icon", "Label"]
        assert _get_instance_context(children) is None

    def test_returns_none_for_non_list(self):
        assert _get_instance_context(None) is None
        assert _get_instance_context("string") is None

    def test_mixed_list_ignores_non_context(self):
        children = ["Icon", "@context: size=sm", "Label"]
        assert _get_instance_context(children) == "size=sm"


# ---------------------------------------------------------------------------
# list_components
# ---------------------------------------------------------------------------


class TestListComponents:
    def test_returns_sorted_unique_names(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_PLAIN))
        assert names == sorted(set(names))

    def test_includes_root_and_nested_components(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_PLAIN))
        assert "LoginCard" in names
        assert "Card" in names
        assert "CardHeader" in names
        assert "CardTitle" in names
        assert "Button" in names
        assert "Icon" in names

    def test_excludes_context_block_key(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_FULL))
        assert "_Context_" not in names

    def test_excludes_global_context_values(self, tmp_path):
        # "A shell container" and "A pressable element" must not appear as names
        names = list_components(_write(tmp_path, TREE_FULL))
        for n in names:
            assert "shell" not in n.lower()
            assert "pressable" not in n.lower()

    def test_excludes_context_annotations(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_WITH_INSTANCE_CONTEXT))
        for n in names:
            assert not n.startswith("@context")
            assert not n.startswith("variant=")
            assert not n.startswith("size=")

    def test_no_duplicates(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_DEEP))
        assert len(names) == len(set(names))

    def test_deep_tree_all_components(self, tmp_path):
        names = list_components(_write(tmp_path, TREE_DEEP))
        for expected in ["LoginCard", "Card", "CardHeader", "CardTitle", "CardSubtitle",
                         "CardContent", "Field", "Label", "InputGroup", "InputGroupInput",
                         "InputGroupAddon", "Icon", "Button", "CardFooter"]:
            assert expected in names, f"Expected '{expected}' in component list"


# ---------------------------------------------------------------------------
# list_deps
# ---------------------------------------------------------------------------


class TestListDeps:
    def test_root_deps_plain(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_PLAIN), "LoginCard")
        assert "Card" in deps
        assert "CardHeader" in deps
        assert "CardTitle" in deps
        assert "CardSubtitle" in deps
        assert "CardFooter" in deps
        assert "Button" in deps

    def test_root_deps_with_instance_context(self, tmp_path):
        # @context annotations must not appear as dependency names
        deps = list_deps(_write(tmp_path, TREE_WITH_INSTANCE_CONTEXT), "LoginCard")
        for d in deps:
            assert not d.startswith("@context")
            assert not d.startswith("variant=")
        assert "Button" in deps

    def test_root_deps_with_global_context(self, tmp_path):
        # _Context_ front matter must not pollute the dependency list
        deps = list_deps(_write(tmp_path, TREE_FULL), "LoginCard")
        assert "_Context_" not in deps
        assert "Card" in deps
        assert "Button" in deps

    def test_leaf_component_deps(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_PLAIN), "Button")
        assert deps == ["Icon"]

    def test_component_no_block_returns_empty(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_PLAIN), "CardTitle")
        assert deps == []

    def test_unknown_component_returns_empty(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_PLAIN), "NonExistent")
        assert deps == []

    def test_sorted(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_DEEP), "LoginCard")
        assert deps == sorted(deps)

    def test_deep_tree_deps_exclude_annotations(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_DEEP), "LoginCard")
        for d in deps:
            assert not d.startswith("@context")
            assert not d.startswith("variant=")
            assert not d.startswith("NO_CHANGE")

    def test_deep_tree_all_deps_present(self, tmp_path):
        deps = list_deps(_write(tmp_path, TREE_DEEP), "LoginCard")
        for expected in ["Card", "CardHeader", "CardTitle", "CardSubtitle",
                         "CardContent", "Field", "Label", "InputGroup",
                         "InputGroupInput", "InputGroupAddon", "Icon", "Button",
                         "CardFooter"]:
            assert expected in deps


# ---------------------------------------------------------------------------
# get_context
# ---------------------------------------------------------------------------


class TestGetContextStructure:
    """get_context always returns {"global": ..., "instances": [...]}."""

    def test_returns_required_keys(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_PLAIN), "Button")
        assert "global" in result
        assert "instances" in result

    def test_no_context_at_all(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_PLAIN), "Button")
        assert result["global"] is None
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert annotated == []

    def test_unknown_component(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_PLAIN), "NonExistent")
        assert result["global"] is None
        assert result["instances"] == []


class TestGetContextGlobal:
    def test_present(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_FULL), "Button")
        assert result["global"] == "A pressable element"

    def test_present_for_another_component(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_FULL), "Card")
        assert result["global"] == "A shell container"

    def test_absent_when_no_front_matter(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_PLAIN), "Button")
        assert result["global"] is None

    def test_absent_for_unlisted_component(self, tmp_path):
        # Icon is not in the _Context_ block
        result = get_context(_write(tmp_path, TREE_FULL), "Icon")
        assert result["global"] is None


class TestGetContextInstances:
    def test_single_instance(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_FULL), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert len(annotated) == 1
        assert annotated[0]["context"] == "variant=primary, size=lg"

    def test_instance_path_trace(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_FULL), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert annotated[0]["path"] == ["LoginCard", "Card", "CardFooter", "Button"]

    def test_multiple_instances_count(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_MULTIPLE_INSTANCES), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert len(annotated) == 2

    def test_multiple_instances_contexts(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_MULTIPLE_INSTANCES), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        contexts = {i["context"] for i in annotated}
        assert "variant=primary" in contexts
        assert "variant=ghost" in contexts

    def test_no_instance_context_when_unannotated(self, tmp_path):
        # Button appears as plain string leaf in TREE_GLOBAL_CONTEXT_ONLY
        result = get_context(_write(tmp_path, TREE_GLOBAL_CONTEXT_ONLY), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert annotated == []

    def test_own_definition_block_not_an_instance(self, tmp_path):
        # Button's own definition block "Button: - Icon" must not appear in instances
        result = get_context(_write(tmp_path, TREE_FULL), "Button")
        for inst in result["instances"]:
            assert inst["path"][0] != "Button"

    def test_instance_context_absent_returns_none(self, tmp_path):
        # A plain leaf like "Button" (no dict wrapper, no @context) yields context=None
        result = get_context(_write(tmp_path, TREE_GLOBAL_CONTEXT_ONLY), "Button")
        for inst in result["instances"]:
            assert inst["context"] is None


class TestGetContextDeepTree:
    """Validates real-world-like deep nesting with the full LoginCard tree."""

    def test_button_has_two_annotated_instances(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert len(annotated) == 2

    def test_button_contexts_correct(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        contexts = {i["context"] for i in annotated}
        assert "variant=primary, size=lg" in contexts
        assert "variant=ghost, size=icon-sm, icon=eye-closed" in contexts

    def test_button_addon_path(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        paths = [i["path"] for i in annotated]
        assert [
            "LoginCard", "Card", "CardContent", "Field",
            "InputGroup", "InputGroupAddon", "Button",
        ] in paths

    def test_button_footer_path(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Button")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        paths = [i["path"] for i in annotated]
        assert ["LoginCard", "Card", "CardFooter", "Button"] in paths

    def test_label_context_no_change(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Label")
        annotated = [i for i in result["instances"] if i["context"] is not None]
        assert len(annotated) == 1
        assert annotated[0]["context"] == "NO_CHANGE"

    def test_card_global_context(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "Card")
        assert result["global"] == "Just a shell container"

    def test_input_group_input_global_context(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "InputGroupInput")
        assert result["global"] == "The interactive input element used within an InputGroup"

    def test_component_not_in_global_context(self, tmp_path):
        result = get_context(_write(tmp_path, TREE_DEEP), "CardContent")
        assert result["global"] is None
