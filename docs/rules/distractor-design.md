# Distractor Design Rules

How to write the incorrect options. Part of the [Question Rules](../questions_rules.md) module set.
See also the psychometric strategy catalog in [distractor_design.md](../distractor_design.md).

## 1. Manifestly wrong, never "less correct"

Every distractor must be unambiguously false to someone who understands the concept, while still looking plausible to someone who does not. A distractor must never be merely a worse-but-defensible answer than the key. If two options could both be argued correct, the item is broken.

## 2. A genuine answer to the question, in the same form

Each distractor must actually answer what the stem asks, in the same rhetorical register as the key. A "Por qué…?" stem needs "Porque…" distractors (see [stem-design.md](stem-design.md) §7). Options that simply fail to address the question are weak and easily discarded.

- Stem: `¿Por qué una excepción personalizada puede ser preferible…?`
- ❌ `Una excepción genérica basta porque las capas superiores solo necesitan saber que la operación falló…` (does not answer in the stem's "porque preferible" frame; trivially discardable)

## 3. Never contradict what the stem states or implies

A distractor must not deny any fact the stem asserts or logically entails. Distractors may **ignore** information or answer incompletely, but they may **never contradict** the premise — that makes them eliminable by pure logic, not by understanding.

- Stem asserts Python is *híbrido* → ❌ `Python debe considerarse completamente compilado…`
- Stem asserts the definition *genera un error de sintaxis* → ❌ `No hay error; esta definición es válida…`
- Stem asks why a random forest is *menos interpretable* → ❌ `El random forest ofrece una interpretabilidad muy superior…`

## 4. No lazy partial-element distractors

When the stem cites several elements as distinct levers, a distractor that silently collapses or ignores one of them is usually obviously wrong and signals lazy design. Engage all cited elements.

- Stem distinguishes optimizer choice, regularization, and learning-rate scheduling →
  ❌ `Regularization y scheduling son equivalentes; ambos solo cambian el número de épocas.`

## 5. Strategy variety

Use varied distractor strategies across and within a batch (Procedural False Positive, Causal Confusion, Intuitive Attractor, Concept Blend, Semantic Inversion). Do not rely on a single pattern. Keep option structure, length, and specificity comparable across the four — see [anti-bias.md](anti-bias.md).

## 6. Adversarial feedback is mandatory

For every distractor, write feedback that unambiguously explains *why it is false*. If the explanation needs hedging ("almost true", "not the best"), the distractor is ambiguous — replace it. This is the practical hard gate (see [Question Rules §6](../questions_rules.md)).
