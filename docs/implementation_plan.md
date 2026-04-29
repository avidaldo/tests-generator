# Implementation Plan

> Updated: 2026-04-29 (refresh)
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
| Q2 | open | `prompts/summarize-sources.prompt.md:27`, `prompts/merge-summaries.prompt.md:23`, `AGENTS.md:42` | Should language transformation happen only at question generation, with earlier stages preserving the source language? And should `AGENTS.md` even state a default output language, given that language is a per-step concern? | Review the Subject Profile flow across all three prompt stages and decide the single consistent model |
| Q3 | open | `prompts/summarize-sources.prompt.md:133`, `README.md:48-49` | Should summarization explicitly ban external knowledge and recommend per-material subagent fan-out for context control? | Review the current prompt wording and the actual capabilities of the target agents before editing the prompts |
| Q4 | open | `prompts/generate-questions.prompt.md:15`, `prompts/generate-questions.prompt.md:198` | How should the adversarial-feedback rule be clarified, and where should the editor JSON schema live as a single source of truth? | Compare the prompt output block with the editor state schema and decide whether a shared schema doc is needed |
| Q5 | open | `editor/v3/README.md:3` | Should editor v3 graduate to the main `editor/` path, or is the current split still useful for the repo's didactic purpose? | Review migration cost, import paths, and the documentation impact before moving files |
| Q6 | open | `.github/skills/todo-analysis/SKILL.md:7` | What does `disable-model-invocation: false` control in VS Code skill frontmatter, and are there cases where setting it to `true` would make sense for this skill? | Check VS Code skill frontmatter docs; determine whether this field needs a documented value rationale or can be removed |
| Q7 | open | `.github/skills/todo-analysis/SKILL.md:16` | Does a Markdown link inside a SKILL.md to another doc cause that doc to be auto-loaded in context (as `chat.includeReferencedInstructions` does for instruction files)? | Verify in VS Code docs or empirically; if the link has no effect, remove or replace it with a plain reference note |
| Q8 | open | `docs/customization_architecture.md:102` | What concrete advantage do Python hook scripts provide over equivalent behavior expressed as markdown instructions inside the agent file for deterministic tasks like context injection? | Read the hook script runtime contract; assess whether dynamic data (git branch, marker counts) is the key reason, and document the answer inline in `customization_architecture.md` |
| Q9 | open | `prompts/merge-summaries.prompt.md:55` | Can subcategory weighting be reformulated in terms of expected question yield rather than concept count? Would a separate scenario-generation agent or doc help cover concept-poor areas? | Review the merge-summaries weighting logic as part of the P4 prompt design pass |

## Planned Work

| ID | Status | Type | Summary | Source | Depends on |
| --- | --- | --- | --- | --- | --- |
| P1 | completed | decision | Define the customization architecture for the SDD and living-documentation loop | `AGENTS.md:3`, old planner TODOs | none |
| P2 | completed | action | Replace the stale planner setup with explicit planner and implementer custom agents plus planner guard rails | old `.github/agents/todo-planner.md`, `.github/skills/todo-analysis/SKILL.md` | P1 |
| P3 | completed | action | Seed this implementation plan and add a living-docs reminder hook | user request, repo customization inventory | P1 |
| P7 | completed | action | Remove leftover legacy planner surfaces and document the active hook, handoff, and terminology model | user follow-up audit, customization TODOs | P2 |
| P4 | planned | decision | Review the prompt pipeline TODO cluster as a separate design pass | `README.md:48-49`, prompt TODOs | Q2, Q3, Q4, Q9 |
| P5 | planned | decision | Decide the long-term role of `convert_xml_to_md.py` | `resources/convert_xml_to_md.py:1` | Q1 |
| P6 | planned | decision | Decide whether and how to promote editor v3 to the main editor path | `editor/v3/README.md:3` | Q5 |
| P8 | planned | debt | Improve the `todo-analysis` SKILL.md enrichment step to explicitly encourage broader architecture analysis | `.github/skills/todo-analysis/SKILL.md:46` | none |
| P9 | planned | bug | Complete or remove the dangling incomplete TODO comment in `todo_planner_context.py:123` | `.github/hooks/src/todo_planner_context.py:123` | none |
| P10 | planned | action | Implement difficulty sub-categorization for the editor ("Lista pero fácil" export filter) | `editor/v3/README.md:33-34` | Q5 |

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
- `AGENTS.md:42`

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

### Q6 — `disable-model-invocation` frontmatter field semantics

**Source**: `.github/skills/todo-analysis/SKILL.md:7`

**Question**: What does `disable-model-invocation: false` control, and are there cases where `true` is appropriate for this skill?

**Context**: The field is present in the skill frontmatter but undocumented locally. VS Code skills can run in tool-only mode (no LLM call) or with model inference. For a planning skill that writes a file, the model must be invoked. The field value is therefore correct, but its presence without documentation creates confusion about intent.

**Next step**: Verify the field's semantics in VS Code docs. If `false` is always the default, remove it as noise. If the field is meaningful, add a comment explaining why it is set to `false`.

### Q7 — Does a Markdown link in SKILL.md auto-load the linked doc?

**Source**: `.github/skills/todo-analysis/SKILL.md:16`

**Question**: Does `chat.includeReferencedInstructions` apply to SKILL.md files, or only to `.instructions.md` and AGENTS.md? If not, the Markdown link to `customization_architecture.md` provides no automatic context injection and may be misleading.

**Context**: AGENTS.md and `.instructions.md` files support referenced instruction loading. It is unclear whether SKILL.md files have the same behavior. The doc reference in the skill header is intended to explain rationale, but if it does not inject context, it adds reader confusion rather than value.

**Next step**: Check VS Code skill docs or test empirically. If the link has no injection effect, replace it with a plain text note or remove it.

### Q8 — Why Python hook scripts over markdown instructions for context injection

**Source**: `docs/customization_architecture.md:102`

**Question**: What specific advantage do Python hook scripts provide over equivalent markdown instructions inside the agent file for the planner context-injection task?

**Context**: The planner guard rails (context injection, write restriction) are implemented as Python scripts (`todo_planner_context.py`, `todo_planner_write_guard.py`) rather than as markdown instructions inside `todo-planner.agent.md`. The architecture doc explains that this is the design, but does not explain why the dynamic capabilities of a script are needed. The context injection script injects git branch and marker counts dynamically — that is the key capability plain markdown cannot provide.

**Next step**: Confirm this is the full reason (runtime dynamic data), document it in `customization_architecture.md`, and close the TODO.

### Q9 — Subcategory weighting by question yield in merge-summaries

**Source**: `prompts/merge-summaries.prompt.md:55`

**Question**: Can the subcategory-proposal step in merge-summaries be reformulated around expected question yield rather than concept count? Would a scenario-generation agent or curated scenario doc help fill concept-poor areas?

**Context**: The current prompt asks agents to weight subcategories by approximate concept count. The TODO notes that some concepts naturally yield more questions than others (due to relationships and subcases), making concept count a weak proxy. The question also raises whether a scenario-generation layer (new agent or manual doc) could compensate.

**Next step**: Address during the P4 prompt design pass. Decide whether yield-based weighting is feasible at the merge stage, and whether the scenario-generation idea becomes a separate P11.

### P8 — Improve `todo-analysis` SKILL.md enrichment step for architecture analysis

**Type**: debt
**Source TODOs**:

- `.github/skills/todo-analysis/SKILL.md:46` — "Plenty of TODOs are going to be architecture or design questions / change proposals, so a broader analysis will be important."

**Current understanding**:

- Step 3 ("Enrich locally") instructs the agent to read the surrounding scope and nearest relevant docs per marker. It does not call for a wider architectural assessment across modules.
- For a codebase where most TODOs are design or architecture questions (rather than simple bug fixes), this narrow per-marker enrichment may miss cross-cutting concerns.

**Decision or change to make**:

- Add an explicit architecture-scan pass to Step 3: after per-marker enrichment, scan for cross-cutting impacts, module-boundary questions, and recurring themes before classifying.

**Docs to sync after implementation**:

- `.github/skills/todo-analysis/SKILL.md`

### P9 — Remove dangling incomplete TODO in `todo_planner_context.py`

**Type**: bug
**Source TODOs**:

- `.github/hooks/src/todo_planner_context.py:123` — `# TODO: for a better understanding of` (text cut off, no actionable content)

**Current understanding**:

- This comment is an incomplete capture at the end of the `main()` function in the context-injection hook. It does not describe an action or a question. It likely started as a note that was never finished.

**Decision or change to make**:

- Remove the dangling comment, or complete it with the intended thought before the next merge.

**Docs to sync after implementation**:

- none

### P10 — Implement difficulty sub-categorization for editor export ("Lista pero fácil")

**Type**: action
**Source TODOs**:

- `editor/v3/README.md:33-34` — informal `todo:` listing "Exportar solo las 'Listas'" (already implemented) and "'Lista pero fácil'" (not implemented)

**Current understanding**:

- The editor currently has three question statuses: `PENDIENTE`, `REVISAR`, `LISTA`. Export already filters to `LISTA` only.
- "Lista pero fácil" implies a secondary attribute — either a difficulty level field, a tag/label, or a sub-status. The current `Question` model has no difficulty field.
- This is a new feature request for the editor data model and export logic.

**Decision or change to make**:

- Resolve Q5 first (v3 path migration) to avoid implementing against a path that will change.
- Then decide where difficulty lives: a new `difficulty: Enum` field on `Question`, a free-text tag, or a separate status value (e.g., `LISTA_FACIL`).
- Update the data model, the UI, and the XML writer accordingly.

**Docs to sync after implementation**:

- `editor/v3/README.md`
- `editor/AGENTS.md`
- `editor/SPECS_v3.md`

## Recently Resolved

- 2026-04-29 - The reusable planning workflow stays in the `todo-analysis` skill, while persona, handoff, and planner-only guard rails move to custom agents.
- 2026-04-29 - `TODO:` remains the canonical inline marker; importance is decided during planning rather than encoded inline.
- 2026-04-29 - Hooks are used for deterministic reminders and constraints only, not for automatic documentation authoring.
- 2026-04-29 - The planner handoff keeps an explicit prompt because handoff prompts seed the next-step context; they complement, not replace, the target agent instructions.
- 2026-04-29 - Planner hook scripts are agent-scoped hooks registered in `todo-planner.agent.md`; the old workspace hook JSON and shell wrappers were removed as legacy.
- 2026-04-29 - `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` remain supported as equivalent planning inputs, but `TODO:` is the only preferred new marker.
- 2026-04-29 - A periodic customization audit against current VS Code docs would be a skill rather than a prompt.
