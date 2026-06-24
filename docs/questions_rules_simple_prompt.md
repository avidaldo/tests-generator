# Question Rules (Stage 3)

1. Review and generate questions only from the provided Stage 2 subcategory file.
2. Do not inject external knowledge beyond that file.
3. Achieve complete coverage os stage 2 outputs. Use subagents as necessary to avoid context drift.

## Mandatory Structural Constraints

Every question must satisfy all of the following:

- Master's level (EQF Level 7) cognitive demand.
- Exactly 7 answer options:
  - 1 correct answer (`fraction: "100"`)
  - 6 distractors (`fraction: "-50"`)
- `answers[].feedback` is mandatory for all 7 options.
- `status` must be `"pending"`.
- JSON must follow the editor schema and omit editor-populated fields (`default_grade`, `penalty`, `single`, `shuffle_answers`, `answer_numbering`, `correct_feedback`, `partially_correct_feedback`, `incorrect_feedback`).

## Stem & Distractor Anti-Patterns (hard rejection)

Regenerate any question that hits these (full detail: [questions_rules.md](questions_rules.md) and [rules/](rules/)):

- Stem leaks the answer or presumes its conclusion ("¿Por qué X *puede ser preferible*…?"). Ask "what … and why?" instead.
- Stem bundles unrelated concepts whose relationship is not what is tested (kernel/stride/padding/pooling; dataloaders/mini-batches/device-consistency). Split them.
- Stem uses graded/superlative framing ("¿Qué … describe **mejor**…?", "más apropiada"). Use direct phrasing.
- A distractor contradicts a fact the stem states or implies (stem says *híbrido* → distractor says *completamente compilado*). Distractors may ignore info, never contradict it.
- A distractor is a lazy partial-element answer, a non-answer, childish/strawman, or merely "less correct" than the key.
- "¿Por qué…?" stems: every option must begin "Porque…".
- Avoid "y confiar en que…" and loaded adjectives ("enorme", "confuso") that tell which option is wrong.

## Content and Cognitive Rules

Default to direct stems for definitions, distinctions, taxonomy, hierarchy, and misconception correction.

Use scenarios only when concrete context materially changes reasoning, diagnosis, trade-off, or procedure selection. Remove decorative wrappers (named speakers, classroom narratives, debate framing) when they do not change the tested logic.

Balance coverage across definitions, procedures, comparisons, scenarios, misconceptions, diagnostics, and cross-subcategory interactions (when available).

If two drafts test almost the same thing, keep the stronger one and replace the weaker with a different surface.

The following fields must be self-contained:

- `question_text`
- `general_feedback`
- `answers[].feedback`

Do not use learner-facing external anchors such as:

- `según el material`, `según las notas`, `según el cuaderno`, `del material`
- `according to the material`, `according to the notes`, `the material`, `in the notebook`
- equivalent references to slides, notebooks, class notes, or source files

If any such phrasing appears, rewrite by embedding the needed fact directly in the field.

## Distractor Design Rules

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

## Adversarial Validation Rules (Hard Gate)

Every distractor must pass adversarial validation:

1. Write explicit feedback that unambiguously explains why the distractor is false.
2. If feedback requires hedging (“almost true”, “not the best”), treat the distractor as ambiguous and replace it.
3. Correct-option feedback must explain why it is correct, not only restate the option.

This is the practical adversarial filter: weak falseness explanations signal weak distractors and must trigger regeneration.

## Anti-Bias Rules

Apply anti-bias checks before finalizing each question:

1. **Length bias**: Compare normalized visible option text (ignore HTML wrappers/tags). If the correct answer is uniquely longest/shortest by a clear margin, rebalance.
2. **Structural bias**: Keep options similar in grammatical structure and specificity.
3. **Position bias**: Shuffle correct-answer position across questions; avoid predictable placement.
4. **Triviality bias**: Avoid superficial “best definition” wording that tests vocabulary matching instead of understanding.
5. **Absurdity bias**: Every distractor must remain plausible under partial knowledge.


Do not keep a stylistically elegant item that fails adversarial clarity or conceptual correctness.