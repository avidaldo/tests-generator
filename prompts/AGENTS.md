# Prompts — Agent Instructions

## Current State

This folder contains the canonical prompt files for the repository. VS Code is configured to discover prompt files from this folder.

| File | Status | Description |
|------|--------|-------------|
| `summarize-sources.prompt.md` | **Active — Stage 1** | Rich content extraction from source files; one per repo or topic area |
| `merge-summaries.prompt.md` | **Active — Stage 2** | Organizes raw summaries into subcategory files with cross-cutting context |
| `generate-questions.prompt.md` | **Active — Stage 3** | Question generation in JSON format; one subcategory file per invocation |
| `deprecated/inventory.prompt.md` | **Deprecated** | Superseded by `summarize-sources.prompt.md` |
| `deprecated/generate-test.prompt.md` | **Deprecated** | Monolithic prompt — superseded by the 3-stage pipeline |

> **Note:** `metaprompting.prompt.md` was merged into `.github/instructions/prompt-authoring.instructions.md` — it was behavioural guidance, not a workflow prompt.

### Pipeline Overview

```
User provides repos (list of paths)
        │
        ▼  ── one invocation per repo (parallelizable) ──
[Stage 1: summarize-sources.prompt.md]
        │  Reads source files; extracts rich content (definitions,
        │  explanations, processes, cases, comparisons, examples)
        │  Strips irrelevant code and metadata
        │  Output: summary-{repo}.md  (one per repo, self-contained)
        ▼
User collects all summary files
        │
        ▼  ── single invocation ──
[Stage 2: merge-summaries.prompt.md]
        │  Reads all summaries; proposes subcategory taxonomy
        │  User reviews and adjusts subcategory names/boundaries
        │  Assigns concept IDs; adds "Related context" for cross-cutting concepts
        │  Output: subcategory-{name}.md  (one per subcategory, self-contained)
        ▼
User reviews subcategory files, adjusts if needed
        │
        ▼  ── one invocation per subcategory file (parallelizable) ──
[Stage 3: generate-questions.prompt.md]
        │  Reads one subcategory file (sole input)
        │  Generates questions + adversarial feedback validation
        │  Output: {subcategory}.json  (one per subcategory)
        ▼
[Quiz Editor — human review]   ← mandatory validation gate
        │  Human marks: Pendiente / Revisar / Lista
        ▼
[resources/json_to_moodle_xml.py]  ← deterministic script
        │  Output: Moodle XML (Lista questions only)
        ▼
Moodle import
```

Each stage is run manually by the user. Stages 1 and 3 are parallelizable (independent invocations); Stage 2 is a single merge pass.

**Intermediate format**: JSON conforming to [`docs/editor_json_schema.md`](../docs/editor_json_schema.md) — the canonical schema shared between the prompt output and the editor import (`editor/file_io/state_io.py`).
- Direct editor import — no conversion step
- Adversarial filter preserved via required `feedback` fields per distractor
- ~30 lines/question vs. ~60–80 for XML → roughly 2× throughput improvement

### Subject Profile

All three prompts accept a **Subject Profile** — two parameters the user can override at invocation time:

| Parameter | Default | Options |
|-----------|---------|---------|
| **Output language** | Castellano (Spanish), technical terms in English in parentheses | Any language |
| **Question focus** | `conceptual-only` | `conceptual-only` · `syntax-included` |

Each prompt asks the user to confirm these settings if they weren't stated in the invocation message.

### Cross-Cutting Concepts

A concept that appears across multiple subcategories (e.g. "overfitting" in regularisation, cross-validation, and bias-variance) has:

- A **primary subcategory** where its full content lives.
- **"Related context" entries** in other subcategory files — enough content (full scenarios, cases, comparisons) to generate cross-subcategory questions without reading the primary file.

This allows the question generator to create relationship questions (e.g. *"¿Cómo afecta la normalización al sobreajuste en modelos basados en distancia?"*) from a single file, with a fresh context window, and no cross-file drift.

### Tiered Reference System

Questions use **concept references** (e.g. `NORM-01` = concept #1 in the Normalización subcategory) in the `source_ref` field instead of raw file paths. Concept IDs are assigned in Stage 2 (merge), where the taxonomy is fixed.

```
Question JSON          Subcategory file          Raw summaries          Source files
─────────────          ────────────────          ─────────────          ────────────
source_ref: "NORM-01"  →  [NORM-01] defined in   →  summary-repo-a.md   →  02-preprocessing.ipynb
                           normalizacion.md           §Normalización          §Normalización
```

The human reviewer traces back via the subcategory file and raw summaries.

### Source File Types

Stage 1 handles three file types. Extraction depth depends on **question focus**:

| Type | `conceptual-only` (default) | `syntax-included` |
|------|----------------------------|---------------------|
| `.md` | Full text | Full text |
| `.ipynb` | Markdown cells + code cells read for concept context (not syntax) | Both markdown and code cells fully processed |
| `.py` | Docstrings, comments, conceptual patterns demonstrated by code | Code structure, function signatures, implementation patterns |

### Domain Knowledge

Psychometric design knowledge is maintained in `docs/` and auto-attached via instructions:

| Document | Content | Auto-attached via |
|----------|---------|-------------------|
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
|-------|---------|-----------------|
| Summarise (per repo) | Content extraction | One repo's files |
| Merge | Taxonomy + cross-cutting context | All summaries (small: no source files) |
| Generate (per subcategory) | Question design + adversarial validation | One subcategory file |

### Why Rich Summaries, Not Concept Lists

An earlier design extracted only concept names and definitions. This lost:
- **Processes**: step-by-step algorithms and procedures
- **Cases and analogies**: real-world examples that motivate scenario-based questions
- **Comparisons and decision criteria**: when to use X vs. Y, and why
- **Quantitative details**: numerical values and thresholds that make questions concrete

The current design preserves full content from source files, stripping only code syntax (in `conceptual-only` mode) and irrelevant metadata. The rule is: **when in doubt, keep it.**

### Why a Merge Step

Without a merge, the same subcategory (e.g. "normalisation") appears independently in multiple repo summaries, with no cross-repo connections. The merge step:
1. Identifies the unified taxonomy across all repos
2. Deduplicates overlapping content (using the most complete formulation)
3. Creates "Related context" sections so each subcategory file is self-contained for generation
4. Assigns concept IDs once the taxonomy is fixed

### Why Self-Contained Subcategory Files

The question generator receives one file and produces one JSON. This means:
- Each generation invocation gets a **fresh context window** — no drift
- No cross-file dependencies at generation time
- Stages 1 and 3 are trivially parallelizable (independent invocations)
- The subcategory file can be reviewed and adjusted before generation

### Why Concept IDs Are Assigned at Stage 2

Concept IDs are stable references for `source_ref` in question JSON. They need to be assigned after the taxonomy is fixed (Stage 2), not during extraction (Stage 1), because:
- The same concept may appear in multiple raw summaries under different names
- The subcategory a concept belongs to determines its ID prefix
- IDs assigned before merging would need renaming and conflict resolution

### Why the Editor Is a Mandatory Step

The editor is the human-in-the-loop validation gate. It catches domain errors the adversarial filter cannot self-detect, selects the best questions when there is redundancy, adjusts difficulty, and controls what actually reaches students.

### Why JSON as Intermediate Format

Direct editor import (zero conversion), adversarial filter preserved via required `feedback` fields, ~30 lines/question vs. ~60–80 for XML, source traceability via `source_ref`. Plain GIFT was rejected because the absence of feedback fields removes the adversarial filter entirely.

---

## Files

| File | Description |
|------|-------------|
| `prompts/summarize-sources.prompt.md` | Stage 1: rich content extraction from source files |
| `prompts/merge-summaries.prompt.md` | Stage 2: taxonomy organization, deduplication, cross-cutting context |
| `prompts/generate-questions.prompt.md` | Stage 3: question generation from subcategory files |
| `docs/adversarial_logic_filters.md` | Adversarial filter mechanism and prompting meta-techniques |
| `docs/distractor_design.md` | Distractor strategies, anti-bias rules, psychometric item quality |
| `resources/json_to_moodle_xml.py` | Export script: JSON → Moodle XML, status-filtered |
