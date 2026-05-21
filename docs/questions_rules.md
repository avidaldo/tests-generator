# Question Rules (Stage 3)

This document consolidates the mandatory rules that generated questions must follow in Stage 3 (`prompts/generate-questions.prompt.md`), integrating the adversarial validation and distractor design guidance from:

- [prompts/generate-questions.prompt.md](../prompts/generate-questions.prompt.md)
- [docs/adversarial_logic_filters.md](adversarial_logic_filters.md)
- [docs/distractor_design.md](distractor_design.md)

Use this as an operational checklist for writing, reviewing, or rejecting question batches.

---

## 1) Scope and Source Discipline

1. Generate questions only from the provided Stage 2 subcategory file.
2. Do not inject external knowledge beyond that file.
3. Use `SURF-*` entries as primary coverage units when they exist.
4. Keep source traceability in `source_ref`; learner-facing fields must stand on their own without referring to notes or source files.

---

## 2) Mandatory Structural Constraints

Every question must satisfy all of the following:

- Master's level (EQF Level 7) cognitive demand.
- Exactly 7 answer options:
  - 1 correct answer (`fraction: "100"`)
  - 6 distractors (`fraction: "-50"`)
- `answers[].feedback` is mandatory for all 7 options.
- `status` must be `"pendiente"`.
- JSON must follow the editor schema and omit editor-populated fields (`default_grade`, `penalty`, `single`, `shuffle_answers`, `answer_numbering`, `correct_feedback`, `partially_correct_feedback`, `incorrect_feedback`).

Batch constraints:

- Maximum 20 questions per file.
- Never overwrite existing batch files unless explicitly requested.

---

## 3) Content and Cognitive Rules

### 3.1 Conceptual Focus

When `Question focus` is `conceptual-only` (default):

- Test conceptual understanding, procedures, relationships, trade-offs, diagnosis, and interpretation.
- Code may appear only as context illustration.
- Do **not** test syntax recall, API parameter names, library implementation trivia, or answers that are code lines.

When `Question focus` is `syntax-included`:

- Include syntax/API/implementation questions in addition to conceptual ones (not as a replacement).

### 3.2 Directness vs. Scenario Use

Default to direct stems for definitions, distinctions, taxonomy, hierarchy, and misconception correction.

Use scenarios only when concrete context materially changes reasoning, diagnosis, trade-off, or procedure selection. Remove decorative wrappers (named speakers, classroom narratives, debate framing) when they do not change the tested logic.

### 3.3 Coverage Diversity

Within each batch, avoid narrow repetition:

- Prefer one strong item per selected `SURF-*` before adding a second item for the same surface.
- Balance coverage across definitions, procedures, comparisons, scenarios, misconceptions, diagnostics, and cross-subcategory interactions (when available).
- If two drafts test almost the same thing, keep the stronger one and replace the weaker with a different surface.

---

## 4) Learner-Facing Text Rules

The following fields must be self-contained:

- `question_text`
- `general_feedback`
- `answers[].feedback`

Do not use learner-facing external anchors such as:

- `según el material`, `según las notas`, `según el cuaderno`, `del material`
- `according to the material`, `according to the notes`, `the material`, `in the notebook`
- equivalent references to slides, notebooks, class notes, or source files

If any such phrasing appears, rewrite by embedding the needed fact directly in the field.

---

## 5) Distractor Design Rules

Distractors must be plausible and diagnostically useful, not filler.

Use varied distractor strategies across and within questions:

- Procedural False Positive
- Causal Confusion
- Intuitive Attractor
- Concept Blend
- Semantic Inversion

Do not rely on a single distractor pattern across a batch.

Plausibility constraints:

- Avoid absurd distractors that a partially informed student would instantly discard.
- Keep option structure and specificity comparable.
- Do not create a “3 similar + 1 odd one” style pattern (extended here to the 7-option format).

---

## 6) Adversarial Validation Rules (Hard Gate)

Every distractor must pass adversarial validation:

1. Write explicit feedback that unambiguously explains why the distractor is false.
2. If feedback requires hedging (“almost true”, “not the best”), treat the distractor as ambiguous and replace it.
3. Correct-option feedback must explain why it is correct, not only restate the option.

This is the practical adversarial filter: weak falseness explanations signal weak distractors and must trigger regeneration.

---

## 7) Anti-Bias Rules

Apply anti-bias checks before finalizing each question:

1. **Length bias**: Compare normalized visible option text (ignore HTML wrappers/tags). If the correct answer is uniquely longest/shortest by a clear margin, rebalance.
2. **Structural bias**: Keep options similar in grammatical structure and specificity.
3. **Position bias**: Shuffle correct-answer position across questions; avoid predictable placement.
4. **Triviality bias**: Avoid superficial “best definition” wording that tests vocabulary matching instead of understanding.
5. **Absurdity bias**: Every distractor must remain plausible under partial knowledge.

---

## 8) Pre-Release Quality Checklist

Reject a question or batch if any item fails one or more checks below:

- [ ] Maps to one or more concept IDs in `source_ref`.
- [ ] Tests understanding rather than superficial recall (for conceptual-only mode).
- [ ] Uses direct stem unless scenario context is materially required.
- [ ] Contains 7 options with valid fractions and mandatory feedback.
- [ ] Includes self-contained learner-facing text with no external-material anchors.
- [ ] Uses plausible, varied distractors.
- [ ] Passes adversarial validation (clear falseness explanations for all distractors).
- [ ] Passes option-length and structure bias checks.
- [ ] Contributes non-redundant coverage of selected `SURF-*` surfaces.

---

## 9) Priority Order for Conflict Resolution

If constraints compete, apply this order:

1. Structural validity (schema, option counts, required fields)
2. Conceptual correctness and source-boundedness
3. Adversarial clarity of distractor falseness
4. Anti-bias balancing
5. Style/narrative polish

Do not keep a stylistically elegant item that fails adversarial clarity or conceptual correctness.
