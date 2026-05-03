---
name: summarize-all-sources
description: 'Fan out Stage 1 summarization across multiple material paths. Use when a subject spans several repos or topic folders and you want one summary per path while keeping each summarization in an isolated context window.'
argument-hint: 'Required: list of material paths; optional Question focus override'
---

# Summarize All Sources Workflow

This skill orchestrates Stage 1 of the quiz pipeline across multiple material paths. The canonical pipeline lives in [prompts/AGENTS.md](../../../prompts/AGENTS.md), and the Stage 1 extraction rules live in [prompts/summarize-sources.prompt.md](../../../prompts/summarize-sources.prompt.md).

## When To Use

- Summarize multiple repos, folders, or files in one request while keeping one summary per path.
- Parallelize Stage 1 work instead of manually running `summarize-sources.prompt.md` once per path.
- Reuse one shared Question focus setting across several Stage 1 runs.

## Inputs To Confirm

1. The complete list of material paths to summarize.
2. Any shared Subject Profile overrides relevant to Stage 1.
   In practice this usually means **Question focus** only; output language does not apply at this stage.
3. The preferred naming convention or destination for the resulting summary files if the user already has one.
4. Whether the run should continue from existing Stage 1 artifacts or start from scratch.

## Procedure

1. Validate the scope.
   Use this skill only for Stage 1 summarization. Do not merge summaries or generate questions here.
2. Normalize the work into explicit Stage 1 units.
   Treat each repo, folder, or file path as its own Stage 1 unit unless that unit triggers the split rule in [prompts/summarize-sources.prompt.md](../../../prompts/summarize-sources.prompt.md). When a path is too large, split it by coherent topic area before launching any summarization.
3. Create a checkpoint manifest before fan-out.
   Record every unit together with its intended artifact path and an explicit status such as `pending`, `running`, `done`, or `needs-fix`. Keep the manifest updated throughout the run so partial progress is visible and resumable.
4. Fan out one isolated summarization per unit, but only in small batches.
   Prefer one subagent or equivalent isolated invocation per unit when tooling allows it. Launch only a small batch at a time, typically 2 to 4 units, instead of dispatching the entire corpus at once.
5. Persist each output immediately to a deterministic artifact path.
   Prefer a subject-scoped folder such as `stage1-summaries/<subject>/summary-<unit>.md`. Do not report a unit as complete until its Stage 1 artifact exists on disk.
6. Keep the Stage 1 rules stable across all runs.
   Preserve the source material language, avoid external knowledge, and keep the selected Question focus consistent unless the user explicitly varies it per path.
7. Validate each artifact immediately after creation.
   Use the conventions in [docs/summary_format.md](../../../docs/summary_format.md): exact H1 section headings `# File Inventory`, `# Content`, `# Cross-References`; a clean inventory table; and no fenced code blocks. If an artifact fails validation, stop the current batch, repair or rerun that unit, and revalidate before launching more work.
8. Return one summary artifact per unit.
   Recommend filenames such as `summary-{slug}.md` and clearly map each output file back to its source path.
9. Stop at the Stage 1 boundary.
   Once all summaries are produced, direct the user to [prompts/merge-summaries.prompt.md](../../../prompts/merge-summaries.prompt.md).

## Guardrails

- Do not collapse multiple unrelated paths into one shared summary unless the user explicitly asks for that tradeoff.
- Do not invent cross-path taxonomy, deduplicate concepts, or add "Related context" sections here; that belongs to Stage 2.
- Do not translate Stage 1 outputs. Summaries preserve the source material language.
- If one path is too large or heterogeneous for one clean summary, say so and recommend splitting it by topic before proceeding.
- Do not mix planning narration with execution state. Report exact artifact paths and manifest status instead of vague progress claims.
- Do not continue fan-out after the first invalid Stage 1 artifact in a batch. Fix the failing unit first, then resume.
- Do not hand Stage 2 any Stage 1 artifact that has not passed the post-write validation checks.