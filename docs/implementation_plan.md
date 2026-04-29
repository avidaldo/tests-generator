# Implementation Plan

> Updated: 2026-04-29
> Branch: decomposed
> Status: active

## Working Agreements

- `TODO:` is the canonical capture marker.
- Question-style TODOs stay in the Clarification Queue until resolved.
- Implement one approved item at a time.
- Update this file and the relevant docs and instructions after each meaningful implementation step.

## Clarification Queue

| ID | Status | Source | Question | Next step |
| --- | --- | --- | --- | --- |
| Q1 | open | `resources/convert_xml_to_md.py:1` | When should XML-to-Markdown conversion be part of the workflow, and should that behavior stay as a script, become a skill resource, or disappear? | Inspect actual usage sites and decide whether it belongs in the prompt pipeline or should be removed |
| Q2 | open | `prompts/summarize-sources.prompt.md:27`, `prompts/merge-summaries.prompt.md:23` | Should language transformation happen only at question generation, with earlier stages preserving the source language? | Review the Subject Profile flow across all three prompt stages and decide the single consistent model |
| Q3 | open | `prompts/summarize-sources.prompt.md:133`, `README.md:48-49` | Should summarization explicitly ban external knowledge and recommend per-material subagent fan-out for context control? | Review the current prompt wording and the actual capabilities of the target agents before editing the prompts |
| Q4 | open | `prompts/generate-questions.prompt.md:15`, `prompts/generate-questions.prompt.md:198` | How should the adversarial-feedback rule be clarified, and where should the editor JSON schema live as a single source of truth? | Compare the prompt output block with the editor state schema and decide whether a shared schema doc is needed |
| Q5 | open | `editor/v3/README.md:3` | Should editor v3 graduate to the main `editor/` path, or is the current split still useful for the repo's didactic purpose? | Review migration cost, import paths, and the documentation impact before moving files |

## Planned Work

| ID | Status | Type | Summary | Source | Depends on |
| --- | --- | --- | --- | --- | --- |
| P1 | completed | decision | Define the customization architecture for the SDD and living-documentation loop | `AGENTS.md:3`, old planner TODOs | none |
| P2 | completed | action | Replace the stale planner setup with explicit planner and implementer custom agents plus planner guard rails | old `.github/agents/todo-planner.md`, `.github/skills/todo-analysis/SKILL.md` | P1 |
| P3 | completed | action | Seed this implementation plan and add a living-docs reminder hook | user request, repo customization inventory | P1 |
| P4 | planned | decision | Review the prompt pipeline TODO cluster as a separate design pass | `README.md:48-49`, prompt TODOs | Q2, Q3, Q4 |
| P5 | planned | decision | Decide the long-term role of `convert_xml_to_md.py` | `resources/convert_xml_to_md.py:1` | Q1 |
| P6 | planned | decision | Decide whether and how to promote editor v3 to the main editor path | `editor/v3/README.md:3` | Q5 |

## Next Sequence

1. Review and approve the new customization architecture and planning loop.
2. Resolve the open clarification items that block prompt-pipeline and tooling cleanup.
3. Implement one approved follow-up item at a time, updating this plan after each item.

## Item Details

### P1 - Define the customization architecture for the SDD and living-documentation loop

**Type**: decision
**Source TODOs**:

- `AGENTS.md:3` - how to keep customizations aligned
- old `.github/agents/todo-planner.md:54` - whether the workflow belongs in an agent or prompt
- `.github/skills/todo-analysis/SKILL.md:14` - whether the planning flow should be a skill

**Current understanding**:

- The repo already wanted a planning-first loop, but it was split awkwardly across a skill, a custom agent, and a workspace hook using stale assumptions.
- The current VS Code model is clearer: reusable workflow in a skill, persona and handoff in custom agents, deterministic behavior in hooks.

**Decision or change to make**:

- Keep the planning workflow in `todo-analysis`.
- Keep planning persona and handoff in `todo-planner` and `sdd-implementer`.
- Keep hooks deterministic and non-authorial.

**Docs to sync after implementation**:

- `AGENTS.md`
- `README.md`
- `docs/customization_architecture.md`

### P2 - Replace the stale planner setup with explicit planner and implementer custom agents plus planner guard rails

**Type**: action
**Source TODOs**:

- old `.github/agents/todo-planner.md:54`
- `.github/skills/todo-analysis/SKILL.md:42`

**Current understanding**:

- The previous planner setup depended on a workspace hook with Claude-style matcher assumptions.
- Current VS Code guidance favors agent-scoped hooks for behavior that should only apply to a specific custom agent.

**Decision or change to make**:

- Replace the old planner file with `.agent.md` agents.
- Move planner-only context injection and write restriction into agent-scoped hooks.

**Docs to sync after implementation**:

- `AGENTS.md`
- `docs/customization_architecture.md`

### P3 - Seed this implementation plan and add a living-docs reminder hook

**Type**: action
**Source TODOs**:

- user request for a persistent plan and post-implementation doc sync reminder

**Current understanding**:

- The repo had planner intent but no active `docs/implementation_plan.md`.
- There was a reminder for prompt/customization drift, but not for ordinary source-to-doc drift.

**Decision or change to make**:

- Create a lightweight implementation plan with a Clarification Queue.
- Add a non-blocking hook that reminds when source edits happen without nearby doc or plan updates.

**Docs to sync after implementation**:

- `AGENTS.md`
- `README.md`
- `docs/customization_architecture.md`

### P4 - Review the prompt pipeline TODO cluster as a separate design pass

**Type**: decision
**Source TODOs**:

- `README.md:48-49`
- `prompts/summarize-sources.prompt.md:27`
- `prompts/summarize-sources.prompt.md:133`
- `prompts/merge-summaries.prompt.md:23`
- `prompts/merge-summaries.prompt.md:55`
- `prompts/generate-questions.prompt.md:15`
- `prompts/generate-questions.prompt.md:198`

**Current understanding**:

- Most prompt TODOs are not implementation tasks yet. They are design questions about subject-profile scope, context boundaries, scenario generation, and interface ownership.

**Decision or change to make**:

- Resolve the open questions first, then update the prompts in one focused pass.

**Docs to sync after implementation**:

- `README.md`
- `prompts/AGENTS.md`
- `AGENTS.md`

### P5 - Decide the long-term role of `convert_xml_to_md.py`

**Type**: decision
**Source TODOs**:

- `resources/convert_xml_to_md.py:1`

**Current understanding**:

- The script exists, but its place in the workflow is not documented and may not be justified.
- This is a good test case for choosing between a plain script, a skill resource, or removal.

**Decision or change to make**:

- Confirm whether the pipeline really needs this conversion step. If yes, document where it is invoked. If no, remove or archive it.

**Docs to sync after implementation**:

- `README.md`
- `AGENTS.md`
- `resources` docs or instructions if retained

### P6 - Decide whether and how to promote editor v3 to the main editor path

**Type**: decision
**Source TODOs**:

- `editor/v3/README.md:3`

**Current understanding**:

- v3 is the maintained editor, but the current folder split still supports the repo's didactic history.

**Decision or change to make**:

- Decide whether the teaching value of the historical layout still outweighs the cost of the extra indirection.

**Docs to sync after implementation**:

- `editor/AGENTS.md`
- `editor/v3/README.md`
- `README.md`

## Recently Resolved

- 2026-04-29 - The reusable planning workflow stays in the `todo-analysis` skill, while persona, handoff, and planner-only guard rails move to custom agents.
- 2026-04-29 - `TODO:` remains the canonical inline marker; importance is decided during planning rather than encoded inline.
- 2026-04-29 - Hooks are used for deterministic reminders and constraints only, not for automatic documentation authoring.
