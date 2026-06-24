# Question Rules (Stage 3)

Operational rules that generated questions must follow in Stage 3 (`prompts/generate-questions.prompt.md`). The detailed, frequently-edited guidance is split into focused modules under [`docs/rules/`](rules/) for maintainability; this file is the index plus the cross-cutting hard rules.

## Rule modules

- [rules/stem-design.md](rules/stem-design.md) — how to phrase the stem: direct/open, self-contained, no leaked answer, no presumed conclusion, one coherent target, no graded "mejor" wording, "Por qué" ⇒ "Porque".
- [rules/distractor-design.md](rules/distractor-design.md) — manifestly wrong yet plausible, a genuine answer in the same form, never contradicting the stem, no lazy partial-element distractors, strategy variety.
- [rules/anti-bias.md](rules/anti-bias.md) — length, structure, position, triviality, and absurdity checks.
- [rules/register-and-tone.md](rules/register-and-tone.md) — clarity over ornate formality, no "confiar en que…", no loaded adjectives, no childish distractors.

Supporting background: [distractor_design.md](distractor_design.md) (psychometric strategies) and [adversarial_logic_filters.md](adversarial_logic_filters.md) (adversarial filter mechanism).

---

## 1. Scope and source discipline

1. Generate questions only from the provided Stage 2 subcategory file.
2. Do not inject external knowledge beyond that file.
3. Use `SURF-*` entries as primary coverage units when they exist.
4. Keep source traceability in `source_ref`; learner-facing fields (`question_text`, `general_feedback`, `answers[].feedback`) must stand on their own.

## 2. Mandatory structural constraints

- Master's level (EQF Level 7) cognitive demand.
- Exactly 7 answer options: 1 correct (`fraction: "100"`) + 6 distractors (`fraction: "-50"`).
- `answers[].feedback` is mandatory for all 7 options.
- `status` must be `"pending"`.
- JSON follows the editor schema and omits editor-populated fields (`default_grade`, `penalty`, `single`, `shuffle_answers`, `answer_numbering`, `correct_feedback`, `partially_correct_feedback`, `incorrect_feedback`).
- Max 20 questions per file; never overwrite existing batch files unless explicitly requested.

> Stage 3 starts with 6 distractors so the Stage 4 reviewer can prune weak ones down to a final 3.

## 3. Adversarial validation (hard gate)

Every distractor must pass adversarial validation:

1. Write explicit feedback that unambiguously explains why the distractor is false.
2. If the feedback needs hedging ("almost true", "not the best"), the distractor is ambiguous — replace it.
3. Correct-option feedback must explain *why* it is correct, not merely restate it.

Weak falseness explanations signal weak distractors and must trigger regeneration.

## 4. Pre-release quality checklist

Reject a question or batch if any check fails:

- [ ] Maps to one or more concept IDs in `source_ref`.
- [ ] Tests understanding, not superficial recall (conceptual-only mode).
- [ ] Direct stem unless scenario context is materially required ([stem-design.md](rules/stem-design.md)).
- [ ] Stem does not leak the answer or presume the conclusion ([stem-design.md](rules/stem-design.md) §2–§3).
- [ ] Single coherent target; unrelated concepts are not bundled ([stem-design.md](rules/stem-design.md) §5).
- [ ] 7 options with valid fractions and mandatory feedback.
- [ ] Self-contained learner-facing text, no external-material anchors.
- [ ] No distractor contradicts the stem; none is a lazy partial-element or non-answer ([distractor-design.md](rules/distractor-design.md) §2–§4).
- [ ] Plausible, varied distractors; passes adversarial validation.
- [ ] Passes length/structure/position/triviality/absurdity checks ([anti-bias.md](rules/anti-bias.md)).
- [ ] Register and tone consistent; no graded "mejor" wording, no "confiar en que…", no childish distractors ([register-and-tone.md](rules/register-and-tone.md)).
- [ ] Contributes non-redundant coverage of selected `SURF-*` surfaces.

## 5. Priority order for conflict resolution

1. Structural validity (schema, option counts, required fields)
2. Conceptual correctness and source-boundedness
3. Adversarial clarity of distractor falseness
4. Anti-bias balancing
5. Style / narrative polish

Do not keep a stylistically elegant item that fails adversarial clarity or conceptual correctness.
