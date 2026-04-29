---
name: refresh-plan
description: Refresh the implementation plan by triaging TODOs and clarifying blocked decisions before coding.
argument-hint: "[scope: optional path or topic]"
agent: agent
---

This launcher runs in the built-in `agent` runtime.

Within that runtime, invoke the hidden `todo-planner` custom agent to refresh `docs/implementation_plan.md` using the repository planning workflow.

- Pass `$ARGUMENTS` through as optional scope guidance if it is provided.
- Preserve the planner-only guard rails and work through open clarification items.
- When planning is complete, stop and tell the user to run `/implement-plan-item` for the approved next item.
