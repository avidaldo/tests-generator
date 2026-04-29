#!/usr/bin/env python3
"""PreToolUse hook that restricts todo-planner writes to docs/implementation_plan.md."""

# TODO: but shouldn't the us of this script be defined in a json? I cannot find it

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWED_PATHS = {"docs", "docs/implementation_plan.md"}
PATCH_PATH_PATTERN = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (?P<path>.+?)(?: -> .+)?$", re.MULTILINE)


def _normalize_repo_path(raw_path: str) -> str | None:
    path = Path(raw_path)
    candidate = path.resolve() if path.is_absolute() else (REPO_ROOT / path).resolve()
    try:
        return candidate.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return None


def _extract_candidate_paths(payload: dict) -> set[str]:
    candidate_paths: set[str] = set()

    for key in ("filePath", "file_path", "path", "newPath", "new_path", "target_file", "filename", "dirPath", "dir_path"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            normalized = _normalize_repo_path(value.strip())
            if normalized:
                candidate_paths.add(normalized)

    files_value = payload.get("files")
    if isinstance(files_value, list):
        for value in files_value:
            if isinstance(value, str) and value.strip():
                normalized = _normalize_repo_path(value.strip())
                if normalized:
                    candidate_paths.add(normalized)

    patch_text = payload.get("input")
    if isinstance(patch_text, str):
        for match in PATCH_PATH_PATTERN.finditer(patch_text):
            normalized = _normalize_repo_path(match.group("path").strip())
            if normalized:
                candidate_paths.add(normalized)

    return candidate_paths


def _is_allowed(path: str) -> bool:
    return path in ALLOWED_PATHS


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError, ValueError):
        sys.exit(0)

    tool_input = data.get("tool_input") or data.get("input") or {}
    candidate_paths = _extract_candidate_paths(tool_input)

    if not candidate_paths:
        sys.exit(0)

    disallowed = sorted(path for path in candidate_paths if not _is_allowed(path))
    if not disallowed:
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "todo-planner may only update docs/implementation_plan.md",
            "additionalContext": "Switch to the sdd-implementer agent after the plan is reviewed if you need to modify code or other docs.",
        }
    }))


if __name__ == "__main__":
    main()