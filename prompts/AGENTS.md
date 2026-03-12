# Prompts — Agent Instructions & Decomposition Planning

## Current State

This folder contains the canonical prompt files for the repository, along with prompt design notes and decomposition planning. VS Code is configured to discover prompt files from this folder.

| File | Status | Description |
|------|--------|-------------|
| `generate-test.prompt.md` | **Active — to be decomposed** | Monolithic exam generation prompt |
| `metaprompting.prompt.md` | Stable | Prompt design guidelines |

## Canonical Prompt Authoring Rules

This file is the canonical, tool-agnostic instruction surface for the `prompts/` module.

- Keep `.github/instructions/prompt-authoring.instructions.md` as a VS Code routing adapter only, not as a second source of prompt policy.
- Keep canonical project prompt files under `prompts/` in this repository. Use VS Code settings only to discover that location.
- Use current prompt metadata only. In prompt files, `agent` must be a valid agent identifier such as `ask`, `agent`, `plan`, or a custom agent name available in the workspace.
- Keep prompt instructions focused on a single reusable workflow. If a workflow requires persistent persona, tool restrictions, or handoffs, prefer a custom agent or skill instead of growing one prompt indefinitely.
- When designing or reviewing prompts, consult current official prompting guidance and current VS Code customization docs before changing the file.
- For quiz-generation prompts, preserve the requirement to consult `docs/adversarial_logic_filters.md`.

---

## Problem Analysis: Why Decomposition is Needed

`generate-test.prompt.md` currently performs three distinct tasks in a single agent turn:

1. **Inventory**: Reads all source files, classifies by concept density, produces a tracking table.
2. **Generation**: Designs questions with adversarial distractor validation, outputs Moodle XML with `<feedback>` fields.
3. **Continuation tracking**: Maintains state across multiple output batches.

### Observed Failure Modes

**Context exhaustion on input**: When source material is large (many `.md` files + `.ipynb` notebooks), the inventory phase consumes so much context that generation quality degrades.

**Output bloat causing degradation**: Moodle XML + feedback is ~50–80 lines per question (7 options × feedback + CDATA wrappers). After ~15 questions the model begins truncating, losing structure, or hallucinating XML syntax.

**Coupled responsibilities**: A failure in XML formatting corrupts otherwise good question content. The quality of the question and the correctness of the format should be independently verifiable.

---

## Proposed Pipeline Architecture

```
Source files
    │
    ▼
[Agent 1: Inventory]
    │  Output: concept list with metadata (Markdown table)
    ▼
[Agent 2: Generation]  ◄── one subcategory at a time
    │  Output: intermediate format (see options below)
    ▼
[Editor v3: Manual Validation]  ◄── human review step (mandatory)
    │  Human marks questions Lista / Revisar / Pendiente
    │  Human edits text, removes weak distractors
    ▼
[Agent 3: Export]  (or script)
    │  Output: Moodle XML, only "Lista" questions
    ▼
Moodle import
```

### Why the Editor is a Mandatory Step (Not Optional)

The editor is not a convenience tool. It is the **human-in-the-loop validation gate** that:

- Catches factual errors the adversarial filter couldn't catch (domain errors the model cannot self-detect)
- Selects the best questions when there is redundancy
- Adjusts difficulty and removes culturally biased distractors
- Controls what actually reaches students

The pipeline must be designed around this, not as an afterthought.

---

## Agent Responsibilities

### Agent 1 — Inventory

**Input**: Directory paths from user **Output**: Markdown table with file paths, density classification (🟢 High / 🟡 Medium / 🔴 Low), key concepts per file, and estimated question count **Context requirement**: Medium (reads files, outputs compact summary) **Can be reused**: Yes — same inventory for multiple generation runs

### Agent 2 — Generation

**Input**: Concept list (from Agent 1) + intermediate format template **Output**: Questions in intermediate format (see design options below) **Context requirement**: Small — operates on one subcategory at a time, does not read source files directly **Key constraint**: Must encode adversarial distractor validation (see `docs/adversarial_logic_filters.md` §1 and §6)

### Agent 3 — Export (or script)

**Input**: Editor state (questions marked "Lista") **Output**: Moodle XML file(s) per category **Context requirement**: Minimal — pure format conversion **Implementation**: Could be a deterministic script rather than an LLM agent, since the editor's JSON state already contains all content.

---

## Core Design Decision: Intermediate Format

This is the central open question for the decomposition. The format produced by Agent 2 and consumed by the Editor must balance:

- **Compactness** (token budget during generation)
- **Adversarial filter compatibility** (distractor reasoning must be possible)
- **Editor compatibility** (ideally maps directly to the editor's model)
- **Human readability** (for manual inspection if needed)

The editor's native state format is already defined in `editor/v3/file_io/state_io.py`. The JSON schema it produces and consumes is the reference implementation.

---

### Option A — GIFT (plain, no feedback)

GIFT is Moodle's plain-text import format:

```
::Q001:: What is the purpose of train/test split?{
  =To estimate generalization error on unseen data
  ~To reduce training time
  ~To increase model complexity
  ~To avoid the need for cross-validation
}
```

**Pros:**
- Extremely compact: ~5–8 lines per question (vs. 50–80 for XML)
- Proven to work — earlier experiments showed better results than XML
- Token budget allows ~60–80 questions per output vs. ~15 with XML
- No syntax overhead competing with semantic generation
- Moodle imports GIFT natively

**Cons:**
- No feedback fields — adversarial filter mechanism is lost entirely (see `docs/adversarial_logic_filters.md` §1: feedback is the anchor that forces the model to validate distractors)
- No `source_file` traceability metadata
- Editor cannot import GIFT (would need a new parser)
- 7-option questions need careful GIFT syntax (supported but verbose)

**Verdict**: High throughput, but the quality control regression is a known risk. Suitable only if a separate validation pass compensates.

---

### Option B — GIFT + Reasoning Block (custom hybrid)

Generate GIFT syntax for the question, followed by a structured reasoning block per distractor that gets **stripped before import**:

```
::Q001:: What is the purpose of train/test split?{
  =To estimate generalization error on unseen data
  ~To reduce training time
  ~To increase model complexity
  ~To avoid the need for cross-validation
}

<!-- VALIDATION
  distractor "To reduce training time":
    False because: training time is irrelevant to the split's purpose.
    Confidence: HIGH — unambiguously wrong.
  distractor "To increase model complexity":
    False because: split does not affect model architecture.
    Confidence: HIGH.
  distractor "To avoid the need for cross-validation":
    False because: split and CV are complementary, not alternatives.
    Confidence: MEDIUM — a student might confuse hold-out vs. CV.
    Action: KEEP — the confusion is pedagogically relevant.
-->
```

**Pros:**
- Preserves the adversarial filter (reasoning forces distractor validation)
- Compact enough: ~20–30 lines per question
- Reasoning block is human-readable for inspection
- GIFT part can be imported directly after stripping comments
- Confidence flagging gives the human editor prioritized review targets

**Cons:**
- Non-standard format requiring a custom stripper/parser
- The reasoning block is not stored in the editor — traceability lost after import
- GIFT still not importable by editor natively

---

### Option C — JSON (editor-native format)

Generate JSON matching the editor's `state_io.py` schema directly:

```json
{
  "version": "1.0",
  "questions": [
    {
      "id": "auto",
      "name": "Q001: Purpose of train/test split",
      "question_text": "What is the primary purpose of splitting data...",
      "general_feedback": "The train/test split estimates...",
      "category_path": "$course$/ML/Evaluation",
      "status": "pendiente",
      "source_file": "02_model_evaluation.md",
      "answers": [
        {"text": "To estimate generalization error on unseen data", "fraction": "100", "feedback": "Correct. The split..."},
        {"text": "To reduce training time", "fraction": "-50", "feedback": "Incorrect. Training time..."},
        ...
      ]
    }
  ]
}
```

**Pros:**
- **Direct editor import** — zero conversion step, generated file opens in editor immediately with `Ctrl+O`
- All fields preserved: feedback, source traceability, status, category
- Adversarial filter fully operational (feedback field forces reasoning)
- Clean structure — the model only fills content, not formatting
- Versioned schema means future editor improvements are backward compatible
- Export to Moodle XML is already implemented in `file_io/xml_writer.py`

**Cons:**
- More verbose than GIFT (but less than Moodle XML): ~25–35 lines/question with feedback, ~10–15 without
- JSON syntax errors would corrupt the entire output batch
- Feedback fields (full reasoning per distractor) are still verbose

**Variant C1 — JSON without feedback fields (generation pass only)**:

Omit `feedback` from answers during generation; add feedback in a separate pass or in the editor. This reduces to ~10–15 lines/question.

- Adversarial filter must be implemented differently: the instruction would ask the model to reason internally and only keep distractors it can silently justify, without writing the justification. This is weaker than the current mechanism but may be sufficient with reasoning models (see `docs/adversarial_logic_filters.md` §6).

---

### Option D — Two-Pass XML

**Pass 1**: Generate Moodle XML without feedback fields (~20–25 lines/question). **Pass 2**: For each question, generate feedback fields separately and merge.

**Pros:**
- Final output is already valid Moodle XML — no export step
- Adversarial filter deferred to Pass 2 where context is smaller

**Cons:**
- Two LLM calls per batch — cost and latency doubles
- Requires a merge script to recombine passes
- Still verbose compared to JSON or GIFT
- XML syntax errors in either pass corrupt the question
- Does not improve editor integration

**Verdict**: High complexity for modest benefit. Only worthwhile if Moodle XML is the mandatory intermediate (e.g., for third-party tooling).

---

## Comparison Matrix

| Criterion | A: GIFT | B: GIFT+Reasoning | C: JSON | C1: JSON no-feedback | D: Two-pass XML |
|-----------|---------|------------------|---------|----------------------|-----------------|
| Lines/question | ~7 | ~25 | ~30 | ~12 | ~45 |
| Questions/batch | ~70 | ~30 | ~25 | ~60 | ~10 |
| Adversarial filter | ✗ None | ✓ Full | ✓ Full | △ Implicit | ✓ Deferred |
| Editor import | ✗ New parser | ✗ Strip+parse | ✓ Native | ✓ Native | ✗ No |
| Human-readable | ✓✓ | ✓✓ | ✓ | ✓ | △ |
| Moodle import | ✓ Direct | ✓ After strip | ✗ Via editor export | ✗ Via editor export | ✓ Direct |
| Source traceability | ✗ | ✗ | ✓ | ✓ | △ |
| Implementation effort | Low | Medium | Low (schema exists) | Low | High |

---

## Recommendation Rationale

**Option C1 (JSON without feedback, reasoning models)** is likely the best starting point because:

1. The editor import is native — no new parser needed.
2. Token budget (~60 questions/batch) comparable to GIFT.
3. With current reasoning models (Gemini 3, Claude 4.5, GPT 5.2), the adversarial filter can be applied implicitly: instruct the model that it must be able to justify each distractor's falseness internally, and to discard any it cannot. This uses the model's internal CoT rather than requiring explicit output (see `docs/adversarial_logic_filters.md` §6 — "Functional Output Constraint").
4. Feedback can optionally be added as a second pass only for questions the human marks "Lista" in the editor — deferring verbose generation to a smaller, focused batch.

**Option B (GIFT + reasoning)** is the best fallback if implicit reasoning is insufficient — it restores the explicit adversarial filter while keeping output compact, at the cost of a custom stripper.

**Option A (plain GIFT)** should be tested empirically first as a baseline, given that it produced better results historically. If quality is acceptable without explicit feedback, the simpler pipeline wins.

---

## Action Items for Decomposition (Ordered by Priority)

1. **Baseline experiment**: Run Agent 2 as plain GIFT (Option A) on a known topic. Compare distractor quality against an XML run. This is cheap to test and may close the debate.
2. **Decide on intermediate format** based on experiment results.
3. **Implement Agent 1** (Inventory): Extract from current `generate-test.prompt.md` FASE PREVIA section. Small, self-contained.
4. **Implement Agent 2** (Generation): New prompt for chosen format, operating on one subcategory at a time. Move adversarial filter instructions from current prompt.
5. **Implement Export Agent or script** (`resources/`): If JSON is chosen, a deterministic Python script using the existing `xml_writer.py` is preferable to an LLM call.
6. **Update editor** if needed: Add import support for chosen format if not JSON (Option A or B).
7. **Update this document** with the chosen format and link to the implemented agents.

---

## Files To Create (Pending)

| File | Description |
|------|-------------|
| `prompts/inventory.prompt.md` | Agent 1: source file inventory and concept extraction |
| `prompts/generate-questions.prompt.md` | Agent 2: question generation in chosen format |
| `prompts/export.prompt.md` OR `resources/json_to_moodle_xml.py` | Agent 3 / export script |
