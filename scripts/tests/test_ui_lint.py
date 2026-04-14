#!/usr/bin/env python3
"""Tests for ui-lint.py."""

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module loading
# ---------------------------------------------------------------------------

_SCRIPT = Path(__file__).resolve().parent.parent / "ui-lint.py"
_spec = importlib.util.spec_from_file_location("ui_lint", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

lint = _mod.lint
LintError = _mod.LintError
_looks_collapsed = _mod._looks_collapsed
_is_context_anno = _mod._is_context_anno


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(tmp_path: Path, content: str) -> Path:
    f = tmp_path / "tree.yaml"
    f.write_text(content, encoding="utf-8")
    return f


def _messages(errors: list) -> list:
    return [e.message for e in errors]


def _has_collapsed_error(errors: list) -> bool:
    return any('multiple components merged' in e.message for e in errors)


# ---------------------------------------------------------------------------
# Unit tests for helper functions
# ---------------------------------------------------------------------------


class TestLooksCollapsed:
    def test_two_components(self):
        assert _looks_collapsed("Foo - Bar") is True

    def test_three_components(self):
        assert _looks_collapsed("Select - SelectTrigger - SelectValue") is True

    def test_many_components(self):
        assert _looks_collapsed(
            "Select - SelectTrigger - SelectValue - Icon - SelectContent - SelectItem"
        ) is True

    def test_single_component_is_not_collapsed(self):
        assert _looks_collapsed("Button") is False

    def test_single_word_with_hyphen_is_not_collapsed(self):
        # a plain word with hyphens (rn-style names) shouldn't match
        assert _looks_collapsed("my-component") is False

    def test_context_annotation_is_not_collapsed(self):
        assert _looks_collapsed("@context: ghost button variant") is False

    def test_description_with_dash_not_collapsed(self):
        # lowercase words don't match — component names must start with uppercase
        assert _looks_collapsed("ghost - primary") is False

    def test_mixed_case_not_collapsed(self):
        # second token starts lowercase — not a collapsed scalar
        assert _looks_collapsed("Button - icon") is False

    def test_leading_whitespace_ignored(self):
        assert _looks_collapsed("  Foo - Bar  ") is True


class TestIsContextAnno:
    def test_basic(self):
        assert _is_context_anno("@context: primary") is True

    def test_case_insensitive(self):
        assert _is_context_anno("@Context: primary") is True

    def test_with_leading_whitespace(self):
        assert _is_context_anno("  @context: primary  ") is True

    def test_regular_string(self):
        assert _is_context_anno("Button") is False


# ---------------------------------------------------------------------------
# Clean YAML — should pass without errors
# ---------------------------------------------------------------------------


class TestCleanFiles:
    def test_minimal_clean(self, tmp_path: Path):
        content = """\
Button:
  - Icon
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_clean_with_context_frontmatter(self, tmp_path: Path):
        content = """\
_Context_:
  Button: "A pressable element"
---
Button:
  - Icon
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_clean_with_instance_context(self, tmp_path: Path):
        content = """\
Card:
  - CardHeader:
    - CardTitle
  - CardFooter:
    - Button:
      - "@context: primary button variant"
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_leaf_component_no_children(self, tmp_path: Path):
        # A doc with just a bare root key and null value is valid
        content = """\
Badge
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_multiple_clean_documents(self, tmp_path: Path):
        content = """\
Card:
  - CardHeader
  - CardFooter
---
Button:
  - Icon
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_homepage_tree_is_clean(self):
        """The actual homepage.tree.yaml in the repo must pass cleanly."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        tree = repo_root / "homepage.tree.yaml"
        if not tree.exists():
            pytest.skip("homepage.tree.yaml not found")
        errors = lint(tree)
        assert errors == [], "\n".join(str(e) for e in errors)


# ---------------------------------------------------------------------------
# YAML parse errors
# ---------------------------------------------------------------------------


class TestYamlParseErrors:
    def test_invalid_yaml_unclosed_bracket(self, tmp_path: Path):
        content = "Button:\n  - [unclosed bracket\n"
        errors = lint(_write(tmp_path, content))
        assert len(errors) == 1
        assert "YAML parse error" in errors[0].message
        assert errors[0].doc_root == "<yaml>"

    def test_invalid_yaml_tab_character(self, tmp_path: Path):
        content = "Button:\n\t- Icon\n"
        errors = lint(_write(tmp_path, content))
        assert len(errors) == 1
        assert "YAML parse error" in errors[0].message

    def test_file_not_found(self, tmp_path: Path):
        errors = lint(tmp_path / "nonexistent.yaml")
        assert len(errors) == 1
        assert "cannot read file" in errors[0].message


# ---------------------------------------------------------------------------
# Collapsed scalar detection (missing ":" on component with children)
# ---------------------------------------------------------------------------


class TestCollapsedScalar:
    def test_collapsed_list_item(self, tmp_path: Path):
        """The classic bug: component with children but no colon."""
        # YAML parses "- Select\n  - SelectTrigger" as one string
        # We must feed the *already parsed* collapsed string directly to
        # reproduce the symptom without relying on YAML folding behaviour.
        content = """\
FindMyMatchCard:
  - "Select - SelectTrigger - SelectValue - Icon"
"""
        errors = lint(_write(tmp_path, content))
        assert _has_collapsed_error(errors)

    def test_collapsed_dict_key(self, tmp_path: Path):
        content = """\
AccordianGroupItem:
  - "AccordianGroupItemTrigger - AccrodianGroupItemTitle - AccordianGroupItemIcon":
    - SomeChild
"""
        errors = lint(_write(tmp_path, content))
        assert _has_collapsed_error(errors)

    def test_two_component_collapsed(self, tmp_path: Path):
        content = """\
Nav:
  - "DropdownMenuTrigger - NavListItem"
"""
        errors = lint(_write(tmp_path, content))
        assert _has_collapsed_error(errors)

    def test_context_annotation_not_flagged(self, tmp_path: Path):
        content = """\
Button:
  - "@context: ghost button variant"
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_single_component_string_not_flagged(self, tmp_path: Path):
        content = """\
Card:
  - CardHeader
  - CardFooter
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []

    def test_error_path_contains_parent(self, tmp_path: Path):
        content = """\
Nav:
  - NavList:
    - "DropdownMenuTrigger - Icon"
"""
        errors = lint(_write(tmp_path, content))
        assert _has_collapsed_error(errors)
        # The error should be inside the Nav doc
        assert all(e.doc_root == "Nav" for e in errors)

    def test_multiple_collapsed_strings(self, tmp_path: Path):
        content = """\
Footer:
  - "FooterColumn - FooterColumnTitle - FooterLink"
  - "FooterNav - FooterNavItem"
"""
        errors = lint(_write(tmp_path, content))
        assert len([e for e in errors if _has_collapsed_error([e])]) == 2


# ---------------------------------------------------------------------------
# Multi-root document
# ---------------------------------------------------------------------------


class TestMultiRootDocument:
    def test_two_roots_in_one_document(self, tmp_path: Path):
        content = """\
Button:
  - Icon
Card:
  - CardHeader
"""
        errors = lint(_write(tmp_path, content))
        assert len(errors) == 1
        assert "2 top-level key(s)" in errors[0].message

    def test_three_roots_in_one_document(self, tmp_path: Path):
        content = """\
A:
  - B
C:
  - D
E:
  - F
"""
        errors = lint(_write(tmp_path, content))
        assert len(errors) == 1
        assert "3 top-level key(s)" in errors[0].message

    def test_multi_root_shows_all_keys_in_message(self, tmp_path: Path):
        content = """\
Button:
  - Icon
Card:
  - CardHeader
"""
        errors = lint(_write(tmp_path, content))
        assert "Button" in errors[0].message
        assert "Card" in errors[0].message


# ---------------------------------------------------------------------------
# Unexpected value types
# ---------------------------------------------------------------------------


class TestUnexpectedValueTypes:
    def test_integer_value(self, tmp_path: Path):
        content = """\
Button:
  speed: 42
"""
        errors = lint(_write(tmp_path, content))
        assert any("unexpected value type" in e.message for e in errors)

    def test_boolean_value(self, tmp_path: Path):
        content = """\
Button:
  active: true
"""
        errors = lint(_write(tmp_path, content))
        assert any("unexpected value type" in e.message for e in errors)


# ---------------------------------------------------------------------------
# Error metadata correctness
# ---------------------------------------------------------------------------


class TestErrorMetadata:
    def test_doc_root_is_set(self, tmp_path: Path):
        content = """\
BrokerCard:
  - "CardHeader - CardTitle"
"""
        errors = lint(_write(tmp_path, content))
        assert all(e.doc_root == "BrokerCard" for e in errors)

    def test_lint_error_str(self, tmp_path: Path):
        content = """\
Nav:
  - "Foo - Bar"
"""
        errors = lint(_write(tmp_path, content))
        assert len(errors) == 1
        s = str(errors[0])
        assert s.startswith("ERROR [doc:Nav]")
        assert "Foo - Bar" in s

    def test_context_frontmatter_never_flagged(self, tmp_path: Path):
        """_Context_ values are plain text — they must never trigger errors."""
        content = """\
_Context_:
  Button: "A pressable element with a primary - secondary variant"
  Card: "Just a wrapper"
---
Card:
  - Button
"""
        errors = lint(_write(tmp_path, content))
        assert errors == []
