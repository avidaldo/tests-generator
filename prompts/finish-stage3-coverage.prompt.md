---
name: finish-stage3-coverage
description: >
  Launch exhaustive Stage 3 generation across an approved Stage 2 scope until tracked SURF coverage is exhausted. Preferred user-facing one-step lane for unattended Stage 3 runs.
argument-hint: 'Approved Stage 2 scope or root; Stage 3 output root; optional Output language, Question batch size, Model label, continuation mode, and stop condition'
agent: agent
---

# Exhaustive Stage 3 Launcher

Use this prompt when the relevant Stage 2 subcategory files already exist, their taxonomy is approved, and you want Stage 3 to continue batch by batch until tracked `SURF-*` coverage is exhausted.

Do not use this prompt when Stage 2 is incomplete or still being debated, when you want exact control over a single subcategory or batch, or when you only want one breadth-first Stage 3 pass.

Use [generate-questions.prompt.md](generate-questions.prompt.md) for one subcategory at a time. Use the breadth-first bulk lane documented in [docs/pipeline_execution_modes.md](../docs/pipeline_execution_modes.md) when you want at most one new batch per subcategory in a delegated pass.

## Inputs

You can provide the Stage 2 scope in two ways:
- **Inline text**: fill in the `stage2_scope` form field below.
- **`@file:` folder attachment**: attach the Stage 2 subcategory folder directly in the chat. If a folder is attached, it takes precedence over the form field.

If both are provided, the `@file:` attachment wins. If neither is provided, ask once before proceeding.

- Approved Stage 2 scope: ${input:stage2_scope:Explicit subcategory file list or a Stage 2 root to exhaust — or attach with @file:}
- Stage 3 output root: ${input:stage3_root:Path to the user-owned Stage 3 root}
- Output language: ${input:output_language:Castellano}
- Question batch size: ${input:batch_size:12}
- Model label: ${input:model_label:omit if unknown; otherwise one stable batch-wide label such as gpt-5.4}
- Continuation mode: ${input:continuation_mode:clean-start | resume-manifest | adopt-legacy}
- Stop condition: ${input:stop_condition:coverage-complete}

## Instructions

1. Treat this prompt as the preferred user-facing launcher for exhaustive Stage 3 runs over an approved Stage 2 scope.
2. Reuse the workflow in [`.github/skills/finish-question-coverage/SKILL.md`](../.github/skills/finish-question-coverage/SKILL.md). Do not invent a second exhaustive Stage 3 policy here.
3. Reuse [generate-questions.prompt.md](generate-questions.prompt.md) as the per-batch Stage 3 policy and JSON contract. Do not weaken its guardrails.
4. Validate the upstream prerequisites first. If the selected Stage 2 scope is incomplete, unstable, or still being debated, stop and report the blockers instead of generating batches.
5. Ask only for missing or ambiguous inputs. If the inputs are already clear, start directly.
6. Keep all outputs under the provided Stage 3 root, maintain or create the coverage manifest there, and never overwrite an existing batch implicitly.
7. If a Model label is provided, treat it as a shared batch-wide Stage 3 setting and write that exact value to `generated_by_model` on every question in each saved batch.
8. Continue batch by batch until the stop condition is reached or the first blocker or invalid artifact appears.
9. Keep progress messages terse: saved batch path, question count, targeted `SURF-*`, model label when used, and next state.
10. Finish with a concise run summary listing completed subcategories, blocked items, and the manifest path.

## Requested Run

- Approved Stage 2 scope: ${input:stage2_scope}
- Stage 3 output root: ${input:stage3_root}
- Output language: ${input:output_language}
- Question batch size: ${input:batch_size}
- Model label: ${input:model_label}
- Continuation mode: ${input:continuation_mode}
- Stop condition: ${input:stop_condition}