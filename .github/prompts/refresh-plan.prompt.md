---
description: >
  Refresh .github/implementation_plan.md from the current repository state for
  the advanced unattended maintenance lane.
---

# Refresh Maintenance Plan

Update `.github/implementation_plan.md` so it matches the repository's current state.

## Required Inputs

- The current contents of `.github/implementation_plan.md`
- Any nearby docs or instruction files affected by queued maintenance items
- A current scan for tracked `TODO:`, `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` markers

## Procedure

1. Read `.github/implementation_plan.md` before editing anything else.
2. Compare the plan with the current repository state and the latest marker scan.
3. Keep only approved and unblocked implementation items in the active queue.
4. Move unresolved clarification, architecture, or product-decision work into a blocked / decision section instead of implementing it.
5. Preserve completed items with short validation notes so later runs can see what already landed.
6. Update any directly affected docs or instruction files if the plan's workflow contract changes.

## Output Contract

- Do not invent roadmap work that is not grounded in the repository state.
- Keep statuses explicit: `approved`, `blocked`, `done`, or `dropped`.
- Stop after refreshing the plan; do not implement queued items in the same pass unless explicitly asked.
