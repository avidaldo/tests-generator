#!/usr/bin/env python3
"""PostToolUse hook: remind agents to sync docs after prompt/customization changes.

Receives tool invocation details as JSON on stdin. When the current file write
targets prompt files or chat customization files, the hook inspects the working
tree and emits a non-blocking reminder if none of the registered documentation
surfaces have been updated yet.

Exit codes:
  0  — success or no action (never blocks the agent)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
_PATCH_PATH_PATTERN = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (?P<path>.+?)(?: -> .+)?$", re.MULTILINE)
_TRIGGER_GLOBS = (
    "prompts/*.prompt.md",
    ".github/instructions/*.instructions.md",
    ".github/skills/*/SKILL.md",
    ".github/agents/*.agent.md",
    ".github/hooks/*.json",
)
_SYNC_SURFACES = {
    "README.md",
    "AGENTS.md",
    "prompts/AGENTS.md",
    ".github/copilot-instructions.md",
}


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

    for key in ("filePath", "file_path", "path", "target_file", "filename", "dirPath", "dir_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            normalized = _normalize_repo_path(value.strip())
            if normalized:
                candidate_paths.add(normalized)

    patch_text = tool_input.get("input")
    if isinstance(patch_text, str):
        for match in _PATCH_PATH_PATTERN.finditer(patch_text):
            normalized = _normalize_repo_path(match.group("path").strip())
            if normalized:
                candidate_paths.add(normalized)

    return candidate_paths


def _matches_trigger(path: str) -> bool:
    return any(fnmatch(path, pattern) for pattern in _TRIGGER_GLOBS)


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
    changed_sync_paths = sorted(path for path in changed_paths if path in _SYNC_SURFACES)

    if not changed_trigger_paths or changed_sync_paths:
        sys.exit(0)

    preview = ", ".join(changed_trigger_paths[:3])
    if len(changed_trigger_paths) > 3:
        preview = f"{preview}, +{len(changed_trigger_paths) - 3} more"

    sync_list = ", ".join(sorted(_SYNC_SURFACES))
    print(json.dumps({
        "systemMessage": (
            "Documentation sync reminder: prompt/customization changes "
            f"({preview}) currently have no matching updates in {sync_list}. "
            "If the workflow or customization surface changed, update the relevant docs before finishing."
        )
    }))

    sys.exit(0)


if __name__ == "__main__":
    main()
