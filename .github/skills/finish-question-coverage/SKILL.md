---
name: finish-question-coverage
description: 'Continue Stage 3 generation across an approved Stage 2 scope until the selected subcategories have tracked SURF coverage or a declared stop condition is reached. Use when you want an advanced delegated or background lane that keeps designing batches after the first breadth-first wave while reusing one stable model label per written batch when known.'
argument-hint: 'Required: approved Stage 2 subcategory paths or root; Stage 3 output root; optional Output language, Question batch size, Model label, and stop condition'
---

# Finish Question Coverage Workflow

This skill orchestrates repeated Stage 3 runs over an approved Stage 2 scope. The canonical pipeline lives in [prompts/AGENTS.md](../../../prompts/AGENTS.md), the per-subcategory generation rules live in [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md), and the one-wave breadth-first Stage 3 lane lives in [generate-question-batches](../generate-question-batches/SKILL.md).

## When To Use

- Continue after the first breadth-first Stage 3 wave when selected subcategories still expose uncovered `SURF-*` units.
- Run exhaustive Stage 3 work until tracked coverage is exhausted across an approved Stage 2 scope.
- Resume a previous Stage 3 coverage run from a manifest created by this skill.

> **Background / Copilot CLI lane**: This skill runs inline in the current context window — context accumulates across all subcategories and waves. For runs where VS Code may close, or where context isolation per subcategory matters, use the [`stage3-runner` agent](../../agents/stage3-runner.agent.md) instead. It delegates each subcategory to an isolated `batch-generator` subagent and is Copilot CLI-compatible.

## When Not To Use

- The relevant Stage 2 subcategory files do not exist yet or their taxonomy is still being debated.
- You only want one new batch per subcategory in a single pass.
- You want exact manual control over one subcategory or one batch.

## Inputs To Confirm

1. The exact approved Stage 2 scope.
   Accept either an explicit list of `subcategory-*.md` files or a Stage 2 root whose files should be exhausted.
2. The Stage 3 output root.
   This is required. Use the existing Stage 3 path contract from [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md).
3. Shared Stage 3 settings.
   In practice this usually means **Output language**, optionally **Question batch size**, and optionally one stable **Model label** for the generated batches.
4. Continuation mode.
   Distinguish among a clean start, resuming from an existing manifest created by this skill, or adopting a Stage 3 root that already contains legacy batches.
5. The stop condition.
   Default to running until tracked Stage 3 coverage is exhausted for the selected scope. Allow a user-specified cap such as a maximum number of new batches or waves when needed.

## Procedure

1. Validate the upstream prerequisites.
   Use this skill only after the intended Stage 2 subcategory files already exist and their taxonomy is accepted. Do not summarize sources, merge summaries, or invent missing Stage 2 files here. If the user asks for full subject coverage but some intended source areas still lack Stage 2 files, stop and list those blockers as `blocked-upstream`.
2. Normalize the work into explicit Stage 3 units.
   Treat each `subcategory-*.md` file as one Stage 3 unit and extract its `SURF-*` list into a per-subcategory coverage ledger.
3. Create or load a coverage manifest.
   Store it under the Stage 3 root, for example `stage3-coverage-manifest.md`. For each subcategory, record the subcategory path, known `SURF-*` entries, tracked `SURF-*` entries already assigned to validated batches, the next intended batch path, status, and any resume notes.
4. Handle existing Stage 3 artifacts honestly.
   - If a manifest from this skill already exists, resume from it.
   - If batches exist without a manifest, record them as `legacy-existing` rather than pretending their `SURF-*` coverage is known.
   - If the user wants a clean run, write to a fresh Stage 3 root or mark older artifacts ignored for coverage accounting.
5. Choose the next batch scope from uncovered `SURF-*` entries.
   Group uncovered surfaces into a coherent batch that honors the requested question batch size and prefers fresh surfaces before duplicates. Use an explicit `SURF-*` scope when invoking Stage 3 generation.
6. Reuse the canonical Stage 3 rules for every batch.
   For each selected scope, apply [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md) without inventing a second Stage 3 policy. Respect the inherited Question focus, the user-provided Stage 3 output root, the learner-facing self-containment rules, the direct-stem rules, and the JSON schema contract.
   If the run includes a Model label, write that exact stable value to `generated_by_model` on every question in the saved batch. Do not vary the value inside one batch.
7. Persist and validate each batch before continuing.
   Write the next free `batch-###.json`, then re-open it and confirm that it parses, each question has exactly 7 answers, every answer has feedback, the learner-facing text is self-contained, the correct option is not uniquely longest or shortest by a clear margin when you compare normalized visible option text only, the manifest records which `SURF-*` entries this batch was meant to cover, and when a Model label was requested every question in that batch carries the same `generated_by_model` value. If one batch fails validation, stop the run, mark that unit `needs-fix`, and do not continue.
8. Update the manifest after every batch.
   Record the saved batch path, the targeted `SURF-*` entries, validation status, and the next uncovered surfaces so the run stays inspectable and resumable.
9. Continue wave by wave until the stop condition is met.
   The default stop condition is: every selected subcategory is now `done`, `needs-fix`, `blocked-upstream`, or `skipped`. Mark a subcategory `done` only when every known `SURF-*` entry in that Stage 2 file has at least one validated tracked batch.
10. Stop at the Stage 3 boundary.
    Completion here means coverage-complete Stage 3 artifacts for the approved Stage 2 scope. It does not mean reviewed or export-ready exams. Human editor review remains mandatory before XML export.

## Guardrails

- Do not replace missing or unstable Stage 2 work. Upstream taxonomy gaps are blockers, not an invitation to improvise Stage 2 here.
- Do not overload the one-wave Stage 3 skill. Use [generate-question-batches](../generate-question-batches/SKILL.md) for a single breadth-first pass; use this skill only when repeated successive batching is the point.
- Do not infer `SURF-*` coverage from untracked legacy batches.
- Do not overwrite existing batch files implicitly. Always advance to the next free `batch-###.json` unless the user explicitly requests a specific batch number.
- Do not mix model labels inside one written batch. If a different model label is needed, that is a different batch run.
- Do not continue past the first invalid generated artifact in the current run.
- Do not claim full subject coverage unless the selected Stage 2 scope itself covers the intended subject.
- Do not skip the human review gate. This skill increases Stage 3 throughput only; it does not replace editor review.