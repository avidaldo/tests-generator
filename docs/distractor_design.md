# Distractor Design & Psychometric Techniques

This document is the knowledge base for distractor (incorrect answer) design in multiple-choice questions. It is referenced automatically by the question generation prompt via `.github/instructions/question-design.instructions.md`.

For the adversarial filter mechanism that *validates* distractors after design, see [adversarial_logic_filters.md](adversarial_logic_filters.md) §1.

---

## 1. Distractor Strategies

Use variety across questions — do not rely on a single strategy for all distractors within a question or across questions.

### Procedural False Positive
The correct outcome described with an incorrect method or reasoning path. The student who memorised the result but not the process will select it.

*Example*: "Normalisation scales values to [0,1]" — correct result, but the explanation attributes it to standardisation (z-score), which actually centres around 0 with unit variance.

### Causal Confusion
Inverts the cause-effect relationship between two concepts. Exploits students who recognise both concepts but confuse the direction of dependency.

*Example*: "Overfitting causes high variance" inverted to "High variance causes overfitting."

### Intuitive Attractor
An answer that sounds like "common sense" but is technically false. Exploits the gap between everyday intuition and domain-specific precision.

*Example*: "More training data always improves model performance" — intuitive but false (e.g., label noise, class imbalance, irrelevant features).

### Concept Blend
Confuses two related but distinct terms or definitions. Targets students who have surface-level familiarity with both concepts but haven't internalised the boundary.

*Example*: Blending "precision" and "recall" — e.g., defining precision using the recall formula.

### Semantic Inversion
Changes a single conceptual axis of the correct answer (e.g., increases↔decreases, always↔never, necessary↔sufficient). The distractor is structurally identical to the correct answer except for one inverted claim.

*Example*: "Increasing regularisation strength *increases* model complexity" — correct answer says *decreases*.

---

## 2. Scenario Triangulation

Instead of asking "What is X?" (atomicity → recall/memorisation), design questions that require **triangulation**: "What happens to X if we change Y given context Z?"

This forces the student to simulate a mental model where variables interact, testing deep comprehension rather than definition recall.

**Levels of triangulation:**

| Level | Pattern | Cognitive demand |
|-------|---------|-----------------|
| 1-axis | "What is X?" | Recall |
| 2-axis | "What happens to X when Y changes?" | Comprehension |
| 3-axis | "Given context Z, what happens to X when Y changes?" | Analysis |
| Comparative | "When is X better than Y, and why?" | Evaluation |

Aim for 2-axis or higher in all questions. 1-axis questions are acceptable only when the concept itself is subtle enough that precise definition *is* the challenge.

---

## 3. Anti-Bias Rules

LLM-generated multiple-choice questions exhibit systematic statistical biases. These must be actively countered:

### Length Bias
The correct answer must NOT be systematically longer or shorter than distractors. When the correct answer requires a detailed explanation, make distractors equally detailed. When it's brief, keep distractors brief.

### Structural Bias
Avoid the pattern of 3 similar options + 1 obviously different one. All 7 options should have comparable structure, vocabulary level, and specificity.

### Position Bias
Shuffle the correct answer position across questions. Do not place it first or last consistently. LLMs tend to put the correct answer first — actively counteract this.

### Triviality Bias
Avoid questions of the type "Which is the best definition?" — these test vocabulary matching, not understanding. Every option should sound like a plausible definition; the question should test whether the student understands the *implications* of the definition.

### Absurdity Bias
All distractors must be plausible to a student with partial knowledge. No filler options that any student would immediately dismiss. If you can't make 6 plausible distractors for a concept, the concept may not support a 7-option question — reduce to fewer options or combine with a related concept.

---

## 4. Item Quality Indicators

*(Placeholder for future psychometric research expansion)*

- **Discrimination index**: How well the item separates high-performing from low-performing students.
- **Difficulty index**: Proportion of students answering correctly — aim for 0.3–0.7 for discriminating items.
- **Distractor analysis**: Each distractor should be selected by at least some students. Unused distractors indicate poor design.
- **Point-biserial correlation**: Correlation between item score and total test score — positive for correct answer, negative for distractors.

---

## References

- [Adversarial Filters & Prompting Techniques](adversarial_logic_filters.md) — the self-correction mechanism that validates distractors during generation
