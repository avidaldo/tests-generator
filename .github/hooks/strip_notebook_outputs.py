#!/usr/bin/env python3
"""PostToolUse hook: automatically strip outputs from any .ipynb file the agent writes.

Receives tool invocation details as JSON on stdin. Runs nbstripout on any .ipynb
file the agent creates or edits, silently, before the agent continues.

Exit codes:
  0  — success or no .ipynb file targeted (never blocks the agent)
"""

import json
import subprocess
import sys
from pathlib import Path


def extract_file_path(data: dict) -> str | None:
    """Extract the target file path from hook stdin, handling multiple runtime formats.

    VS Code Copilot and Claude Code use different field names for tool inputs;
    this function tries all known variants defensively.
    """
    tool_input = data.get("tool_input") or data.get("input") or {}
    for key in ("filePath", "file_path", "path", "target_file", "filename"):
        value = tool_input.get(key)
        if value and isinstance(value, str):
            return value
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError, ValueError):
        sys.exit(0)

    file_path = extract_file_path(data)

    if not file_path or not file_path.endswith(".ipynb"):
        sys.exit(0)

    path = Path(file_path)
    if not path.exists():
        sys.exit(0)

    result = subprocess.run(
        ["nbstripout", str(path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        # Non-blocking: surface a warning but do not stop the agent.
        # Common cause: nbstripout not installed in the agent's environment.
        print(json.dumps({
            "systemMessage": (
                f"nbstripout could not strip {path} "
                f"(exit {result.returncode}): "
                f"{result.stderr.strip() or 'is nbstripout installed?'}"
            )
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
