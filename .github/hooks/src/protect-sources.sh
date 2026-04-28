#!/usr/bin/env bash
# .claude/hooks/protect-sources.sh
#
# PreToolUse hook: blocks Write/Edit/MultiEdit calls to source files
# while the todo-planner subagent is active.
#
# Strategy: SubagentStart creates a flag file at
#   /tmp/claude_planner_<session_id>
# SubagentStop removes it. This hook checks for the flag and blocks
# any write to a path that is NOT docs/implementation_plan.md.
#
# Registered in .claude/settings.json under:
#   hooks.PreToolUse[matcher="Write|Edit|MultiEdit"]
#
# NOTE: This hook fires for ALL agents in the project. It is a no-op
# unless the todo-planner flag file is present for this session.

set -euo pipefail

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
FLAG_FILE="/tmp/claude_planner_${SESSION_ID}"

# Not in a todo-planner session — allow everything
if [ ! -f "$FLAG_FILE" ]; then
  exit 0
fi

# In a todo-planner session — check the target path
FILE_PATH=$(echo "$INPUT" | jq -r '
  .tool_input.file_path //
  .tool_input.path //
  .tool_input.new_path //
  empty
' 2>/dev/null || echo "")

ALLOWED_PATH="docs/implementation_plan.md"

if [ -z "$FILE_PATH" ]; then
  # Cannot determine target — allow with warning
  echo "⚠️  todo-planner: write target unknown; proceeding with caution" >&2
  exit 0
fi

# Normalize: strip leading ./ for comparison
FILE_PATH_NORM="${FILE_PATH#./}"

if [ "$FILE_PATH_NORM" = "$ALLOWED_PATH" ]; then
  # Writing to the plan file — allowed
  exit 0
fi

# Any other write target — blocked
cat >&2 << MSG
╔══════════════════════════════════════════════════════════════╗
║  BLOCKED by todo-planner guard                               ║
╠══════════════════════════════════════════════════════════════╣
║  The todo-planner agent is in planning mode only.            ║
║  It may not modify source files.                             ║
║                                                              ║
║  Blocked path : $FILE_PATH_NORM
║  Allowed path : $ALLOWED_PATH
║                                                              ║
║  If you want to implement changes, finish the plan first,    ║
║  then switch to the standard agent or a new conversation.    ║
╚══════════════════════════════════════════════════════════════╝
MSG
exit 2
