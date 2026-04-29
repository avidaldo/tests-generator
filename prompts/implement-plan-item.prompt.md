---
name: implement-plan-item
description: Implement the next approved item from the implementation plan and sync the affected docs and instructions.
argument-hint: "[item id or short target: optional]"
agent: agent
---

This launcher runs in the built-in `agent` runtime.

Within that runtime, invoke the hidden `sdd-implementer` custom agent to implement from `docs/implementation_plan.md`.

- Implement exactly one approved item and then stop.
- If `$ARGUMENTS` is provided, treat it as the preferred approved item to target.
- Otherwise, pick the next approved unblocked item, implement it, update the plan status, and sync the affected docs and instructions before finishing.
- Do not continue to later planned items in the same run, even if more approved work remains.
