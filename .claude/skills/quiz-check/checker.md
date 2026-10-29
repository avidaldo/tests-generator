# Checker instructions

## For both passes

You check multiple-choice quiz items in Spanish, written for students of a vocational AI course (FP de Grado Superior: junior developers, not researchers). You did not write them. Your job is to find what is wrong with each item, not to defend or fix it. The rules and their IDs are those of `docs/item-rules.md`; read that page once before you start.

- Read only the files your task names, and check only the items it names.
- Write every `why` as one short sentence in Spanish that names the concrete words or idea behind your judgement.
- Write exactly one JSON file, at the path your task gives, following the skeleton of your pass; then reply with one line.

## Steps A and B

Your input is a key-less view (`blind_view`). For each item it gives its number `n`, its `id`, the `stem`, the `options` under letters and, when the item has them, `evidence` quotes from the course material. Nothing tells you which option is correct, and you must not look for it elsewhere. Finish step A for an item before you start its step B.

### Step A: the wording alone

Picture a test-wise student who has not studied this topic. Using only the wording, never what you know about the subject, decide what this student would do.

`eliminated` lists each option the student would discard, with the cue that gives it away:

- DIS-STEM: it contradicts something the stem states or implies.
- DIS-ANSWERS: it doesn't answer the question asked, or answers in another form (a "¿Por qué…?" answered without "Porque", a definition where a consequence is asked, "todas las anteriores").
- DIS-TOPIC: it brings in a term from another topic.
- DIS-ELEMENTS: it leaves out one of the elements the stem names.
- DIS-ABSURD: it reads as a joke, a strawman or a random mix of technical terms.
- DIS-LOADED: an adjective marks it as wrong ("enorme", "caótico").
- DIS-ABSOLUTE: an absolute ("siempre", "nunca", "solo") singles it out among options that have none.
- OPT-PARALLEL: it is the odd one in structure, length class, specificity or register.
- OPT-PAIR: two other options contradict each other, so the student keeps that pair and discards the rest; report each discarded option.

`picked` is the option the student would choose from the wording alone, with its cue, or `null` when no cue points anywhere: KEY-LENGTH (the longest or most detailed), KEY-ECHO (it repeats the stem's words), OPT-PARALLEL (the only one built differently).

You know the subject, so you will be tempted to eliminate options because they are false. That belongs to step B. Report a cue only when it is one of the above and a student without the knowledge could act on it; when in doubt, leave it out.

### Step B: solve with the source

Now answer the item as a knowledgeable teacher would, from the evidence when the item has it and from what you know when it doesn't.

- `answer`: the letter of the correct option, or `null` when the item as written has no single correct option.
- `confidence`: `high`, `medium` or `low`.
- `why`: why that option is correct.
- `defensible`: every other option that a competent teacher could defend as correct for the stem as written, each with the argument. An option is defensible when a reasonable reading of the stem makes it true, including when it is true but less complete than yours; it is not defensible merely because it mentions related ideas.

### Skeleton of steps A and B

```json
{
  "artifact_type": "blind_checks",
  "version": "1.0",
  "items": [
    {
      "n": 0,
      "id": "ID_FROM_THE_VIEW",
      "form": {"eliminated": [{"option": "c", "rule": "DIS-TOPIC", "why": "..."}], "picked": null},
      "solve": {"answer": "b", "confidence": "high", "why": "...", "defensible": [{"option": "d", "why": "..."}]}
    }
  ]
}
```

## Step C

Your input is the question file itself and its lint report (`qb lint --json`). Now you see everything: the key (fraction 100), every feedback, and in items from the current pipeline the reasoning fields (`evidence`, `claim`, `stem_premises`, `why_right`, each distractor's `misconception` and `why_wrong`). Items written before that pipeline lack the reasoning fields: infer the claim and each distractor's belief from the text, and apply the same rules. Each item you audit already carries `checks.blind` (steps A and B, options as answer indices counted from 0) and `checks.failed`, the failures they imply. An item's `n` is its position in the file's `questions` array, counted from 0.

For each item:

1. **`findings`**: every break of a rule tested in step C, with the option's `answer_index`, or `null` when it concerns the whole item. You may also report a step A rule that step A missed. Don't repeat what the lint report or `checks.failed` already record. How to judge the less obvious ones:
   - GROUND-SUPPORT: compare the claim, `why_right` and each `why_wrong` with the evidence. Without evidence, report it when the key's justification or a refutation is false.
   - STEM-CLAIM and STEM-OPEN: ask what the stem takes for granted. If that is the claim being tested, even paraphrased, it fails.
   - DIS-BELIEF: would a student who holds the stated belief really give this answer, and do these students plausibly hold it? In a numeric item, can the wrong value be reproduced from a named slip?
   - FB-MATCH: read each feedback against its own option; feedback copied from an earlier version of the option is the usual failure.
   - LANG-GLOSSARY: when your task names a glossary, follow it; otherwise check only that each concept has one term across the options and that English terms are in italics.
2. **`options`**: one decision per distractor, that is, per answer that isn't the key. `drop` every distractor with an error-level failure in `checks.failed` or in your findings; `keep` the others. When more than three distractors are kept, mark the weakest of them `spare`, never more than one.
3. **`verdict`**: `accept` when the item, with the distractors you keep, breaks no error-level rule and keeps three distractors; `repair` when rewriting some parts would fix it; `reject` when the claim itself is wrong, untestable or not worth testing. With `repair`, say in `repair` what to rewrite and why, citing rule IDs, and only the parts that fail.

Steps A and B are binding: you can't keep a distractor they failed, and the item can't be accepted while the blind solver missed the key. If you think one of their failures is wrong, write `disputed: RULE option N - why` in `repair` and give the verdict `repair`; the teacher decides.

### Skeleton of step C

```json
{
  "artifact_type": "audit_checks",
  "version": "1.0",
  "items": [
    {
      "n": 0,
      "id": "ID_FROM_THE_FILE",
      "findings": [{"rule": "FB-MATCH", "answer_index": 2, "why": "..."}],
      "options": [
        {"answer_index": 1, "decision": "keep", "why": "..."},
        {"answer_index": 2, "decision": "drop", "why": "..."},
        {"answer_index": 3, "decision": "keep", "why": "..."}
      ],
      "verdict": "repair",
      "repair": "..."
    }
  ]
}
```
