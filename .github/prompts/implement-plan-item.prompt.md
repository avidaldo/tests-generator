---
description: >
  Implement the next approved unblocked item from .github/implementation_plan.md
  for the advanced unattended maintenance lane.
---

# Implement Maintenance Plan Item

Complete exactly one approved and unblocked item from `.github/implementation_plan.md`.

## Required Inputs

- The current contents of `.github/implementation_plan.md`
- Any directly affected docs, instructions, or code for the selected item
- The current PR / branch isolation state

## Procedure

1. Read `.github/implementation_plan.md` first.
2. Verify the current execution surface is safe for PR-oriented work.
3. Select the next queue item whose status is approved and unblocked.
4. Implement the smallest complete change for that item only.
5. Validate the touched slice using existing repository checks where available.
6. Update `.github/implementation_plan.md` with the item's result, validation note, and any newly discovered blocker.
7. Sync any directly affected docs and instruction files before stopping.

## Stop Conditions

- No approved unblocked items remain.
- The next item depends on unresolved clarification or decision work.
- Repository state is unsafe or validation fails and cannot be repaired confidently within the current item.

## Output Contract

- Do not silently skip blockers; record them in the plan.
- Do not batch multiple queue items into one pass.
