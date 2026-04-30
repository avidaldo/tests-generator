#!/usr/bin/env python3
"""SessionStart hook for the todo-planner custom agent.

Configured in `.github/agents/todo-planner.agent.md` as an agent-scoped hook so
it only runs for planner sessions. It injects a small planning snapshot instead
of relying on a workspace-wide hook.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PLAN_PATH = REPO_ROOT / ".github" / "implementation_plan.md"
DEBUG_ENV_VAR = "TODO_PLANNER_CONTEXT_DEBUG"
DEFAULT_DEBUG_LOG_PATH = Path(tempfile.gettempdir()) / REPO_ROOT.name / "todo_planner_context.json"
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
    # Give the planner a small queue-size signal without rescanning interactively first.
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
        return "No implementation plan exists yet. Create .github/implementation_plan.md before planning ends."

    try:
        lines = PLAN_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "Implementation plan exists but could not be read."

    preview = "\n".join(lines[:8]).strip()
    if not preview:
        return "Implementation plan exists but is empty."
    return preview


def _resolve_debug_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def _debug_log_path(argv: list[str]) -> Path | None:
    for arg in argv:
        if arg == "--debug":
            return DEFAULT_DEBUG_LOG_PATH
        if arg.startswith("--debug="):
            path_text = arg.split("=", 1)[1].strip()
            if path_text:
                return _resolve_debug_path(path_text)

    env_value = os.getenv(DEBUG_ENV_VAR, "").strip()
    if not env_value:
        return None

    normalized = env_value.lower()
    if normalized in {"0", "false", "no", "off"}:
        return None
    if normalized in {"1", "true", "yes", "on"}:
        return DEFAULT_DEBUG_LOG_PATH
    return _resolve_debug_path(env_value)


def _write_debug_log(debug_path: Path, payload: str) -> None:
    try:
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(payload + "\n", encoding="utf-8")
    except OSError:
        pass


def main() -> None:
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError, ValueError):
        pass

    counts = _marker_counts()
    # Keep injected context compact: branch, marker counts, and a short plan preview.
    context = "\n".join([
        "Planning mode is active.",
        f"Branch: {_git_branch()}",
        "Marker counts: "
        + ", ".join(f"{marker}={counts[marker]}" for marker in MARKERS),
        "Rules:",
        "- TODO is the canonical capture marker.",
        "- Question-style TODOs go into the Clarification Queue before implementation.",
        "- You may only update .github/implementation_plan.md in this agent.",
        "Current plan preview:",
        _plan_preview(),
    ])

    payload = json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    })

    print(payload)

    debug_path = _debug_log_path(sys.argv[1:])
    if debug_path is not None:
        _write_debug_log(debug_path, payload)


if __name__ == "__main__":
    main()
