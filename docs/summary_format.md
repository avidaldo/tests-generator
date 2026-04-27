# Summary Document Format

This document describes the expected output format of `prompts/summarize-sources.prompt.md`. The summary document serves as the sole input for `prompts/generate-questions.prompt.md`.

## Purpose

The summary document is the **bridge between course material repositories and question generation**. It:

- Is generated once per course or topic area
- Can be saved as a `.md` file and reused across sessions
- Contains all testable conceptual content extracted from the source materials
- Eliminates the need for the generation agent to access the original files

## Structure

A summary document has three sections:

### Section 1: File Inventory

A metadata table listing every file processed:

```markdown
| # | File | Type | Density | Est. Qs | Suggested subcategory |
|---|------|------|---------|---------|----------------------|
| 1 | intro/ml_overview.md | .md | 🟢 | 5–8 | Fundamentos/Introducción |
| 2 | notebooks/preprocessing.ipynb | .ipynb | 🟢 | 6–10 | Preprocessing/Normalización |
| 3 | src/pipeline.py | .py | 🟡 | 2–4 | Preprocessing/Pipelines |
| 4 | src/utils.py | .py | 🔴 | 0 | — |

**Estimated total questions:** 13–22
**Suggested category root:** $course$/top/MachineLearning
```

### Section 2: Concept Summaries (by subcategory)

One subsection per subcategory containing:

- **Key concepts** — definitions and explanations as found in the source
- **Relationships and distinctions** — how concepts relate, when each applies
- **Common misconceptions** — what students typically confuse
- **Examples and scenarios** — concrete cases from the source material
- **Edge cases and exceptions** — when usual rules don't apply

Example:

```markdown
## Preprocessing/Normalización

**Source files:** intro/ml_overview.md §Preprocessing, notebooks/preprocessing.ipynb

### Key concepts

- **Normalización min-max (min-max normalisation)**: Transforms features to a [0, 1] range. Formula: x' = (x - x_min) / (x_max - x_min). Preserves relative distances.
- **Estandarización (standardisation/z-score)**: Transforms features to mean=0, std=1. Formula: z = (x - μ) / σ. Does not bound the range.

### Relationships and distinctions

- Min-max vs. standardisation: min-max is sensitive to outliers because x_min and x_max shift; standardisation is more robust because μ and σ are less affected by individual outliers.
- Both are necessary before algorithms that use distance (KNN, SVM with RBF kernel) because unscaled features dominate the distance metric.

### Common misconceptions

- "Normalisation makes the data normal (Gaussian)" — this is false. Min-max preserves the original distribution shape; it only changes the range.
- Confusion between normalisation and standardisation — they are different transformations with different properties.

### Examples and scenarios

- [Source: notebooks/preprocessing.ipynb §Example 1] Applying min-max to a dataset with ages (0–100) and salaries (20,000–200,000). Without scaling, salary dominates any distance-based algorithm.

### Edge cases and exceptions

- If a feature has zero variance (constant), standardisation produces division by zero. Handle by dropping the feature or using a small epsilon.
```

### Section 3: Generation Notes

Brief guidance for the question generation agent:

```markdown
## Generation Notes

- Highest yield: Preprocessing/Normalización (rich conceptual content, many misconceptions)
- Tricky distractors: Evaluation/CrossValidation (students confuse k-fold with stratified k-fold)
- Cross-cutting: The concept of overfitting spans Fundamentos, Regularización, and Evaluation
- Factual issue: notebooks/preprocessing.ipynb §Section 3 contains an ambiguous explanation of L1 vs. L2 — verify before generating questions
```
