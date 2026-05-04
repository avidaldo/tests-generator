---
name: generate-question-batches
description: 'Traverse multiple Stage 2 subcategory files in one Stage 3 run. Use when you want an advanced delegated or background lane that writes at most one new question batch per subcategory while keeping checkpointed progress under a user-provided Stage 3 root.'
argument-hint: 'Required: Stage 2 subcategory paths or root; Stage 3 output root; optional Output language and Question batch size'
---

# Generate Question Batches Workflow

This skill orchestrates Stage 3 of the quiz pipeline across multiple subcategory files. The canonical pipeline lives in [prompts/AGENTS.md](../../../prompts/AGENTS.md), and the per-subcategory generation rules live in [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md).

## When To Use

- Generate breadth-first Stage 3 coverage across multiple subcategories from one request.
- Run delegated or background Stage 3 work while keeping progress inspectable and resumable.
- Create at most one new JSON batch per subcategory in a single bulk pass before human editor review.

## Inputs To Confirm

1. The exact Stage 2 subcategory scope.
   Accept either an explicit list of subcategory file paths or a Stage 2 root whose `subcategory-*.md` files should be traversed.
2. The Stage 3 output root.
   This is required. Use the existing Stage 3 path contract from [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md).
3. Any shared Stage 3 settings.
   In practice this usually means **Output language** and optionally **Question batch size**. If the user needs materially different settings per subcategory, split the run instead of pretending one bulk pass is coherent.
4. Whether the run should continue from existing Stage 3 artifacts or start from scratch.

## Procedure

1. Validate the scope.
   Use this skill only for Stage 3 question generation. Do not summarize sources, merge summaries, or perform editor review here.
2. Normalize the work into explicit Stage 3 units.
   Treat each `subcategory-*.md` file as one unit. Keep the prompt contract unchanged: one subcategory file remains the source of truth for each generated batch.
3. Create a checkpoint manifest before generation.
   Unless the user already has a manifest, create one under the Stage 3 output root, for example `stage3-bulk-manifest.md`. Record each subcategory path together with its next intended batch path and a status such as `pending`, `running`, `done`, `needs-fix`, or `skipped`.
4. Process the units breadth-first.
   In one bulk pass, generate at most one new batch per subcategory. This lane is for advancing multiple subcategories safely, not for exhausting every surface inside one subcategory before review.
5. Reuse the canonical Stage 3 rules for every unit.
   For each subcategory, apply [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md) without inventing a second Stage 3 policy. Respect the inherited Question focus, the user-provided Stage 3 output root, the direct-stem rules, the learner-facing self-containment rules, and the existing JSON schema contract.
6. Persist each output immediately.
   Derive the per-subcategory folder from the input filename, write the next free `batch-###.json`, and do not report the unit as complete until the file exists on disk and the manifest is updated.
7. Validate each written batch before continuing.
   Re-open the saved JSON and confirm that it parses, each question has exactly 7 answers, every answer has feedback, the learner-facing text is self-contained, and no direct concept stem drifts back into decorative classroom or named-speaker wrappers. If one unit fails validation, stop the pass, mark that unit `needs-fix`, and do not continue to later units until the failure is repaired or consciously deferred.
8. Keep partial progress inspectable.
   Update the manifest after every unit with the saved batch path, status, and any note needed to resume safely.
9. Stop at the Stage 3 boundary.
   Once the bulk pass is done, direct the user to review the generated batches in the editor before generating additional waves.

## Guardrails

- Do not replace the normal precise workflow. The default Stage 3 surface remains one invocation of [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md) per subcategory.
- Do not write more than one new batch per subcategory in a single bulk pass unless the user explicitly narrows the run to that subcategory and asks for repeated batching.
- Do not overwrite existing batch files implicitly. Always advance to the next free `batch-###.json` unless the user explicitly requests a specific batch number.
- Do not continue past the first invalid generated artifact in the current pass. Stop, record the failure, and keep the checkpoint state honest.
- Do not skip the human review gate. Bulk generation increases throughput, but the editor remains the mandatory validation boundary before XML export or further repeated batching.