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

## Procedure

1. Validate the scope.
   Use this skill only for Stage 1 summarization. Do not merge summaries or generate questions here.
2. Split the work by path.
   Treat each repo, folder, or file path as its own Stage 1 unit so each summary is self-contained.
3. Fan out one isolated summarization per path.
   Prefer one subagent or equivalent isolated invocation per path when tooling allows it. Each run should follow [prompts/summarize-sources.prompt.md](../../../prompts/summarize-sources.prompt.md) against only that path.
4. Keep the Stage 1 rules stable across all runs.
   Preserve the source material language, avoid external knowledge, and keep the selected Question focus consistent unless the user explicitly varies it per path.
5. Return one summary artifact per path.
   Recommend filenames such as `summary-{slug}.md` and clearly map each output file back to its source path.
6. Stop at the Stage 1 boundary.
   Once all summaries are produced, direct the user to [prompts/merge-summaries.prompt.md](../../../prompts/merge-summaries.prompt.md).

## Guardrails

- Do not collapse multiple unrelated paths into one shared summary unless the user explicitly asks for that tradeoff.
- Do not invent cross-path taxonomy, deduplicate concepts, or add "Related context" sections here; that belongs to Stage 2.
- Do not translate Stage 1 outputs. Summaries preserve the source material language.
- If one path is too large or heterogeneous for one clean summary, say so and recommend splitting it by topic before proceeding.