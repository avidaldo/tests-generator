#!/usr/bin/env bash
# .github/hooks/inject-planner-context.sh
#
# SubagentStart hook for the todo-planner agent.
# Fires when the todo-planner subagent starts.
# Anything written to stdout is injected into the subagent's context.
#
# Registered in .github/settings.json under:
#   hooks.SubagentStart[matcher="todo-planner"]
#
# Requires: git, grep

set -euo pipefail

# ── Git sanity check ─────────────────────────────────────────────────────────
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "⚠️  Not inside a git repository. Git context unavailable."
  exit 0
fi

# ── Project context ──────────────────────────────────────────────────────────
BRANCH=$(git branch --show-current 2>/dev/null || echo "detached HEAD")
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
LAST_MODIFIED_TODO_FILE=$(git log --diff-filter=M --name-only --pretty=format: -- \
  $(grep -rl --include="*.py" --include="*.ts" --include="*.js" \
    -E "(TODO|ARCH|DESIGN|FIXME|HACK)\s*:" "$REPO_ROOT" 2>/dev/null | head -20) \
  2>/dev/null | grep -v "^$" | head -1 || echo "")

echo "╔══════════════════════════════════════════════════════════╗"
echo "║            TODO PLANNER — CONTEXT INJECTION              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ── Branch and recent history ─────────────────────────────────────────────────
echo "## Git Context"
echo "Branch: $BRANCH"
echo ""
echo "### Recent commits (last 10):"
git log --oneline -10 2>/dev/null || echo "(no commits)"
echo ""

# ── Uncommitted work ─────────────────────────────────────────────────────────
DIRTY=$(git status --short 2>/dev/null)
if [ -n "$DIRTY" ]; then
  echo "### Uncommitted changes:"
  echo "$DIRTY"
  echo ""
  echo "⚠️  There are uncommitted changes. The plan should account for"
  echo "   in-progress work listed above."
  echo ""
fi

# ── TODO inventory ───────────────────────────────────────────────────────────
echo "## Quick TODO Inventory"
echo ""

# Count by type
count_marker() {
  local marker="$1"
  grep -rn --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx" \
    --include="*.jsx" --include="*.java" --include="*.go" --include="*.rs" \
    --include="*.rb" --include="*.md" \
    --exclude-dir=".git" --exclude-dir="node_modules" --exclude-dir=".venv" \
    --exclude-dir="__pycache__" --exclude-dir="dist" --exclude-dir="build" \
    -iE "${marker}\s*:" "$REPO_ROOT" 2>/dev/null | wc -l | tr -d ' '
}

ARCH_COUNT=$(count_marker "ARCH")
DESIGN_COUNT=$(count_marker "DESIGN")
TODO_COUNT=$(count_marker "TODO")
FIXME_COUNT=$(count_marker "FIXME")
HACK_COUNT=$(count_marker "HACK")
TOTAL=$((ARCH_COUNT + DESIGN_COUNT + TODO_COUNT + FIXME_COUNT + HACK_COUNT))

echo "| Marker   | Count |"
echo "|----------|-------|"
echo "| ARCH     | $ARCH_COUNT     |"
echo "| DESIGN   | $DESIGN_COUNT   |"
echo "| TODO     | $TODO_COUNT     |"
echo "| FIXME    | $FIXME_COUNT    |"
echo "| HACK     | $HACK_COUNT     |"
echo "| **Total**| **$TOTAL**  |"
echo ""

# ── Files with most markers (hotspots) ───────────────────────────────────────
echo "### Hotspot files (most markers):"
grep -rn --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx" \
  --include="*.jsx" --include="*.java" --include="*.go" --include="*.rs" \
  --include="*.rb" \
  --exclude-dir=".git" --exclude-dir="node_modules" --exclude-dir=".venv" \
  --exclude-dir="__pycache__" --exclude-dir="dist" --exclude-dir="build" \
  -iE "(TODO|ARCH|DESIGN|FIXME|HACK)\s*:" "$REPO_ROOT" 2>/dev/null \
  | cut -d: -f1 | sort | uniq -c | sort -rn | head -10 \
  | awk '{printf "  %d markers — %s\n", $1, $2}' || echo "  (none found)"
echo ""

# ── Existing plan status ──────────────────────────────────────────────────────
PLAN_FILE="$REPO_ROOT/docs/implementation_plan.md"
if [ -f "$PLAN_FILE" ]; then
  PLAN_MODIFIED=$(git log --oneline -1 -- "$PLAN_FILE" 2>/dev/null || \
    stat -c "%y" "$PLAN_FILE" 2>/dev/null || \
    stat -f "%Sm" "$PLAN_FILE" 2>/dev/null || echo "unknown")
  echo "### ⚠️  Existing plan detected"
  echo "File: docs/implementation_plan.md"
  echo "Last modified: $PLAN_MODIFIED"
  echo ""
  echo "$(head -5 "$PLAN_FILE")"
  echo ""
  echo "Ask the user whether to UPDATE the existing plan or create a fresh one."
  echo ""
fi

echo "════════════════════════════════════════════════════════════"
echo "Context injection complete. Proceed with the todo-analysis skill."
echo "════════════════════════════════════════════════════════════"
