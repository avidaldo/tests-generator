# Summary Document Format

This document describes the expected output of `prompts/summarize-sources.prompt.md`. A Stage 1 summary document is the input to `prompts/merge-summaries.prompt.md`, not directly to question generation.

## Purpose

The summary document is the **loss-minimizing bridge between source materials and the merge step**. It:

- Is generated once per repository or coherent topic area
- Can be saved as a `.md` file and reused across sessions
- Preserves all question-worthy content from the source materials, not just high-level concepts
- Eliminates the need for the merge agent to reopen the original files
- Must not degrade into a repo overview, executive summary, or topic synopsis

## Structure

A Stage 1 summary document has three sections in this order.

### Section 1: File Inventory

A traceability table listing every processed file.

```markdown
| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | intro/ml_overview.md | `.md` | ✅ |
| 2 | notebooks/preprocessing.ipynb | `.ipynb` | ✅ |
| 3 | src/pipeline.py | `.py` | ✅ |
| 4 | src/utils.py | `.py` | ❌ (boilerplate) |
```

Rules:

- `File` is always relative to the input root for that Stage 1 run.
- `Relevant` is `✅` only when the file contributes extractable teaching content.
- Any file marked `✅` must appear in Section 2.

### Section 2: Content

This section is **source-preserving extraction**, not subcategory organization.

- Every relevant file gets its own top-level heading: `## [Source: relative/path.ext]`
- Preserve the file's own major headings as `###` subsections when they exist.
- For notebooks or scripts with little prose, create explicit subsections such as `Code-demonstrated concepts`, `Observed results`, or `Procedure shown by the code` and describe the demonstrated content faithfully.
- Preserve near-verbatim wording for scenarios, trade-offs, warnings, decision criteria, step sequences, and quantitative examples whenever paraphrasing would weaken the material.
- Strip only raw syntax, metadata, boilerplate, and formatting artefacts.

Example:

```markdown
## [Source: sklearn/overfitting_train_test_split.ipynb]

### Problem Definition and Data Preparation

Overfitting occurs when the model fits the training data too closely and fails to generalize to new data. A typical mitigation is to hold out a test set, often around 20% of the data, though the appropriate split depends on dataset size.

### Why Train/Test Separation Matters

If the error is low on the training set but high on the test set, the model is overfitted. This means performance on seen data is not evidence of reliable future behavior.

### Code-demonstrated concepts

[Code example: demonstrates splitting tabular data into train and test partitions with a fixed random seed so evaluation is reproducible.]
```

What Section 2 must preserve whenever present in the source:

- Definitions and explanations
- Processes and procedures
- Cases, analogies, and scenarios
- Comparisons and distinctions
- Decision criteria and trade-offs
- Common misconceptions and warnings
- Quantitative anchors, parameters, and thresholds
- Edge cases and exceptions

### Section 3: Cross-References

This section records relationships that span source files and will matter during merge.

```markdown
## Cross-References

### Comparisons and distinctions
- "Min-max scaling" vs. "Z-score standardisation": [full explanation with when each applies] [Source: file.md §Comparison]

### Dependencies and prerequisites
- "Cross-validation" builds on "Train/test split" as a base concept. [Source: ...]

### Decision criteria and context-dependent choices
- When to prefer precision over recall: [full explanation with motivating scenarios] [Source: ...]
```

## Quality Rules

- Do not collapse multiple files into one repo-level paragraph.
- Do not replace procedures or examples with short labels such as "this notebook covers preprocessing".
- If two passages look similar but one adds nuance, preserve the nuance.
- If the input is too large or heterogeneous for one faithful document, split it by topic area instead of compressing it.
- The final document must be rich enough that Stage 2 can work without reopening the original repository.
