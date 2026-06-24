# Stem Design Rules

How to write the question stem (`question_text`). Part of the [Question Rules](../questions_rules.md) module set.

## 1. Direct and open by default

Prefer direct, open stems over framings that pre-decide the answer. Ask *what* something is and *why*, not *why* a conclusion you already stated holds.

- ❌ `¿Por qué logistic regression se considera un modelo de clasificación aunque su nombre contenga la palabra regression?`
- ✅ `¿Qué tipo de modelo de IA es logistic regression y por qué?`

## 2. Do not leak the answer in the stem

The stem must not state or strongly imply the very fact being tested. Giving the classification away makes the correct option trivially identifiable and turns distractors into throwaways.

- ❌ `Una noticia puede etiquetarse simultáneamente como "economía", "energía" y "política internacional". ¿Por qué esta tarea encaja mejor con multilabel classification que con multiclass classification?`
- ✅ `Una noticia puede pertenecer a varias categorías temáticas a la vez. ¿Qué tipo de problema de clasificación lo describe y por qué?`

## 3. Do not presume the conclusion

Avoid stems that assume the proposition under test is true (e.g. "¿Por qué X *puede ser preferible*…?"). Such framing lets the student discard any option that disagrees, regardless of its reasoning.

- ❌ `¿Por qué una excepción personalizada puede ser preferible a una genérica cuando falla una regla de negocio?`
- ✅ `Cuando falla una regla de negocio, ¿qué diferencia hay entre lanzar una excepción personalizada y una genérica?`

## 4. Self-contained

Stems must stand on their own. Never reference "el material", "las notas", "el cuaderno", slides, or source files, implicitly or explicitly. Embed any needed fact directly. Stems may be as long as necessary to be self-contained.

## 5. One coherent target per question

Do not bundle several concepts that have no mutual relationship relevant to what is asked. If the relationship between the concepts is not the point, split into separate questions.

- ❌ `¿Qué combinación describe mejor cómo kernel size, stride, padding y pooling afectan la salida espacial de una CNN?`
- ❌ `¿Por qué dataloaders, mini-batches y device consistency importan en el entrenamiento práctico de redes neuronales?`

If a stem cites several elements (e.g. "optimizer choice, regularization, and learning-rate scheduling"), every option must engage all of them — see [distractor-design.md](distractor-design.md) §4.

## 6. No graded / comparative-superlative framing

Avoid "¿Qué … describe **mejor**…?", "¿Qué comparación describe mejor…?", "más apropiada", and similar graduated wording. It implies options differ by degree rather than being true/false, which contradicts the rule that every distractor is manifestly wrong. Use direct phrasing instead.

## 7. "Por qué" ⇒ "Porque"

If the stem begins with "¿Por qué…?", every option (correct and distractors) should be a hypothesis beginning with "Porque…", so distractors are genuine candidate answers in the same rhetorical form rather than non-answers.
