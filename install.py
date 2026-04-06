#!/usr/bin/env python3
"""Safely install the live agent and skill files into a .copilot tree.

The script mirrors the repository's top-level `agents/` and `skills/`
directories into a destination `.copilot/` directory. It only touches files
that are new, changed, or stale, and prints a detailed per-file report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SOURCE_DIRS = ("agents", "skills")


@dataclass(frozen=True)
class FileAction:
    action: str
    path: Path
    detail: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mirror live agents and skills into a .copilot directory."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Repository root containing the agents/ and skills/ directories.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path(".copilot"),
        help="Destination .copilot directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing anything.",
    )
    return parser.parse_args()


def normalize_dest(dest: Path, source_root: Path) -> Path:
    if not dest.is_absolute():
        return (source_root / dest).resolve()
    return dest.resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def iter_source_files(source_root: Path) -> list[tuple[Path, Path, str]]:
    files: list[tuple[Path, Path, str]] = []
    for folder_name in SOURCE_DIRS:
        folder = source_root / folder_name
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(source_root)
            files.append((path, relative, folder_name))
    return sorted(files, key=lambda item: str(item[1]))


def destination_path(dest_root: Path, relative_path: Path) -> Path:
    return dest_root / relative_path


def write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        if path.exists():
            shutil.copymode(path, temp_path)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def prune_stale(dest_root: Path, source_relative_paths: set[Path], dry_run: bool) -> list[FileAction]:
    actions: list[FileAction] = []
    for folder_name in SOURCE_DIRS:
        target_root = dest_root / folder_name
        if not target_root.exists():
            continue
        for path in sorted(target_root.rglob("*"), reverse=True):
            if not path.is_file():
                continue
            relative = path.relative_to(dest_root)
            if relative in source_relative_paths:
                continue
            actions.append(FileAction("delete", relative))
            if not dry_run:
                path.unlink()
    return actions


def install_files(source_root: Path, dest_root: Path, dry_run: bool) -> list[FileAction]:
    actions: list[FileAction] = []
    source_files = iter_source_files(source_root)
    source_relative_paths = {relative for _, relative, _ in source_files}

    for source_path, relative_path, _ in source_files:
        target_path = destination_path(dest_root, relative_path)
        source_content = read_bytes(source_path)

        if target_path.exists():
            target_content = read_bytes(target_path)
            if sha256_bytes(source_content) == sha256_bytes(target_content):
                continue
            actions.append(FileAction("overwrite", relative_path))
            if not dry_run:
                write_atomic(target_path, source_content)
        else:
            actions.append(FileAction("create", relative_path))
            if not dry_run:
                write_atomic(target_path, source_content)

    actions.extend(prune_stale(dest_root, source_relative_paths, dry_run))
    return actions


def format_report(actions: list[FileAction], dest_root: Path, dry_run: bool) -> str:
    lines = []
    header = "Dry run" if dry_run else "Install complete"
    lines.append(f"{header}: {len(actions)} file(s) touched in {dest_root}")
    if not actions:
        lines.append("No create, overwrite, or delete operations were needed.")
        return "\n".join(lines)

    for action in actions:
        suffix = f" - {action.detail}" if action.detail else ""
        lines.append(f"{action.action.upper():9} {action.path}{suffix}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    dest_root = normalize_dest(args.dest, source_root)

    if not source_root.exists():
        print(f"Source root does not exist: {source_root}", file=sys.stderr)
        return 1

    if dest_root == source_root:
        print("Destination must not be the same as the source root.", file=sys.stderr)
        return 1

    for folder_name in SOURCE_DIRS:
        source_folder = (source_root / folder_name).resolve()
        if dest_root == source_folder or dest_root.is_relative_to(source_folder):
            print(
                f"Destination must not be inside the source tree: {source_folder}",
                file=sys.stderr,
            )
            return 1

    actions = install_files(source_root, dest_root, args.dry_run)
    print(format_report(actions, dest_root, args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())