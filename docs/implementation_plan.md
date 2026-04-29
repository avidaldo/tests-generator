# Implementation Plan

> Updated: 2026-04-29 (refresh 6)
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
| Q1 | resolved | `resources/convert_xml_to_md.py:1` | When should XML-to-Markdown conversion be part of the workflow, and should that behavior stay as a script, become a skill resource, or disappear? | Resolved 2026-04-29: remove the script |
| Q2 | resolved | `prompts/summarize-sources.prompt.md:27`, `prompts/merge-summaries.prompt.md:23`, `AGENTS.md:42` | Should language transformation happen only at question generation, with earlier stages preserving the source language? And should `AGENTS.md` even state a default output language, given that language is a per-step concern? | Resolved 2026-04-29: yes — language only at generation stage |
| Q3 | resolved | `prompts/summarize-sources.prompt.md:132-133`, `README.md:48-49` | Should summarization explicitly ban external knowledge and recommend per-material subagent fan-out for context control? | Resolved 2026-04-29: three sub-decisions, all approved — see P12, P13, P14 |
| Q4 | resolved | `prompts/generate-questions.prompt.md:15`, `prompts/generate-questions.prompt.md:198` | How should the adversarial-feedback rule be clarified, and where should the editor JSON schema live as a single source of truth? | Resolved 2026-04-29: remove dangling TODO (P15); create shared schema doc (P16) |
| Q5 | resolved | `editor/v3/README.md:3` | Should editor v3 graduate to the main `editor/` path, or is the current split still useful for the repo's didactic purpose? | Resolved 2026-04-29: yes, promote v3 to `editor/`; P6 must land before P10 and P16 |
| Q6 | resolved | `.github/skills/todo-analysis/SKILL.md:7` | What does `disable-model-invocation: false` control in VS Code skill frontmatter, and are there cases where setting it to `true` would make sense for this skill? | Resolved 2026-04-29: remove the field — it is noise in a SKILL.md context → P17 |
| Q7 | resolved | `.github/skills/todo-analysis/SKILL.md:16` | Does a Markdown link inside a SKILL.md to another doc cause that doc to be auto-loaded in context? | Resolved 2026-04-29: keep as-is — human navigation value justifies the link even without auto-loading |
| Q8 | resolved | `docs/customization_architecture.md:102` | What concrete advantage do Python hook scripts provide over equivalent behavior expressed as markdown instructions inside the agent file for deterministic tasks like context injection? | Resolved 2026-04-29: dynamic runtime data is the key reason → P18 |
| Q9 | resolved | `prompts/merge-summaries.prompt.md:55` | Can subcategory weighting be reformulated in terms of expected question yield rather than concept count? Would a separate scenario-generation agent or doc help cover concept-poor areas? | Resolved 2026-04-29: keep bundled inside P4 — scenario-generation layer is speculative until the prompt design pass |
| Q10 | resolved | `.github/instructions/customization-authoring.instructions.md:18` | Should a dedicated VS Code documentation audit skill be built that periodically fetches the official customization docs and suggests improvements to this repo's customization files? | Resolved 2026-04-29: build it → P19 |
| Q11 | resolved | `.github/agents/todo-planner.agent.md:14` | Is the explicit handoff prompt needed given that `sdd-implementer` already has instructions — would the agent instructions alone be sufficient? | Resolved 2026-04-29: keep it — handoff prompt seeds next-step context into the new chat state; complements, not replaces, target agent instructions → P21 |

## Planned Work

| ID | Status | Type | Summary | Source | Depends on |
| --- | --- | --- | --- | --- | --- |
| P11 | planned | action | Remove language column from `summarize-sources` and `merge-summaries` Subject Profiles; remove/rephrase language default from `AGENTS.md` | Q2 resolution | none |
| P12 | planned | action | Replace specific `docs/` prohibition in `summarize-sources` with a general external-knowledge rule | `prompts/summarize-sources.prompt.md:132` | none |
| P13 | planned | action | Update README Step 1 example to show explicit `#prompt:` invocation before materials list | `README.md:48` | none |
| P14 | planned | decision | Build a fan-out skill that spawns `summarize-sources` as one subagent per material path | `README.md:49` | none |
| P16 | planned | action | Create `docs/editor_json_schema.md` as the canonical schema; update prompt output block and editor AGENTS.md to reference it | `prompts/generate-questions.prompt.md:198` | none |
| P18 | planned | debt | Document why hook scripts are used over markdown instructions in `customization_architecture.md`; remove the TODO | `docs/customization_architecture.md:102` | none |
| P19 | planned | action | Build a `customization-audit` skill that fetches VS Code customization docs and reports gaps in this repo's customization files | `.github/instructions/customization-authoring.instructions.md:18` | none |
| P4 | planned | decision | Review the prompt pipeline TODO cluster as a separate design pass | `README.md:48-49`, prompt TODOs | none |
| P8 | planned | debt | Improve the `todo-analysis` SKILL.md enrichment step to explicitly encourage broader architecture analysis | `.github/skills/todo-analysis/SKILL.md:46` | none |
| P9 | planned | debt | Decide whether to add file-based debug logging to the context-injection hook (`todo_planner_context.py`) | `.github/hooks/src/todo_planner_context.py:123` | none |
| P10 | planned | action | Implement difficulty sub-categorization for editor export ("Lista pero fácil") | `editor/README.md` | none |

## Next Sequence

1. P16 — Create `docs/editor_json_schema.md` (unblocked now that P6 is done).
2. P10 — Implement difficulty sub-categorization for editor export (also unblocked by P6).
3. P11, P12, P13 — prompt-stage cleanups (no dependencies).
4. Continue one item at a time.


## Item Details

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

### P19 — Build a `customization-audit` skill

**Type**: action
**Source TODOs**:

- `.github/instructions/customization-authoring.instructions.md:18`

**Current understanding**:

- The VS Code customization surface evolves; the repo's customization files were last reviewed 2026-04-22. Without a periodic check, outdated patterns (like `infer` → `user-invocable`) accumulate silently.
- The skill would fetch the VS Code customization docs overview and key primitive pages using `#tool:web/fetch`, then compare against this repo's live customization files and report gaps or deprecated patterns.

**Decision or change to make**:

- Create `.github/skills/customization-audit/SKILL.md`.
- Define the skill workflow: (1) fetch `https://code.visualstudio.com/docs/copilot/customization/overview` and linked primitive pages; (2) read all customization files in `.github/`; (3) report: deprecated fields in use, missing recommended fields, new primitives not yet adopted.
- Update `AGENTS.md` skills inventory.

**Docs to sync after implementation**:

- `AGENTS.md` (skills inventory)
- `.github/instructions/customization-authoring.instructions.md` (remove the TODO)

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

### P18 — Document hook scripts vs. markdown instructions rationale in `customization_architecture.md`

**Type**: debt
**Source TODOs**:

- `docs/customization_architecture.md:102` — `<!-- TODO: why scripts in hooks are useful instead of just using markdown instructions directly in the agent? -->`

**Current understanding**:

- The architecture doc explains that hooks are used for deterministic reminders and constraints, but does not explain *why* a Python script is preferred over an equivalent markdown instruction.
- The answer: Python scripts can inject **runtime dynamic data** (current git branch, live TODO marker count) that static markdown cannot. This is the primary reason the context-injection hook is a script.
- A secondary reason: hooks provide a harder enforcement boundary (the runtime enforces the hook regardless of what the agent instruction says).
- For purely static rules, markdown instructions would be simpler and equally effective.

**Decision or change to make**:

- Add a short explanation to `customization_architecture.md` near line 102 covering: (a) dynamic data injection as the primary reason, (b) harder enforcement as secondary, (c) when markdown instructions are preferable instead.
- Remove the TODO comment.

**Docs to sync after implementation**:

- none (self-contained doc change)

### P9 — Decide whether to add file-based debug logging to `todo_planner_context.py`

**Type**: debt
**Source TODOs**:

- `.github/hooks/src/todo_planner_context.py:123` — `# TODO: for a better understanding of the hook, could we log the context in a file for debugging purposes?`

**Current understanding**:

- The comment is a complete question at the end of `main()`, not a dangling note. It asks whether context output (the JSON the hook sends to the agent runtime) should also be logged to a file to make hook behavior easier to debug.
- The hook currently prints JSON to stdout. A parallel debug log file would help when the runtime context is opaque.

**Decision or change to make**:

- Decide whether debug logging adds enough value given how rarely hook behavior needs inspection. If yes, implement optional logging (e.g., controlled by an env var or `--debug` flag). If no, remove the TODO and note why.

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

- `editor/README.md`
- `editor/AGENTS.md`
- `editor/SPECS_v3.md`

### P11 — Remove language setting from early prompt stages

**Type**: action
**Source TODOs**:

- `prompts/summarize-sources.prompt.md:27`
- `prompts/merge-summaries.prompt.md:23`
- `AGENTS.md:42`

**Current understanding**:

- All three prompt stages declare a Spanish output language in the Subject Profile. This locks intermediate artifacts to one language and forces full re-runs if the output language changes.
- `AGENTS.md` states a default output language at repo level, which is inconsistent with language being a per-invocation concern.

**Decision or change to make**:

- Remove the output language row from the Subject Profile tables in `summarize-sources.prompt.md` and `merge-summaries.prompt.md`.
- Update the language row in `generate-questions.prompt.md` to make explicit that it is the sole stage where output language is set.
- Remove or rephrase the language default from `AGENTS.md` (line 42 area).

**Docs to sync after implementation**:

- `AGENTS.md`
- `prompts/AGENTS.md`
- `README.md` (if it references language defaults)

### P12 — Replace specific `docs/` prohibition with a general external-knowledge rule

**Type**: action
**Source TODOs**:

- `prompts/summarize-sources.prompt.md:132-133`

**Current understanding**:

- The prompt currently has a specific rule: *"Do not reference or read `docs/adversarial_logic_filters.md` or `docs/distractor_design.md`."* Those files are auto-injected only via `question-design.instructions.md` which has `applyTo: prompts/generate-questions.prompt.md` — so they are not a real risk here.
- The actual risk is the agent using training knowledge or other workspace content not in the provided source files.
- The specific prohibition is misleading (implies only those two files are the risk) and doesn't cover the real concern.

**Decision or change to make**:

- Remove the specific prohibition line.
- Add a general rule: *"Use only the information present in the source materials provided by the user. Do not introduce external knowledge, assumptions, or information not found in those files."*

**Docs to sync after implementation**:

- none (self-contained prompt change)

### P13 — Update README Step 1 example to show explicit prompt invocation

**Type**: action
**Source TODOs**:

- `README.md:48`

**Current understanding**:

- The README Step 1 shows a materials list example inside a code block, but does not show how to invoke the prompt. A new user would not know to attach `#prompt:prompts/summarize-sources.prompt.md` before listing paths.

**Decision or change to make**:

- Update the code block to show the full invocation:
  ```
  #prompt:prompts/summarize-sources.prompt.md

  Summarise the following course materials:
  - /path/to/ml-course/notebooks/01-preprocessing/
  ```

**Docs to sync after implementation**:

- none (self-contained README change)

### P14 — Build a fan-out summarization skill

**Type**: decision
**Source TODOs**:

- `README.md:49`

**Current understanding**:

- Current workflow requires the user to manually run `summarize-sources` once per repo/topic in separate sessions. For large subjects with many repos, this is friction-heavy and sequential.
- A fan-out skill would accept a list of material paths, spawn `summarize-sources` as a subagent per path (parallelized, context-isolated), and return N summary files.
- The primitive choice is a **skill** (not a custom agent) because it is a reusable, parameterized multi-step workflow rather than a persona with guard rails.

**Decision or change to make**:

- Create `.github/skills/summarize-all-sources/SKILL.md`.
- Define the skill interface: takes a list of source paths and an optional shared Subject Profile; fans out one `summarize-sources` subagent per path; collects outputs.
- Update `README.md` Step 1 to mention the fan-out skill as the preferred option for multi-repo subjects.
- Update `prompts/AGENTS.md` pipeline diagram to reflect the optional fan-out.

**Docs to sync after implementation**:

- `README.md`
- `prompts/AGENTS.md`
- `AGENTS.md` (skill inventory)

### P16 — Create `docs/editor_json_schema.md` as the canonical editor JSON schema

**Type**: action
**Source TODOs**:

- `prompts/generate-questions.prompt.md:198`

**Current understanding**:

- The JSON output schema is currently defined inline in the prompt. The editor (`state_io.py`, `xml_parser.py`) independently implements the same schema with no shared canonical reference. Any change to the schema requires manually updating both sides.

**Decision or change to make**:

- Create `docs/editor_json_schema.md` containing the full schema definition with field descriptions and examples.
- Replace the inline schema block in the prompt with a brief reference: *"Output must conform to the editor JSON schema — see `docs/editor_json_schema.md`."* and a minimal structural example (not the full field table).
- Add a reference to the schema doc in `editor/AGENTS.md` as the import contract.

**Docs to sync after implementation**:

- `editor/AGENTS.md`
- `prompts/AGENTS.md` (pipeline interface section)
- `AGENTS.md` (docs table)

### Q10 — Should a periodic VS Code documentation audit skill be built?

**Source**: `.github/instructions/customization-authoring.instructions.md:18`

**Question**: Is a VS Code customization audit skill — one that fetches the current VS Code customization docs and analyzes this repo's customization files for gaps or outdated patterns — worth building?

**Context**: The TODO compares this to the built-in `/init` command but web-aware and repo-aware. The "skill vs prompt" decision was already resolved on 2026-04-29 in favor of skill. What remains open is whether to actually implement it, and if so: what docs URL(s) it would fetch, how it would compare fetched docs against this repo's customization files, and how output would be actionable.

**Options**:

- **Yes, build it**: The VS Code customization surface evolves; periodic checks would catch deprecated patterns and new primitives. The skill would use `#tool:web/fetch` to pull the overview and each primitive's doc page, then compare against the live customization files.
- **No, skip it**: The customization architecture is well-documented and already reviewed on 2026-04-22. Re-reading docs on demand when something breaks is lower cost than maintaining an audit skill.
- **Deferred**: Note the idea but do not plan it now; revisit when VS Code releases a major customization update.

**Next step**: Decide whether to plan, defer, or close the idea.

## Recently Completed

- P15 — 2026-04-29. Removed dangling incomplete TODO from `generate-questions.prompt.md`.
- P17 — 2026-04-29. Removed `disable-model-invocation: false` noise from `todo-analysis` SKILL.md frontmatter.
- P20 — 2026-04-29. Deleted `resources/convert_xml_to_md.py` (decision made in P5; file finally removed).
- P21 — 2026-04-29. Removed stale inline YAML comment from `todo-planner.agent.md` handoff prompt.
- P22 — 2026-04-29. Removed stale Q7-resolved TODO comment from `todo-analysis/SKILL.md`.

- P6 — 2026-04-29. Promoted `editor/v3/` to `editor/`; moved all source files, created `editor/README.md`, updated all run-command references across docs, instructions, and skill files.

- P5 — 2026-04-29. Decided to remove `resources/convert_xml_to_md.py` (unused, no pipeline role). **Note**: actual file deletion not done; tracked as P20.
- P1 — 2026-04-29. Defined the customization architecture for the SDD loop. Decided: workflow in `todo-analysis` skill, persona + handoff in custom agents, deterministic behavior in hooks.
- P2 — 2026-04-29. Replaced stale planner setup with `todo-planner.agent.md` and `sdd-implementer.agent.md`; moved planner guard rails to agent-scoped hooks.
- P3 — 2026-04-29. Seeded `docs/implementation_plan.md` and added living-docs reminder hook (`living-docs-drift-check.json`).
- P7 — 2026-04-29. Removed legacy planner surfaces; documented active hook, handoff, and terminology model in `customization_architecture.md`.

## Recently Resolved

- Q11 — Resolved 2026-04-29. The explicit handoff prompt in `todo-planner.agent.md` is intentional: it seeds specific next-step context into the new chat state and complements the `sdd-implementer` instructions (does not replace them). Decision already recorded in `customization_architecture.md`. Cleanup: remove the stale YAML comment → P21.
- Q10 — Resolved 2026-04-29. Build the `customization-audit` skill → P19. Trigger: on-demand (VS Code major release or customization regression).
- Q9 — Resolved 2026-04-29. Yield-based weighting is speculative before a generation pass reveals whether concept-poor areas are a real problem. Bundled inside P4; scenario-generation layer becomes a new P item only if P4 confirms the gap.
- Q8 — Resolved 2026-04-29. Python hook scripts provide runtime dynamic data (git branch, live TODO count) that static markdown instructions cannot. Harder enforcement boundary is a secondary benefit. Document this in `customization_architecture.md` → P18.
- Q7 — Resolved 2026-04-29. Markdown links in SKILL.md only auto-load files inside the skill directory; external links (e.g. to `docs/`) are not injected. Decision: keep the link as-is for human navigation value. No action item.
- Q6 — Resolved 2026-04-29. `disable-model-invocation` is a valid SKILL.md field (controls whether manual invocation is required), but `false` is the default and its undocumented presence is noise. Remove the field and the TODO comment → P17.
- Q5 — Resolved 2026-04-29. Promote editor v3 to `editor/` root (the `v3/` label is vestigial; didactic history is in `deprecated/`). P6 is the prerequisite for P10 and P16.
- Q4 — Resolved 2026-04-29. (a) Dangling incomplete TODO at line 15 — remove it, the adversarial mechanism is already wired via mandatory `answers[].feedback` → P15. (b) JSON schema — create `docs/editor_json_schema.md` as single source of truth for the editor import contract → P16.
- Q3 — Resolved 2026-04-29. Three sub-decisions: (a) replace specific `docs/` prohibition with a general external-knowledge rule → P12; (b) show explicit `#prompt:` invocation in README Step 1 example → P13; (c) build a fan-out summarization skill → P14.
- Q2 — Resolved 2026-04-29. Language transformation belongs only at the `generate-questions` stage. Earlier stages (summarize-sources, merge-summaries) should be language-agnostic. Language default removed from `AGENTS.md`. → P11.
- Q1 — Resolved 2026-04-29. `resources/convert_xml_to_md.py` has no documented pipeline role and the `summarize-sources` prompt does not reference it. Decision: remove the script.
- 2026-04-29 - The reusable planning workflow stays in the `todo-analysis` skill, while persona, handoff, and planner-only guard rails move to custom agents.
- 2026-04-29 - `TODO:` remains the canonical inline marker; importance is decided during planning rather than encoded inline.
- 2026-04-29 - Hooks are used for deterministic reminders and constraints only, not for automatic documentation authoring.
- 2026-04-29 - The planner handoff keeps an explicit prompt because handoff prompts seed the next-step context; they complement, not replace, the target agent instructions.
- 2026-04-29 - Planner hook scripts are agent-scoped hooks registered in `todo-planner.agent.md`; the old workspace hook JSON and shell wrappers were removed as legacy.
- 2026-04-29 - `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` remain supported as equivalent planning inputs, but `TODO:` is the only preferred new marker.
- 2026-04-29 - A periodic customization audit against current VS Code docs would be a skill rather than a prompt.
