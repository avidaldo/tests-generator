---
name: run-batch-maintenance
description: Run the advanced unattended maintenance workflow for approved and unblocked plan items.
argument-hint: "[scope or starting item: optional]"
agent: batch-maintainer
---

Run the advanced batch-maintenance workflow from `.github/implementation_plan.md`.

- Treat `$ARGUMENTS` as optional scope guidance or a preferred starting item when it is provided.
- Keep the canonical safe path unchanged; this launcher is for long unattended runs.