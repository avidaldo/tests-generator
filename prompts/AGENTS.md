# Prompts — Agent Instructions

## Current State

This folder contains the canonical question-generation prompt files for the repository. VS Code discovers this folder through `chat.promptFilesLocations` in `.vscode/settings.json`. Repository-maintenance launchers live in [../.github/prompts/AGENTS.md](../.github/prompts/AGENTS.md).

For the detailed decision guide on regular versus bulk execution, the user-owned artifact path contract, and when to use the Stage 1 or Stage 3 skills instead of the precise prompt lane, see [docs/pipeline_execution_modes.md](../docs/pipeline_execution_modes.md).

| File | Status | Description |
| ---- | ------ | ----------- |
| `summarize-sources.prompt.md` | **Active — Stage 1** | Loss-minimizing source extraction from source files; one per repo or coherent topic area; write summaries to user-provided Stage 1 paths or roots |
| `merge-summaries.prompt.md` | **Active — Stage 2** | Organizes raw extraction files into subcategory files with concept IDs, question surfaces, and cross-cutting context |
| `generate-questions.prompt.md` | **Active — Stage 3** | Question generation in JSON batches written directly to user-provided Stage 3 paths or roots; one batch per invocation from one subcategory file, repeat until surfaces are covered |
| `finish-stage3-coverage.prompt.md` | **Active — Stage 3 launcher** | Preferred user-facing one-step launcher for approved-scope exhaustive Stage 3 runs; reuses the exhaustive coverage workflow and keeps a manifest under the Stage 3 root |
| `deprecated/inventory.prompt.md` | **Deprecated** | Superseded by `summarize-sources.prompt.md` |
| `deprecated/generate-test.prompt.md` | **Deprecated** | Monolithic prompt — superseded by the 3-stage pipeline |

> **Note:** `metaprompting.prompt.md` was merged into `.github/instructions/prompt-authoring.instructions.md` — it was behavioural guidance, not a workflow prompt.

### Pipeline Overview

Optional helper for Stage 1 fan-out: [`.github/skills/summarize-all-sources/SKILL.md`](../.github/skills/summarize-all-sources/SKILL.md) can orchestrate one isolated `summarize-sources.prompt.md` run per material path, then return one summary artifact per path.

Optional helper for advanced Stage 3 breadth-first runs: [`.github/skills/generate-question-batches/SKILL.md`](../.github/skills/generate-question-batches/SKILL.md) can traverse multiple subcategory files from one delegated or background run, write at most one new batch per subcategory, and keep checkpointed progress under the user-provided Stage 3 root.

Optional helper for advanced Stage 3 exhaustive runs over an approved Stage 2 scope: [`.github/skills/finish-question-coverage/SKILL.md`](../.github/skills/finish-question-coverage/SKILL.md) can continue with successive batches until tracked `SURF-*` coverage is exhausted while keeping a coverage manifest under the user-provided Stage 3 root.

Preferred user-facing launcher for that exhaustive Stage 3 lane: [`finish-stage3-coverage.prompt.md`](finish-stage3-coverage.prompt.md). It keeps the project-facing entrypoint in root `prompts/` while reusing the existing exhaustive skill as the implementation layer.

```text
User provides repos (list of paths)
        │
        ▼  ── one invocation per repo/path (parallelizable; optional `summarize-all-sources` orchestration) ──
[Stage 1: summarize-sources.prompt.md]
        │  Reads source files; performs loss-minimizing extraction
        │  (definitions, explanations, procedures, cases,
        │  comparisons, decision criteria, misconceptions,
        │  quantitative anchors, edge cases)
        │  Strips only irrelevant code syntax and boilerplate
        │  Output: summary-{repo-or-topic}.md under a user-provided Stage 1 root
        ▼
User collects all summary files
        │
        ▼  ── single invocation ──
[Stage 2: merge-summaries.prompt.md]
        │  Reads all summaries; proposes subcategory taxonomy
        │  User reviews and adjusts subcategory names/boundaries
        │  Assigns concept IDs; records question surfaces; adds
        │  "Related context" for cross-cutting concepts
        │  Output: subcategory-{name}.md under a user-provided Stage 2 root
        ▼
User reviews subcategory files, adjusts if needed
        │
        ▼  ── one invocation per subcategory file (parallelizable; optional `generate-question-batches` orchestration for one breadth-first wave; optional `finish-stage3-coverage.prompt.md` launcher for approved-scope exhaustive Stage 3 runs) ──
[Stage 3: generate-questions.prompt.md]
        │  Reads one subcategory file (sole input)
        │  Generates one coverage-first JSON batch + adversarial
        │  feedback validation
        │  Output: <user-stage3-root>/<subcategory>/batch-###.json
        ▼
[Quiz Editor — human review]   ← mandatory validation gate
        │  Imports one or more Stage 3 batches into one Stage 4
        │  review-session JSON; human marks: Pendiente / Revisar / Lista
        ▼
[resources/json_to_moodle_xml.py]  ← deterministic script
        │  Output: Moodle XML (Lista questions only)
        ▼
Moodle import
```

Each stage is run manually by the user. Stages 1 and 3 are parallelizable (independent invocations); Stage 1 fan-out can also be orchestrated through the `summarize-all-sources` skill, Stage 3 breadth-first delegated runs can be orchestrated through the `generate-question-batches` skill, and Stage 3 exhaustive approved-scope runs can be launched through `finish-stage3-coverage.prompt.md` while reusing the `finish-question-coverage` skill underneath. Stage 2 is still a single merge pass. Each prompt should ask for the relevant input or output path when the user did not already provide it. If a repo is too large or heterogeneous for one faithful Stage 1 document, split it by coherent topic area before continuing; a monolithic lossy summary is invalid.

### Stage 3 Artifact Guardrails

- Require either a user-provided Stage 3 output root or an explicit output file path before writing.
- When the user provides a Stage 3 output root, derive a deterministic per-subcategory folder beneath it using the input filename with the `subcategory-` prefix removed, then write `batch-###.json` there.
- Never overwrite an existing batch file implicitly. Repeated runs should create the next free `batch-###.json` in that same subcategory folder unless the user explicitly requests a specific batch number.
- Stage 3 learner-facing text must be self-contained. `question_text`, `general_feedback`, and `answers[].feedback` must not refer to "the material", "the notes", "the notebook", slides, or similar external anchors; source attribution belongs in `source_ref`, not in learner-facing text.
- Stage 3 concept, taxonomy, hierarchy, and misconception-correction stems should be direct by default. Use scenario framing only when the concrete context materially changes the reasoning, diagnosis, trade-off, or procedural choice being tested.

### Stage 1 Operational Guardrails

- Require either a user-provided Stage 1 output root or explicit output file paths before writing summaries.
- When the user provides a Stage 1 output root, write deterministic filenames such as `summary-<repo-or-topic>.md` beneath that root so partial progress is inspectable and resumable.
- Keep a lightweight manifest in that same user-provided Stage 1 root tracking every Stage 1 unit with an explicit status such as `pending`, `running`, `done`, or `needs-fix`.
- Fan out in small batches, typically 2 to 4 Stage 1 units at a time. Do not dispatch the full corpus before validating the first outputs.
- After each batch, validate every produced summary against [docs/summary_format.md](../docs/summary_format.md). In this repo the practical minimum is: exact H1 headings `# File Inventory`, `# Content`, `# Cross-References`; a valid inventory table; and no fenced code blocks.
- Stop the batch on the first invalid summary. Repair or rerun that unit, then revalidate before launching more Stage 1 work.
- Treat existing partial summaries as inputs to validate, not as automatically trusted artifacts. Stage 2 should receive only validated Stage 1 files.

Repository-maintenance launchers are documented separately in [../.github/prompts/AGENTS.md](../.github/prompts/AGENTS.md). This file is only for the quiz-generation pipeline.

**Intermediate format**: JSON conforming to [`docs/editor_json_schema.md`](../docs/editor_json_schema.md) — the canonical schema for both the immutable Stage 3 batch envelope and the editor-owned Stage 4 review-session envelope used by `editor/file_io/state_io.py`.

- Direct Stage 3 import into the editor, then Stage 4 review-session save/load with no conversion step
- Adversarial filter preserved via required `feedback` fields per distractor
- ~30 lines/question vs. ~60–80 for XML → roughly 2× throughput improvement

### Subject Profile

The prompts accept a small **Subject Profile**, but not every parameter belongs in every stage:

| Parameter | Prompts | Default | Options |
| --------- | ------- | ------- | ------- |
| **Question focus** | `summarize-sources`, `merge-summaries` | `conceptual-only` | `conceptual-only` · `syntax-included` |
| **Output language** | `generate-questions` only | Source corpus language (inferred from the subcategory file); if unspecified, explicitly offer Castellano (Spanish) as the usual Stage 3 target | Any language; for translated output, keep domain-standard technical terms in English or include the English term in parentheses |

`generate-questions.prompt.md` inherits **Question focus** from the Stage 2 subcategory file header instead of exposing a local override.

Output language is set only at the question-generation stage (`generate-questions.prompt.md`). Summarisation and merge stages preserve the source material's language.

When translation is required at Stage 3, use a technical register aligned with real field usage: keep terms that are commonly used in English in technical contexts in English, or include the English term in parentheses when translated.

Each prompt asks the user to confirm these settings if they weren't stated in the invocation message.

### Cross-Cutting Concepts

A concept that appears across multiple subcategories (e.g. "overfitting" in regularisation, cross-validation, and bias-variance) has:

- A **primary subcategory** where its full content lives.
- **"Related context" entries** in other subcategory files — enough content (full scenarios, cases, comparisons) to generate cross-subcategory questions without reading the primary file.

This allows the question generator to create relationship questions (e.g. *"¿Cómo afecta la normalización al sobreajuste en modelos basados en distancia?"*) from a single file, with a fresh context window, and no cross-file drift.

### Tiered Reference System

Questions use **concept references** (e.g. `NORM-01` = concept #1 in the Normalización subcategory) in the `source_ref` field instead of raw file paths. Concept IDs are assigned in Stage 2 (merge), where the taxonomy is fixed.

```text
Question JSON          Subcategory file          Raw summaries          Source files
─────────────          ────────────────          ─────────────          ────────────
source_ref: "NORM-01"  →  [NORM-01] defined in   →  summary-repo-a.md   →  02-preprocessing.ipynb
                           normalizacion.md           §Normalización          §Normalización
```

The human reviewer traces back via the subcategory file and raw summaries.

### Source File Types

Stage 1 handles three file types. Extraction depth depends on **question focus**:

| Type | `conceptual-only` (default) | `syntax-included` |
| ---- | --------------------------- | ----------------- |
| `.md` | Full text | Full text |
| `.ipynb` | Markdown cells + code cells read for concept context (not syntax) | Both markdown and code cells fully processed |
| `.py` | Docstrings, comments, conceptual patterns demonstrated by code | Code structure, function signatures, implementation patterns |

### Domain Knowledge

Psychometric design knowledge is maintained in `docs/` and auto-attached via instructions:

| Document | Content | Auto-attached via |
| -------- | ------- | ----------------- |
| [docs/adversarial_logic_filters.md](../docs/adversarial_logic_filters.md) | Adversarial filter mechanism, CoT strategy, prompting meta-techniques | Referenced in generation prompt |
| [docs/distractor_design.md](../docs/distractor_design.md) | Distractor strategies, anti-bias rules, scenario triangulation, psychometric item quality | `.github/instructions/question-design.instructions.md` |

## Canonical Prompt Authoring Rules

- Keep `.github/instructions/prompt-authoring.instructions.md` as a VS Code routing adapter only, not as a second source of prompt policy.
- Keep canonical project prompt files under `prompts/` in this repository.
- Keep prompt instructions focused on a single reusable workflow.
- When designing or reviewing prompts, consult current official prompting guidance and current VS Code customization docs before changing the file.
- For quiz-generation prompts, preserve the requirement to consult `docs/adversarial_logic_filters.md` and `docs/distractor_design.md`.

---

## Design Rationale

### Why Three Stages

The original monolithic `generate-test.prompt.md` performed reading, organisation, and generation in a single agent turn. This caused: context exhaustion, output bloat (XML verbosity), and coupled failures. The 3-stage pipeline isolates each concern:

| Stage | Concern | Context pressure |
| ----- | ------- | ---------------- |
| Summarise (per repo) | Content extraction | One repo's files |
| Merge | Taxonomy + cross-cutting context | All summaries (small: no source files) |
| Generate (per subcategory) | Question design + adversarial validation | One subcategory file |

### Why Loss-Minimizing Extraction, Not High-Level Summaries

An earlier design extracted only concept names and definitions. A later failure mode produced repo-level overviews with a small content synopsis. Both lose too much information. They discard:

- **Processes**: step-by-step algorithms and procedures
- **Cases and analogies**: real-world examples that motivate scenario-based questions
- **Comparisons and decision criteria**: when to use X vs. Y, and why
- **Quantitative details**: numerical values and thresholds that make questions concrete
- **Misconceptions and failure modes**: exactly the material that supports strong distractors

The current design is therefore intentionally loss-minimizing. Stage 1 preserves source-organized content from each relevant file, stripping only raw code syntax (in `conceptual-only` mode) and irrelevant metadata. The rule is: **when in doubt, keep it.**

### Why a Merge Step

Without a merge, the same subcategory (e.g. "normalisation") appears independently in multiple repo summaries, with no cross-repo connections. The merge step:

1. Identifies the unified taxonomy across all repos
2. Deduplicates overlapping content (using the most complete formulation)
3. Creates "Related context" sections so each subcategory file is self-contained for generation
4. Assigns concept IDs once the taxonomy is fixed

### Why Self-Contained Subcategory Files

The question generator receives one file and produces one JSON batch. This means:

- Each generation invocation gets a **fresh context window** — no drift
- No cross-file dependencies at generation time
- Stages 1 and 3 are trivially parallelizable (independent invocations)
- The subcategory file can be reviewed and adjusted before generation
- The merge stage can record explicit `SURF-*` question surfaces so Stage 3 can cover the material systematically instead of improvising from concept names alone

### Why Concept IDs Are Assigned at Stage 2

Concept IDs are stable references for `source_ref` in question JSON. They need to be assigned after the taxonomy is fixed (Stage 2), not during extraction (Stage 1), because:

- The same concept may appear in multiple raw summaries under different names
- The subcategory a concept belongs to determines its ID prefix
- IDs assigned before merging would need renaming and conflict resolution

### Why Question Surfaces Are Assigned at Stage 2

Question yield depends on more than concept count. Good questions come from distinct surfaces such as definitions, comparisons, procedures, decision criteria, misconceptions, scenarios, quantitative anchors, and edge cases.

Stage 2 is the first point where the taxonomy is stable enough to record those surfaces explicitly. That makes Stage 3 coverage-driven instead of relying on the generator to rediscover every angle from scratch in each batch.

### Why the Editor Is a Mandatory Step

The editor is the human-in-the-loop validation gate. It catches domain errors the adversarial filter cannot self-detect, selects the best questions when there is redundancy, adjusts difficulty, and controls what actually reaches students.

The editor now owns a separate Stage 4 review-session artifact so multiple Stage 3 batches can be reviewed together without mutating the original generation outputs.

### Why JSON as Intermediate Format

Direct Stage 3 import into the editor, editor-owned Stage 4 review-session persistence, adversarial filter preserved via required `feedback` fields, ~30 lines/question vs. ~60–80 for XML, and source traceability via `source_ref`. Plain GIFT was rejected because the absence of feedback fields removes the adversarial filter entirely.

---

## Files

| File | Description |
| ---- | ----------- |
| `prompts/summarize-sources.prompt.md` | Stage 1: rich content extraction from source files |
| `prompts/merge-summaries.prompt.md` | Stage 2: taxonomy organization, deduplication, cross-cutting context |
| `prompts/generate-questions.prompt.md` | Stage 3: question generation from subcategory files |
| `prompts/finish-stage3-coverage.prompt.md` | Preferred user-facing launcher for exhaustive Stage 3 runs over an approved Stage 2 scope |
| `docs/adversarial_logic_filters.md` | Adversarial filter mechanism and prompting meta-techniques |
| `docs/distractor_design.md` | Distractor strategies, anti-bias rules, psychometric item quality |
| `resources/json_to_moodle_xml.py` | Export script: JSON → Moodle XML, status-filtered |
