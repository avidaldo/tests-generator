# Anti-Bias Rules

Surface cues must not reveal the key. Part of the [Question Rules](../questions_rules.md) module set.
Apply these checks before finalizing each question.

1. **Length bias.** Compare normalized visible option text (ignore HTML wrappers/tags). If the correct answer is uniquely longest or shortest by a clear margin, rebalance.
2. **Structural bias.** Keep options similar in grammatical structure and specificity. Avoid a "3 similar + 1 odd one" shape.
3. **Position bias.** Shuffle the correct-answer position across questions; avoid predictable placement.
4. **Triviality bias.** Avoid superficial "best definition" wording that tests vocabulary matching instead of understanding.
5. **Absurdity bias.** Every distractor must remain plausible under partial knowledge; none should be discardable at a glance.

> The editor flags length imbalance automatically (`editor/models/question_diagnostics.py`), but structural, position, triviality, and absurdity checks are the author's responsibility.
