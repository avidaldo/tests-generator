# Implementation Plan

> Updated: 2026-04-29 (refresh 10)
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
| P14 | planned | decision | Build a fan-out skill that spawns `summarize-sources` as one subagent per material path | `README.md:49` | none |
| P19 | planned | action | Build a `customization-audit` skill that fetches VS Code customization docs and reports gaps in this repo's customization files | `.github/instructions/customization-authoring.instructions.md:18` | none |
| P4 | planned | decision | Review the prompt pipeline TODO cluster as a separate design pass | `README.md:48-49`, prompt TODOs | none |
| P9 | planned | debt | Decide whether to add file-based debug logging to the context-injection hook (`todo_planner_context.py`) | `.github/hooks/src/todo_planner_context.py:123` | none |

## Next Sequence

1. P14, P19, P4, P9 — no urgent dependencies; P9 requires a decision before coding.
2. Continue one item at a time.

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

## Recently Completed

- P24 — 2026-04-29. Clarified the prompt-launcher semantics in the two SDD launcher prompts and made `implement-plan-item` explicitly single-item-only.
- P23 — 2026-04-29. Added prompt-first launcher entry points for planning and implementation, hid overlapping agent/skill UI surfaces, replaced the planner handoff with the implementation prompt, and rewrote the customization docs around the new public-vs-internal structure.
- P18 — 2026-04-29. Added hook-script-vs-markdown-instructions rationale section to `customization_architecture.md`; removed TODO comment. (Completed silently; plan updated retroactively in refresh 10.)
- P8 — 2026-04-29. Removed stale TODO comment from `todo-analysis/SKILL.md` Step 3; cross-cutting scan section was already present.
- P13 — 2026-04-29. Updated README Step 1 code block to show `#prompt:prompts/summarize-sources.prompt.md` invocation; removed resolved TODO comment.
- P12 — 2026-04-29. Replaced specific `docs/adversarial_logic_filters.md` prohibition in `summarize-sources` Rules with a general external-knowledge rule; removed TODO comment.
- P11 — 2026-04-29. Removed Output language row from `summarize-sources` and `merge-summaries` Subject Profiles; added note to `generate-questions` that it is the sole language-setting stage; rephrased `AGENTS.md` language convention to reflect stage-scoped language; updated `prompts/AGENTS.md` Subject Profile table.
- P16 — 2026-04-29. Created `docs/editor_json_schema.md` as the canonical schema; replaced inline field table in prompt with reference + condensed rules; updated `editor/AGENTS.md`, `prompts/AGENTS.md`, and `AGENTS.md`.
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

- 2026-04-29 - The launcher prompts still declare `agent: agent` because they run in the built-in runtime and then invoke the hidden custom agents programmatically. That wording is now explicit in the prompt bodies and architecture doc.
- 2026-04-29 - `implement-plan-item.prompt.md` is explicitly limited to exactly one approved item per run; no batch "implement all remaining work" launcher was added.
- 2026-04-29 - Public VS Code entry points for the SDD loop are prompt files only; `todo-planner`, `sdd-implementer`, and `todo-analysis` remain as hidden runtime layers behind those launchers.
- 2026-04-29 - The planner no longer surfaces an agent handoff button. In the prompt-first architecture it finishes by telling the user to run `implement-plan-item.prompt.md`, because hidden agents are not valid handoff targets in the current VS Code setup.
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
