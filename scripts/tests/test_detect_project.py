#!/usr/bin/env python3
"""Tests for detect-project.py."""

import importlib.util
import json
from pathlib import Path

import pytest

# Load detect-project.py by path (hyphen prevents normal import).
_SCRIPT = Path(__file__).resolve().parent.parent / "detect-project.py"
_spec = importlib.util.spec_from_file_location("detect_project", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]
detect = _mod.detect


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_pkg(directory: Path, content: dict) -> None:
    (directory / "package.json").write_text(json.dumps(content), encoding="utf-8")


def touch(directory: Path, filename: str) -> None:
    (directory / filename).touch()


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


class TestErrors:
    def test_no_package_json(self, tmp_path: Path) -> None:
        result, code = detect(tmp_path)
        assert code == 2
        assert result["error"] is not None
        assert "package.json" in result["error"]
        assert result["platform"] is None
        assert result["confidence"] == "none"

    def test_invalid_json(self, tmp_path: Path) -> None:
        (tmp_path / "package.json").write_text("{not valid json}", encoding="utf-8")
        result, code = detect(tmp_path)
        assert code == 2
        assert result["error"] is not None
        assert result["platform"] is None

    def test_empty_package_json(self, tmp_path: Path) -> None:
        """Empty but valid JSON object — no deps, no lock files."""
        make_pkg(tmp_path, {})
        result, code = detect(tmp_path)
        # platform unknown → exit 1, but not a fatal error
        assert code == 1
        assert result["error"] is None
        assert result["platform"] is None
        assert result["confidence"] == "low"


# ---------------------------------------------------------------------------
# Package manager detection
# ---------------------------------------------------------------------------


class TestPackageManagerDetection:
    def test_npm_via_lock_file(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        touch(tmp_path, "package-lock.json")
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "npm"

    def test_yarn_via_lock_file(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        touch(tmp_path, "yarn.lock")
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "yarn"

    def test_pnpm_via_lock_file(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        touch(tmp_path, "pnpm-lock.yaml")
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "pnpm"

    def test_bun_via_lock_file(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        touch(tmp_path, "bun.lockb")
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "bun"

    def test_packagemanager_field_overrides_lock_file(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {"packageManager": "pnpm@8.0.0", "dependencies": {"react": "^18.0.0"}},
        )
        touch(tmp_path, "yarn.lock")
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "pnpm"

    def test_packagemanager_field_bun(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"packageManager": "bun@1.1.0", "dependencies": {"react": "^18.0.0"}})
        result, _ = detect(tmp_path)
        assert result["package_manager"] == "bun"

    def test_multiple_lock_files_warns_and_picks_highest_priority(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        touch(tmp_path, "yarn.lock")
        touch(tmp_path, "package-lock.json")
        result, _ = detect(tmp_path)
        # bun > yarn > pnpm > npm; yarn is highest present
        assert result["package_manager"] == "yarn"
        assert any("Multiple lock files" in w for w in result["warnings"])

    def test_no_lock_file_warns(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "^18.0.0"}})
        result, _ = detect(tmp_path)
        assert result["package_manager"] is None
        assert any("lock file" in w.lower() for w in result["warnings"])


# ---------------------------------------------------------------------------
# Platform & stack detection
# ---------------------------------------------------------------------------


class TestReactNativeDetection:
    def test_expo_project(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {"dependencies": {"expo": "~50.0.0", "react-native": "0.73.6", "react": "18.2.0"}},
        )
        result, code = detect(tmp_path)
        assert code == 0
        assert result["platform"] == "react-native"
        assert result["stack"] == "expo"
        assert result["confidence"] == "high"

    def test_react_native_cli_project(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {"dependencies": {"react-native": "0.73.6", "react": "18.2.0"}},
        )
        result, code = detect(tmp_path)
        assert code == 0
        assert result["platform"] == "react-native"
        assert result["stack"] == "react-native-cli"
        assert result["confidence"] == "high"

    def test_expo_in_dev_deps(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {"devDependencies": {"expo": "~50.0.0"}, "dependencies": {"react": "18.2.0"}},
        )
        result, _ = detect(tmp_path)
        assert result["platform"] == "react-native"
        assert result["stack"] == "expo"


class TestWebDetection:
    def test_next_project(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"next": "14.0.0", "react": "18.2.0"}})
        result, code = detect(tmp_path)
        assert code == 0
        assert result["platform"] == "web"
        assert result["stack"] == "next"
        assert result["confidence"] == "high"

    def test_vite_project(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {"dependencies": {"react": "18.2.0"}, "devDependencies": {"vite": "5.0.0"}},
        )
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "vite"
        assert result["confidence"] == "high"

    def test_cra_project(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "18.2.0", "react-scripts": "5.0.0"}})
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "cra"

    def test_remix_project(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "18.2.0", "@remix-run/react": "2.0.0"}})
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "remix"

    def test_gatsby_project(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "18.2.0", "gatsby": "5.0.0"}})
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "gatsby"

    def test_astro_project(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "18.2.0", "astro": "4.0.0"}})
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "astro"

    def test_plain_react_medium_confidence(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"react": "18.2.0", "react-dom": "18.2.0"}})
        result, code = detect(tmp_path)
        assert code == 1
        assert result["platform"] == "web"
        assert result["stack"] == "react"
        assert result["confidence"] == "medium"

    def test_web_framework_without_react_is_medium_confidence(self, tmp_path: Path) -> None:
        """vite present but no react dep yet (library/plugin setup)."""
        make_pkg(tmp_path, {"devDependencies": {"vite": "5.0.0"}})
        result, _ = detect(tmp_path)
        assert result["platform"] == "web"
        assert result["stack"] == "vite"
        assert result["confidence"] == "medium"


# ---------------------------------------------------------------------------
# TypeScript detection
# ---------------------------------------------------------------------------


class TestTypescriptDetection:
    def test_typescript_in_dev_deps(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {
                "dependencies": {"next": "14.0.0", "react": "18.2.0"},
                "devDependencies": {"typescript": "5.0.0"},
            },
        )
        result, _ = detect(tmp_path)
        assert result["typescript"] is True

    def test_typescript_via_tsconfig(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"next": "14.0.0", "react": "18.2.0"}})
        touch(tmp_path, "tsconfig.json")
        result, _ = detect(tmp_path)
        assert result["typescript"] is True

    def test_typescript_via_tsconfig_base(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"next": "14.0.0", "react": "18.2.0"}})
        touch(tmp_path, "tsconfig.base.json")
        result, _ = detect(tmp_path)
        assert result["typescript"] is True

    def test_no_typescript(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"next": "14.0.0", "react": "18.2.0"}})
        result, _ = detect(tmp_path)
        assert result["typescript"] is False


# ---------------------------------------------------------------------------
# Combined / realistic scenarios
# ---------------------------------------------------------------------------


class TestRealisticScenarios:
    def test_full_expo_typescript_yarn(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {
                "dependencies": {
                    "expo": "~50.0.0",
                    "react": "18.2.0",
                    "react-native": "0.73.6",
                },
                "devDependencies": {"typescript": "5.3.0"},
            },
        )
        touch(tmp_path, "yarn.lock")
        result, code = detect(tmp_path)
        assert code == 0
        assert result["platform"] == "react-native"
        assert result["stack"] == "expo"
        assert result["package_manager"] == "yarn"
        assert result["typescript"] is True
        assert result["error"] is None
        assert result["warnings"] == []

    def test_full_next_typescript_pnpm(self, tmp_path: Path) -> None:
        make_pkg(
            tmp_path,
            {
                "dependencies": {"next": "14.0.0", "react": "18.2.0"},
                "devDependencies": {"typescript": "5.3.0"},
            },
        )
        touch(tmp_path, "pnpm-lock.yaml")
        result, code = detect(tmp_path)
        assert code == 0
        assert result["platform"] == "web"
        assert result["stack"] == "next"
        assert result["package_manager"] == "pnpm"
        assert result["typescript"] is True

    def test_result_is_json_serialisable(self, tmp_path: Path) -> None:
        make_pkg(tmp_path, {"dependencies": {"expo": "~50.0.0", "react": "18.2.0"}})
        result, _ = detect(tmp_path)
        serialised = json.dumps(result)
        parsed = json.loads(serialised)
        assert parsed["platform"] == "react-native"
