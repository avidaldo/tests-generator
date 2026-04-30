# Manual Cloud Prompt For Batch Maintenance

Copy the full prompt block below into a cloud chat session for this repository. If the cloud session lets you pick the `batch-maintainer` custom agent, pick it first; if not, paste the prompt as-is. Replace the optional scope line only when you want to constrain the run or force a preferred starting item.

```text
Act as the repository's `batch-maintainer` agent and run the advanced unattended maintenance workflow from `.github/implementation_plan.md`.

Optional scope guidance or preferred starting item: <leave blank if none>

Follow the repository's existing instruction files and nested `AGENTS.md` files for any files you touch.

You own the advanced unattended maintenance lane.

- Read `.github/implementation_plan.md` before editing anything.
- Treat the optional scope guidance above as optional scope guidance or a preferred starting item when it is provided.
- Keep `.github/prompts/refresh-plan.prompt.md` and `.github/prompts/implement-plan-item.prompt.md` as the canonical precise workflow. This run is the advanced optional lane, not a replacement.
- Before coding, refresh the plan if `TODO:`, `ARCH:`, `DESIGN:`, `FIXME:`, or `HACK:` markers have drifted or the current plan no longer matches the repo state.
- Build a queue of approved and unblocked items only.
- Do not auto-resolve unresolved clarification or decision work. Stop and report those blockers instead.
- Process the queue one item at a time. After each completed item, update `.github/implementation_plan.md` and sync the affected docs and instructions before continuing.
- Use branch isolation appropriate to the current execution surface. Because this is a cloud or PR-oriented run, stay within the remote branch or pull-request isolation model instead of assuming local git state.
- Stop on unsafe repository state, failed remote isolation, unresolved decision items, or validation failures you cannot repair confidently in the current item.
- Finish with a summary of completed items, remaining blockers, and the next safe manual step if the queue stops early.

Workflow:
1. Read `.github/implementation_plan.md` and any directly affected nearby docs.
2. Refresh the plan first if TODO-marker discovery or current repo state shows the plan is stale.
3. Verify isolation for the current execution surface before making changes.
4. Select the next approved unblocked item from the queue.
5. Implement that item, validate the touched slice, update the plan and docs, then continue.
6. Stop when the queue is empty or the first blocking unresolved decision or validation failure is reached.
```
