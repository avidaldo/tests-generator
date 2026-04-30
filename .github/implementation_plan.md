# Implementation Plan

> Updated: 2026-04-30 (refresh 17)
> Branch: decomposed
> Status: active
> Refresh 17 summary: completed P32 by adding the advanced optional batch-maintenance launcher and agent, documenting it as an unattended lane that keeps the canonical safe loop intact.

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
| Q8 | resolved | `.github/docs/customization_architecture.md` | What concrete advantage do Python hook scripts provide over equivalent behavior expressed as markdown instructions inside the agent file for deterministic tasks like context injection? | Resolved 2026-04-29: dynamic runtime data is the key reason → P18 |
| Q9 | resolved | `prompts/merge-summaries.prompt.md:55` | Can subcategory weighting be reformulated in terms of expected question yield rather than concept count? Would a separate scenario-generation agent or doc help cover concept-poor areas? | Resolved 2026-04-29: keep bundled inside P4 — scenario-generation layer is speculative until the prompt design pass |
| Q10 | resolved | `.github/instructions/customization-authoring.instructions.md:18` | Should a dedicated VS Code documentation audit skill be built that periodically fetches the official customization docs and suggests improvements to this repo's customization files? | Resolved 2026-04-29: build it → P19 |
| Q11 | resolved | `.github/agents/todo-planner.agent.md:14` | Is the explicit handoff prompt needed given that `sdd-implementer` already has instructions — would the agent instructions alone be sufficient? | Resolved 2026-04-29: keep it — handoff prompt seeds next-step context into the new chat state; complements, not replaces, target agent instructions → P21 |

## Planned Work

| ID | Status | Type | Summary | Source | Depends on |
| --- | --- | --- | --- | --- | --- |
| P31 | planned | bug | Fix `todo_planner_context.py` repo-root resolution so plan preview and marker scans use the real workspace root | `.github/hooks/src/todo_planner_context.py:17-18`, `.github/hooks/src/todo_planner_context.py:82` | none |
| P19 | planned | action | Build a `customization-audit` skill that fetches VS Code customization docs and reports gaps in this repo's customization files | `.github/instructions/customization-authoring.instructions.md:18` | none |
| P4 | planned | decision | Decide how `merge-summaries` should estimate subcategory question yield and scenario coverage | `prompts/merge-summaries.prompt.md:54` | none |
| P9 | planned | debt | Decide whether to add file-based debug logging to the context-injection hook (`todo_planner_context.py`) | `.github/hooks/src/todo_planner_context.py:123` | none |

## Next Sequence

1. P31 — fix the planner context repo-root bug so plan preview and marker counts reflect the real workspace.
2. P19 — build the `customization-audit` skill.
3. P4, P9 — the remaining design/debt items once the planner hooks are trustworthy again.

## Item Details

### P4 - Decide how `merge-summaries` should estimate subcategory question yield and scenario coverage

**Type**: decision
**Source TODOs**:

- `prompts/merge-summaries.prompt.md:54-57`

**Current understanding**:

- The only live prompt-pipeline TODO now lives in `merge-summaries.prompt.md`.
- It asks whether subcategories should be weighted by raw concept count or by expected question yield, and whether concept-poor but scenario-rich areas need a dedicated scenario-seeding input or workflow.

**Decision or change to make**:

- Decide whether to keep concept-count weighting, introduce an explicit yield heuristic, or add a separate scenario-seeding surface.
- Update `merge-summaries.prompt.md` and the user-facing workflow docs only after that choice is explicit.

**Docs to sync after implementation**:

- `README.md`
- `prompts/AGENTS.md`
- `AGENTS.md`

### P31 — Fix the `todo-planner` context hook repo-root bug

**Type**: bug
**Source observations**:

- `.github/hooks/src/todo_planner_context.py:17` — `REPO_ROOT = Path(__file__).resolve().parents[2]`
- `.github/hooks/src/todo_planner_context.py:18` — `PLAN_PATH = REPO_ROOT / ".github" / "implementation_plan.md"`
- `.github/hooks/src/todo_planner_context.py:82` — fallback `"No implementation plan exists yet..."` surfaced in this planner session despite the existing plan file.

**Current understanding**:

- `todo_planner_write_guard.py` already needed `parents[3]` to reach the repo root; `todo_planner_context.py` still uses `parents[2]`.
- That makes `PLAN_PATH` resolve to `.github/.github/implementation_plan.md`, which explains the stale planner context saying no plan exists.
- The same bug likely skews marker scans and any git-derived planner context gathered from that hook.

**Decision or change to make**:

- Align repo-root resolution with the fixed write guard.
- Revalidate the injected plan preview, marker counts, and branch detection in a planner session after the fix.

**Docs to sync after implementation**:

- none

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

- `.github/AGENTS.md`
- `AGENTS.md` (customization summary)
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

## Recently Completed

- P32 — 2026-04-30. Added `batch-maintainer` and `run-batch-maintenance.prompt.md` as an advanced optional unattended-maintenance lane; documented queue execution over approved and unblocked items, target-aware branch isolation, and the rule that unresolved decisions still stop the run instead of replacing the canonical safe loop.

- P14 — 2026-04-30. Added `.github/skills/summarize-all-sources/SKILL.md` for Stage 1 fan-out, updated the project and customization inventories, and replaced the README multi-repo TODO with the documented skill workflow.

- P30 — 2026-04-30. Fixed `.github/hooks/src/todo_planner_write_guard.py` to resolve the repository root correctly; validated that absolute `.github/implementation_plan.md` edits are allowed while unrelated files are still denied.

- P29 — 2026-04-30. Moved durable customization rationale into `.github/docs/`, removed stale root duplicate customization docs and maintenance prompts, and removed the obsolete broad `documentation-sync.instructions.md` rule.
- P28 — 2026-04-30. Split prompt surfaces by layer: maintenance prompts now live in `.github/prompts/`, while root `prompts/` is reserved for the quiz-generation pipeline.
- P27 — 2026-04-30. Moved customization docs and the active implementation plan into `.github/`, added `.github/AGENTS.md` and `.github/README.md`, and split project vs. customization documentation surfaces. Durable rationale was later subdivided into `.github/docs/` while the plan stayed at the `.github/` root.
- P26 — 2026-04-30. Inlined the planning workflow from `todo-analysis` into `todo-planner`, removed the separate planning skill, and updated the current architecture docs to match.
- P25 — 2026-04-30. Proved that direct prompt binding works cleanly when `todo-planner` and `sdd-implementer` are visible, then bound both maintenance prompts directly to those agents.
- P24 — 2026-04-29. Clarified the prompt-launcher semantics in the two SDD launcher prompts and made `implement-plan-item` explicitly single-item-only.
- P23 — 2026-04-29. Added prompt-first launcher entry points for planning and implementation, hid overlapping agent/skill UI surfaces, replaced the planner handoff with the implementation prompt, and rewrote the customization docs around the new public-vs-internal structure.
- P18 — 2026-04-29. Added hook-script-vs-markdown-instructions rationale section to the customization architecture doc; removed TODO comment. (Completed silently; plan updated retroactively in refresh 10.)
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
- P1 — 2026-04-29. Defined the initial customization architecture for the SDD loop. The first version kept workflow logic in `todo-analysis`, persona + handoff in custom agents, and deterministic behavior in hooks.
- P2 — 2026-04-29. Replaced stale planner setup with `todo-planner.agent.md` and `sdd-implementer.agent.md`; moved planner guard rails to agent-scoped hooks.
- P3 — 2026-04-29. Seeded the original implementation plan at `docs/implementation_plan.md` and added the living-docs reminder hook (`living-docs-drift-check.json`).
- P7 — 2026-04-29. Removed legacy planner surfaces; documented active hook, handoff, and terminology model in `customization_architecture.md`.

## Recently Resolved

- 2026-04-30 - The repo now has an advanced optional unattended-maintenance lane for delegated and cloud-oriented runs, but the canonical precise workflow remains `refresh-plan.prompt.md` followed by `implement-plan-item.prompt.md`. The batch lane consumes approved and unblocked items only and stops on unresolved decisions.

- 2026-04-30 - Maintenance prompts now live in `.github/prompts/`. Root `prompts/` is reserved for question-generation workflows.
- 2026-04-30 - The old root maintenance-prompt duplicates were removed. `.github/prompts/` is now the only supported maintenance-launcher surface.
- 2026-04-30 - Narrative customization docs now live under `.github/docs/`, while `.github/implementation_plan.md` remains at the `.github/` root as the active operational plan. Root `docs/` is reserved for project and domain documentation.
- 2026-04-30 - Visible direct prompt binding is the current mechanically supported architecture: `refresh-plan.prompt.md` now targets `todo-planner` directly and `implement-plan-item.prompt.md` targets `sdd-implementer` directly.
- 2026-04-30 - The SDD loop no longer uses a separate `todo-analysis` skill. The planning workflow was inlined into `todo-planner` because it had no real second consumer.
- 2026-04-30 - Visible custom agents are acceptable as advanced entry points. Prompts remain the preferred UX, but the repo no longer depends on hidden-agent prompt indirection.
- 2026-04-30 - The legacy broad `documentation-sync.instructions.md` rule was removed. The repo now uses separate project-layer and customization-layer documentation sync instructions only.
- 2026-04-30 - Superseded 2026-04-29 prompt-wrapper architecture notes were retained only as history. The current repo no longer uses hidden-agent wrapper prompts or hidden runtime launch layers for the SDD loop.
- Q11 — Resolved 2026-04-29. The explicit handoff prompt in `todo-planner.agent.md` is intentional: it seeds specific next-step context into the new chat state and complements the `sdd-implementer` instructions (does not replace them). Decision already recorded in `.github/docs/customization_architecture.md`. Cleanup: remove the stale YAML comment → P21.
- Q10 — Resolved 2026-04-29. Build the `customization-audit` skill → P19. Trigger: on-demand (VS Code major release or customization regression).
- Q9 — Resolved 2026-04-29. Yield-based weighting is speculative before a generation pass reveals whether concept-poor areas are a real problem. Bundled inside P4; scenario-generation layer becomes a new P item only if P4 confirms the gap.
- Q8 — Resolved 2026-04-29. Python hook scripts provide runtime dynamic data (git branch, live TODO count) that static markdown instructions cannot. Harder enforcement boundary is a secondary benefit. Document this in `.github/docs/customization_architecture.md` → P18.
- Q7 — Resolved 2026-04-29. Markdown links in SKILL.md only auto-load files inside the skill directory; external links (e.g. to `docs/`) are not injected. Decision: keep the link as-is for human navigation value. No action item.
- Q6 — Resolved 2026-04-29. `disable-model-invocation` is a valid SKILL.md field (controls whether manual invocation is required), but `false` is the default and its undocumented presence is noise. Remove the field and the TODO comment → P17.
- Q5 — Resolved 2026-04-29. Promote editor v3 to `editor/` root (the `v3/` label is vestigial; didactic history is in `deprecated/`). P6 is the prerequisite for P10 and P16.
- Q4 — Resolved 2026-04-29. (a) Dangling incomplete TODO at line 15 — remove it, the adversarial mechanism is already wired via mandatory `answers[].feedback` → P15. (b) JSON schema — create `docs/editor_json_schema.md` as single source of truth for the editor import contract → P16.
- Q3 — Resolved 2026-04-29. Three sub-decisions: (a) replace specific `docs/` prohibition with a general external-knowledge rule → P12; (b) show explicit `#prompt:` invocation in README Step 1 example → P13; (c) build a fan-out summarization skill → P14.
- Q2 — Resolved 2026-04-29. Language transformation belongs only at the `generate-questions` stage. Earlier stages (summarize-sources, merge-summaries) should be language-agnostic. Language default removed from `AGENTS.md`. → P11.
- Q1 — Resolved 2026-04-29. `resources/convert_xml_to_md.py` has no documented pipeline role and the `summarize-sources` prompt does not reference it. Decision: remove the script.
- 2026-04-29 - `TODO:` remains the canonical inline marker; importance is decided during planning rather than encoded inline.
- 2026-04-29 - Hooks are used for deterministic reminders and constraints only, not for automatic documentation authoring.
- 2026-04-29 - The planner handoff keeps an explicit prompt because handoff prompts seed the next-step context; they complement, not replace, the target agent instructions.
- 2026-04-29 - Planner hook scripts are agent-scoped hooks registered in `todo-planner.agent.md`; the old workspace hook JSON and shell wrappers were removed as legacy.
- 2026-04-29 - `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` remain supported as equivalent planning inputs, but `TODO:` is the only preferred new marker.
- 2026-04-29 - A periodic customization audit against current VS Code docs would be a skill rather than a prompt.

## Superseded Historical Notes

- 2026-04-29 - The first SDD-loop architecture kept the reusable planning workflow in `todo-analysis`, while persona, handoff, and planner-only guard rails moved to custom agents. This was superseded on 2026-04-30 when the planning workflow was inlined into `todo-planner`.
