#!/usr/bin/env python3
"""PostToolUse hook that reminds when source changes have no matching doc updates."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PATCH_PATH_PATTERN = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (?P<path>.+?)(?: -> .+)?$", re.MULTILINE)


def _normalize_repo_path(raw_path: str) -> str | None:
    path = Path(raw_path)
    candidate = path.resolve() if path.is_absolute() else (REPO_ROOT / path).resolve()
    try:
        return candidate.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return None


def _extract_candidate_paths(data: dict) -> set[str]:
    tool_input = data.get("tool_input") or data.get("input") or {}
    candidate_paths: set[str] = set()

    for key in ("filePath", "file_path", "path", "newPath", "new_path", "target_file", "filename", "dirPath", "dir_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            normalized = _normalize_repo_path(value.strip())
            if normalized:
                candidate_paths.add(normalized)

    patch_text = tool_input.get("input")
    if isinstance(patch_text, str):
        for match in PATCH_PATH_PATTERN.finditer(patch_text):
            normalized = _normalize_repo_path(match.group("path").strip())
            if normalized:
                candidate_paths.add(normalized)

    return candidate_paths


def _matches_trigger(path: str) -> bool:
    return (
        (path.startswith("editor/") and path.endswith(".py"))
        or (path.startswith("resources/") and path.endswith(".py"))
        or (path.startswith("results/") and path.endswith(".ipynb"))
    )


def _is_sync_surface(path: str) -> bool:
    return (
        path == ".github/implementation_plan.md"
        or path == "README.md"
        or path == "AGENTS.md"
        or path == ".github/README.md"
        or path == ".github/AGENTS.md"
        or path.endswith("/AGENTS.md")
        or path == ".github/copilot-instructions.md"
        or path.startswith("docs/")
        or (path.startswith(".github/") and path.endswith(".md"))
        or path.startswith(".github/instructions/")
    )


def _changed_repo_paths() -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()

    changed_paths: set[str] = set()
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path_text = line[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        if path_text:
            changed_paths.add(path_text.strip())
    return changed_paths


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError, ValueError):
        sys.exit(0)

    candidate_paths = _extract_candidate_paths(data)
    if not any(_matches_trigger(path) for path in candidate_paths):
        sys.exit(0)

    changed_paths = _changed_repo_paths()
    changed_trigger_paths = sorted(path for path in changed_paths if _matches_trigger(path))
    changed_sync_paths = sorted(path for path in changed_paths if _is_sync_surface(path))

    if not changed_trigger_paths or changed_sync_paths:
        sys.exit(0)

    preview = ", ".join(changed_trigger_paths[:3])
    if len(changed_trigger_paths) > 3:
        preview = f"{preview}, +{len(changed_trigger_paths) - 3} more"

    print(json.dumps({
        "systemMessage": (
            "Living-docs reminder: source changes "
            f"({preview}) currently have no matching updates in docs/, .github/, AGENTS.md, README.md, "
            "or .github/implementation_plan.md. If behavior or workflow changed, sync the plan and the relevant docs before finishing."
        )
    }))


if __name__ == "__main__":
    main()