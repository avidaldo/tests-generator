#!/usr/bin/env python3
"""SessionStart hook for the todo-planner custom agent."""

# TODO: Add detailed comments on how this script works

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = REPO_ROOT / "docs" / "implementation_plan.md"
MARKERS = ("TODO", "ARCH", "DESIGN", "FIXME", "HACK")
TEXT_SUFFIXES = {
    ".agent.md",
    ".instructions.md",
    ".json",
    ".md",
    ".prompt.md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {".git", ".venv", "__pycache__", "build", "dist", "node_modules"}


def _is_text_file(path: Path) -> bool:
    suffixes = path.suffixes
    joined = "".join(suffixes[-2:]) if len(suffixes) >= 2 else path.suffix
    return joined in TEXT_SUFFIXES or path.suffix in TEXT_SUFFIXES


def _marker_counts() -> dict[str, int]:
    counts = {marker: 0 for marker in MARKERS}

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not _is_text_file(path):
            continue

        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for line in lines:
            upper = line.upper()
            for marker in MARKERS:
                if f"{marker}:" in upper:
                    counts[marker] += 1

    return counts


def _git_branch() -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "detached"


def _plan_preview() -> str:
    if not PLAN_PATH.exists():
        return "No implementation plan exists yet. Create docs/implementation_plan.md before planning ends."

    try:
        lines = PLAN_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "Implementation plan exists but could not be read."

    preview = "\n".join(lines[:8]).strip()
    if not preview:
        return "Implementation plan exists but is empty."
    return preview


def main() -> None:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError, ValueError):
        pass

    counts = _marker_counts()
    context = "\n".join([
        "Planning mode is active.",
        f"Branch: {_git_branch()}",
        "Marker counts: "
        + ", ".join(f"{marker}={counts[marker]}" for marker in MARKERS),
        "Rules:",
        "- TODO is the canonical capture marker.",
        "- Question-style TODOs go into the Clarification Queue before implementation.",
        "- You may only update docs/implementation_plan.md in this agent.",
        "Current plan preview:",
        _plan_preview(),
    ])

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()