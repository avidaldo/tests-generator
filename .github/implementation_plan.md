# Implementation Plan

> Updated: 2026-05-19 (local sync)
> Branch: decomposed
> Status: active
> Local sync 2026-05-19: added an advanced Stage 3 exhaustive-coverage skill for approved Stage 2 scopes, clarified the distinction from the one-wave breadth-first Stage 3 skill, and synced the project docs, customization inventories, and durable customization rationale.

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
| Q9 | resolved | `prompts/merge-summaries.prompt.md:55` | Can subcategory weighting be reformulated in terms of expected question yield rather than concept count? Would a separate scenario-generation agent or doc help cover concept-poor areas? | Resolved 2026-04-29: keep bundled inside P4. Final outcome 2026-05-03: use explicit question surfaces as the yield heuristic inside merge; no separate scenario-generation layer for now. |
| Q10 | resolved | `.github/instructions/customization-authoring.instructions.md:18` | Should a dedicated VS Code documentation audit skill be built that periodically fetches the official customization docs and suggests improvements to this repo's customization files? | Resolved 2026-04-29: build it → P19 |
| Q11 | resolved | `.github/agents/todo-planner.agent.md:14` | Is the explicit handoff prompt needed given that `sdd-implementer` already has instructions — would the agent instructions alone be sufficient? | Resolved 2026-04-29: keep it — handoff prompt seeds next-step context into the new chat state; complements, not replaces, target agent instructions → P21 |
| Q12 | resolved | `prompts/AGENTS.md`, `.github/skills/summarize-all-sources/SKILL.md`, `.github/prompts/run-batch-maintenance.prompt.md` | Should bulk orchestration become prompt-invocable for both Stage 1 and Stage 3, or only for Stage 3? | Resolved 2026-05-04: keep Stage 1 bulk on the existing `summarize-all-sources` skill and document it clearly; add an optional Stage 3 single-call bulk lane for delegated/background runs while keeping the single-unit prompts as the normal workflow. |
| Q13 | resolved | `prompts/summarize-sources.prompt.md`, `prompts/merge-summaries.prompt.md`, `prompts/generate-questions.prompt.md` | Should quiz-pipeline inputs and outputs continue defaulting to repo-owned `stage*` folders, or should each run use user-provided paths instead? | Resolved 2026-05-04: stop assuming repo-owned artifact roots; ask for the relevant input/output path or root when missing, then derive deterministic filenames under that user-provided root. |
| Q14 | resolved | `prompts/generate-questions.prompt.md:25` | Should Stage 3 keep `Question focus` as a local override/fallback, or rely entirely on the Stage 2 subcategory header? | Resolved 2026-05-04: remove the Stage 3 override and treat the Stage 2 subcategory header as the single source of truth. |

## Planned Work

- No approved unblocked items remain.

## Next Sequence

1. Refresh the plan when new approved work appears.

## Item Details

### P40 — Direct Stage 3 Concept Stems

- Scope: tighten `prompts/generate-questions.prompt.md` so concept, taxonomy, and hierarchy questions are asked directly by default instead of being wrapped in decorative classroom, debate, or named-speaker narration.
- Prompt changes: distinguish essential scenario context from decorative narrative framing; add positive and negative examples; and replace the broad instruction to "Design scenarios" with a direct-by-default rule for definitions, distinctions, and hierarchy questions.
- Guardrail: if removing the narrative wrapper leaves the tested concept, answer logic, and difficulty unchanged, the wrapper is decorative and should be removed.
- Keep: legitimate use cases, decision contexts, diagnostic situations, and procedural scenarios where the concrete facts materially change the answer.
- Exclude: retroactive cleanup or regeneration of existing Stage 3 JSON batches; this item changes future generation behavior only.
- Sync: update `prompts/AGENTS.md` with a concise Stage 3 guardrail so the canonical pipeline summary matches the prompt behavior.
- Validation: run a focused Stage 3 check against the AI Foundations and Learning Paradigms subcategory and verify that direct concept questions no longer use wrappers such as "En un debate de clase, alguien afirma" while real application scenarios remain available.

### P38 — Stage 3 Bulk Generation Lane

- Scope: replace the old dual thin-launcher plan with the actual bulk-execution architecture. Stage 1 keeps the existing `summarize-all-sources` skill as its orchestration surface; Stage 3 gains the missing single-call bulk lane.
- Stage 1: do not add a duplicate public prompt launcher. Treat `summarize-all-sources` as the supported Stage 1 bulk entry point and improve discoverability only through the canonical docs and inventories.
- Stage 3: add an optional bulk launcher over a new Stage 3 helper that can traverse multiple subcategories from one invocation, write artifacts under the existing user-provided Stage 3 root contract, and support long delegated/background runs with explicit checkpoints or resumable progress.
- Guardrails: preserve the existing per-subcategory `generate-questions.prompt.md` flow as the normal precise workflow. The bulk lane is advanced and opt-in. It must stop cleanly on validation failures, keep partial progress inspectable, and avoid hiding where human review is still advisable.
- Dependency: P37 first, so the Stage 3 bulk lane uses the new path contract instead of any repo-owned artifact root assumptions.

### P39 — Detailed Workflow Documentation

- Scope: add a durable project-facing workflow doc under `docs/`, keep `README.md` concise, and sync `AGENTS.md` plus `prompts/AGENTS.md` to the same execution model.
- Content: document regular vs bulk execution, recommended usage criteria, Stage 1 bulk via the existing `summarize-all-sources` skill, the new delegated Stage 3 bulk lane, the user-provided path contract, and the decision to keep prompts as the primary precise UX while exposing orchestration only where it materially improves unattended execution.
- Dependency: depends on P37 and P38 so the doc reflects the final implemented workflow rather than an intermediate state.

## Recently Completed

- P46 — 2026-05-20. Added focused editor regression tests under `editor/tests/`: `test_state_io.py` covers the strict Stage 3 batch versus Stage 4 review-session JSON contract plus legacy editor-state compatibility, and `test_main_window_session_flow.py` covers dirty-state prompt gating and autosave-restore dirty tracking under offscreen Qt; validated the new tests individually and then with the existing `test_question_diagnostics.py` in one focused editor test run.

- P45 — 2026-05-20. Clarified the additive Stage 3 and legacy XML flows in the editor UI by renaming the submenu path to `Archivo -> Añadir -> ...`, updating the relevant dialog titles, toolbar labels, and import status messages in `editor/views/main_window.py`, and syncing the same terminology across `editor/README.md`, `editor/docs/WORKFLOW.md`, `editor/docs/IMPORT_EXPORT.md`, `README.md`, and `docs/editor_json_schema.md`; validation confirmed the touched Python files still compile and no stale `Archivo -> Importar ->` references remain in the synced workflow docs.

- P44 — 2026-05-19. Added explicit dirty-state tracking to `editor/views/main_window.py` so `Nueva sesión`, `Abrir sesión de revisión...`, and window close now prompt only when unsaved changes exist rather than whenever questions are merely loaded; kept autosave recovery dirty on restore; cleared stale autosaves on save, clean replacement, and discard; synced `editor/README.md`, `editor/docs/WORKFLOW.md`, `editor/docs/IMPORT_EXPORT.md`, and `editor/AGENTS.md`; and validated the behavior with an offscreen Qt runtime check plus a final stale-wording scan and error check.

- P43 — 2026-05-19. Simplified the editor session/import/export workflow around a strict Stage 3 vs Stage 4 distinction: added explicit JSON artifact validation in `editor/file_io/state_io.py`, separated Stage 3 batch import from review-session open in `editor/views/main_window.py`, added a shared Save/Discard/Cancel replacement flow plus `Guardar sesión` vs `Guardar sesión como...`, regrouped the File menu around session/import/export responsibilities, demoted legacy XML import to a secondary path, kept easy-only XML export as a secondary export action, replaced the stale `editor/SPECS_v3.md` surface with stronger editor docs under `editor/docs/`, synced `editor/AGENTS.md`, `docs/editor_json_schema.md`, and `README.md`, and validated the result with `py_compile`, `compileall`, and a targeted runtime contract check for the JSON loaders.

- P42 — 2026-05-19. Added `.github/skills/finish-question-coverage/SKILL.md` as an advanced Stage 3 exhaustive-coverage lane for approved Stage 2 scopes; kept it distinct from the existing one-wave breadth-first `generate-question-batches` skill; synced `.github/AGENTS.md`, `.github/README.md`, `.github/docs/customization_architecture.md`, `.github/docs/README.md`, `AGENTS.md`, `docs/pipeline_execution_modes.md`, `prompts/AGENTS.md`, `README.md`, and the existing Stage 3 bulk skill docs; and validated the new skill frontmatter plus required section structure plus the final markdown/doc cleanup.

- P41 — 2026-05-05. Started the Stage 4 review-session architecture: added `editor/models/review_session.py`, changed `editor/file_io/state_io.py` to persist a dedicated review-session JSON envelope while staying backward-compatible with old JSON and raw Stage 3 batch imports, made Stage 3 batch JSON the primary `Ctrl+O` editor import path, added recursive Stage 3 folder import over deterministic `batch-*.json` discovery, added provenance display plus stable duplicate suppression, aligned penalty defaults with the documented `0.0000000` contract, and synced the schema plus the core editor/project workflow docs.

- P39 — 2026-05-04. Added `docs/pipeline_execution_modes.md` as the durable project-facing guide for regular versus bulk execution, the Stage 1 and Stage 3 bulk lanes, and the user-owned artifact path contract; kept `README.md` concise by linking to that detail instead of duplicating it; synced `AGENTS.md` and `prompts/AGENTS.md`; and validated both the content coverage and final markdown lint state.

- P38 — 2026-05-04. Added `.github/skills/generate-question-batches/SKILL.md` as the Stage 3 bulk lane for delegated and background breadth-first runs, kept Stage 1 bulk on `summarize-all-sources`, synced `.github/AGENTS.md`, `.github/README.md`, `AGENTS.md`, and `prompts/AGENTS.md`, and validated the new lane against the approved P38 acceptance criteria.

- P40 — 2026-05-04. Tightened `prompts/generate-questions.prompt.md` so Stage 3 asks concept, taxonomy, hierarchy, and misconception-correction questions directly by default; added explicit positive and negative examples distinguishing legitimate scenarios from decorative wrappers; added a final directness self-check; synced `prompts/AGENTS.md`; and validated the new behavior against the AI Foundations and Learning Paradigms subcategory.

- P37 — 2026-05-04. Replaced the repo-owned Stage 1-3 artifact-path contract with a user-provided path/root contract across `prompts/summarize-sources.prompt.md`, `prompts/merge-summaries.prompt.md`, `prompts/generate-questions.prompt.md`, `prompts/AGENTS.md`, `README.md`, and `AGENTS.md`; removed the stale Stage 3 `Question focus` override/TODO; aligned the docs so generated subject artifacts are no longer described as living canonically inside this repository; and moved the current SAA2 artifacts into `../PIA-SAA/examenSAA/SAA2/` while ignoring the legacy local artifact paths.
- P36 — 2026-05-04. Extended `prompts/generate-questions.prompt.md` so Stage 3 learner-facing feedback forbids external-document anchors, added a final learner-facing-text validation pass, synced `prompts/AGENTS.md`, and repaired the remaining three feedback strings in `stage3-question-batches/saa2/ai-foundations-and-learning-paradigms/batch-001.json`. Validation confirmed no remaining forbidden material anchors under `stage3-question-batches/**`.
- P35 — 2026-05-04. Hardened `prompts/generate-questions.prompt.md` so Stage 3 `question_text` forbids external-document anchors with explicit Spanish and English examples plus a final stem-only validation pass, synced `prompts/AGENTS.md`, and repaired the five offending stems in `stage3-question-batches/saa2/ai-foundations-and-learning-paradigms/batch-001.json`. Scope remained limited to stems; feedback phrasing was left unchanged.
- P34 — 2026-05-04. Changed Stage 3 question generation to write batches directly to deterministic `stage3-question-batches/<subject>/<subcategory>/batch-###.json` paths, synced `README.md`, `prompts/AGENTS.md`, and `AGENTS.md`, and removed the manual save-from-chat expectation from the workflow.
- P4 — 2026-05-03. Reframed the prompt pipeline around question yield instead of raw concept count by making Stage 1 loss-minimizing and source-preserving, adding explicit `SURF-*` question surfaces in Stage 2, and making Stage 3 run coverage-first repeated batches. Synced `README.md`, `docs/summary_format.md`, `prompts/AGENTS.md`, and `AGENTS.md` to the new contract.
- P33 — 2026-04-30. Replaced the stale resolved P4 TODO in `prompts/merge-summaries.prompt.md` with a stable weighting note and revalidated that no live `TODO:` marker remains in that prompt.
- P9 — 2026-04-30. Added opt-in debug logging to `.github/hooks/src/todo_planner_context.py` via `--debug` or `TODO_PLANNER_CONTEXT_DEBUG`, kept default behavior stdout-only, removed the resolved TODO, and validated both unchanged stdout and debug-file emission.
- P19 — 2026-04-30. Added `.github/skills/customization-audit/SKILL.md`, updated the customization inventories and `.github/README.md`, and replaced the old customization-authoring TODO with a concrete periodic-audit workflow.
- P31 — 2026-04-30. Fixed `.github/hooks/src/todo_planner_context.py` to resolve the real repository root, then revalidated that the hook now injects the live `.github/implementation_plan.md` preview, correct marker counts, and the active branch name instead of the stale "no plan exists" fallback.
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

- 2026-05-19 - Repeated Stage 3 batching until coverage is exhausted should be a separate advanced skill over an approved Stage 2 scope. It should not overload the existing one-wave breadth-first Stage 3 bulk lane, and it should not pretend to replace missing Stage 2 taxonomy work.

- 2026-05-04 - Stage 3 concept, taxonomy, and hierarchy questions should be asked directly by default. Classroom, debate, or named-speaker wrappers are decorative when removing them leaves the reasoning unchanged; scenarios remain valid only when the concrete context materially affects the answer. This fix applies to future generation behavior, not retroactive JSON cleanup.
- 2026-05-04 - The old plan to add thin public bulk launchers for both Stage 1 and Stage 3 was reconsidered. Stage 1 bulk should stay on the existing `summarize-all-sources` skill with better documentation, while Stage 3 still needs an optional single-call delegated bulk lane in addition to the normal single-unit workflow.
- 2026-05-04 - The quiz pipeline should stop assuming that generated artifacts live inside this repository. Users provide the relevant input/output path or root, and prompts may derive deterministic filenames only beneath that user-owned location.
- 2026-05-04 - Stage 3 should no longer expose `Question focus` as a local override. The Stage 2 subcategory header is now the agreed single source of truth.

- 2026-04-30 - Resolved P9 direction: if hook-context debug logging is added, it must be opt-in behind an env var or flag. Default planner-hook behavior stays stdout-only.

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
