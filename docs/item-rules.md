# Item rules

The rules every quiz item must meet, each with a stable ID. The writer follows them, `qb lint` and the checker test them, and review notes cite them with the option's number as the editor shows it (`DIS-TOPIC 3`: "Respuesta 3" breaks DIS-TOPIC). This is the only rule page: when a rule changes, it changes here.

Each entry reads `ID · test · severity — rule`:

- **Test:** `lint` is `qb lint`, code run on every item. The checker answers in three steps: `A` without the key, from the wording alone (what would a test-wise student without the knowledge eliminate or pick?); `B` without the key, solving the item with the source; `C` with the key and the reasoning.
- **Severity:** an `error` fails the item, which goes to repair or is rejected; a `warning` is shown in review and may be accepted.

## The idea behind the rules

An item tests one claim, grounded in a quote from the course material. The key states the claim; each distractor is the answer a student holding one named misconception would give. A good distractor sits between two failures, and the checker tests both sides separately:

- it is **false** to someone who knows the concept: in step B a solver with the source refutes it (DIS-FALSE). Merely less right is not false;
- it is **plausible** to someone who doesn't: in step A nobody can eliminate it from its wording alone (the A rules below).

Feedback is written from the reasoning (`why_right`, `why_wrong`), so it doubles as the proof: a distractor whose feedback can't refute it without hedging is defensible, and the item fails.

## Grounding

- **GROUND-EVIDENCE** · lint · error — Every item quotes its source: at least one `evidence` entry with a `locator` (file and section) and a verbatim `quote` from the material, in the material's language. No quote, no item: the target goes back to the teacher.
- **GROUND-REASONING** · lint · error — The reasoning comes before the text it justifies: a `claim`; the key's `why_right`; for each distractor a `misconception` (the belief, whether it was observed in students or inferred, and where) and its `why_wrong`.
- **GROUND-SUPPORT** · C · error — The claim, the key's justification and every refutation follow from the evidence; nothing rests on knowledge outside the quoted material.

## Stem

- **STEM-ONE** · C · error — The stem asks one question about one claim. Several concepts appear together only when their relationship is what is asked.
- **STEM-CLAIM** · lint + C · error — The stem doesn't state or imply the claim it tests: the claim is not among `stem_premises`. Once the stem gives the claim away, every option that disagrees contradicts the stem and is eliminated by logic alone.
- **STEM-OPEN** · C · error — The stem asks instead of presupposing. "¿Por qué…?" is fine when what it takes for granted is a premise, and wrong when it is the claim under test: ask "¿Qué tipo de modelo es X y por qué?", not "¿Por qué X es un clasificador?".
- **STEM-GRADED** · lint · error — The question asks for the correct option, not the best one: no "mejor", "preferible", "más adecuada / precisa / importante / probable…", "con mayor precisión" or "la principal razón / ventaja…" in the question clause, from "¿" to "?". Comparisons in the scenario are fine. To ask for a choice (an architecture under a budget, the specification that gets a change done), the stem states the conditions (figures, constraints, goal) and asks which option meets them, so each distractor breaks a stated condition. Graded wording tells the student the distractors are partly right, which contradicts DIS-FALSE.
- **STEM-DIRECT** · lint · warning — A student could answer the stem before reading the options. "¿Qué afirmación es correcta sobre X?" and "¿Qué opción describe correctamente…?" turn the item into separate true-or-false statements; ask the question those statements answer.
- **STEM-NEGATIVE** · C · error — The stem asks for what is true, never for the exception ("¿Cuál NO…?", "excepto"): under a negative stem the distractors are true statements and can't come from misconceptions.

## Options

### Key

- **KEY-UNIQUE** · B · error — The key is the only correct option: a solver who has the source but not the key chooses it.
- **KEY-LENGTH** · lint + A · warning — The key is as short as its content allows, and all options stay within about 30% of its length in words. Lint flags a key that is uniquely the longest or shortest option and differs from the median distractor by at least 35% and four words (for options under six words, by 35% and 24 characters). Fix it by shortening the key, not by padding the distractors.
- **KEY-ECHO** · A · error — The key doesn't repeat words of the stem that the distractors lack.

### Distractors

- **DIS-FALSE** · B · error — Each distractor is false, not less right: someone who knows the concept refutes it in one sentence with the evidence. A distractor that can be defended breaks the item.
- **DIS-BELIEF** · C · error — Each distractor is what a student holding its misconception would answer, and that belief is plausible for the course's students. In a numeric item each wrong value comes from a named slip (p·n instead of pⁿ, precision read as recall), not from a random number.
- **DIS-DISTINCT** · C · error — Each distractor comes from a different misconception; no two distractors are wrong for the same reason.
- **DIS-STEM** · A · error — A distractor may ignore part of the stem or fall short, but never contradicts what the stem states or implies.
- **DIS-ANSWERS** · A · error — Every distractor answers the question asked, in the same form as the key, and is a complete answer on its own (no "todas / ninguna de las anteriores").
- **DIS-TOPIC** · A · error — Every distractor stays in the item's topic: its mistake is about the concept being tested, not a term borrowed from another unit.
- **DIS-ELEMENTS** · A · error — When the stem names several elements, every option deals with all of them.
- **DIS-ABSURD** · A · error — Every distractor is a credible technical mistake: no jokes, strawmen or random combinations of technical terms.
- **DIS-LOADED** · lint + A · warning — No adjective marks a distractor as wrong ("enorme", "confuso", "caótico", "absurdo").
- **DIS-ABSOLUTE** · lint + A · warning — Absolutes ("siempre", "nunca", "solo", "automáticamente") don't single out the distractors: lint flags them when they appear in at least half of the distractors and not in the key.

### All options

- **OPT-PARALLEL** · A · error — All options share form, structure, specificity and register; neither the key nor a distractor stands out as the odd one. Numeric options share units and precision.
- **OPT-PAIR** · A · warning — Opposites appear only when the options cover the possible answers (it rises, it falls, it doesn't change). Two options that contradict each other among unrelated ones tell the student that the key is one of the two.
- **OPT-PORQUE** · lint · error — Under a "¿Por qué…?" stem every option, the key included, starts with "Porque".

## Feedback

- **FB-KEY** · C · error — The key's feedback explains why it is right and why none of the other options is.
- **FB-MATCH** · C · error — Each distractor's feedback refutes that distractor's exact statement: it names what the option claims, corrects only the false part and never contradicts a true part.
- **FB-HEDGE** · lint + C · warning — Feedback says plainly that an option is wrong. If the refutation needs a hedge ("casi correcta", "no es la mejor"), the distractor is defensible (DIS-FALSE): replace it.
- **FB-THIN** · lint · warning — Every option's feedback explains, in at least five words beyond "Correcto." or "Incorrecto.".
- **FB-GENERAL** · C · warning — The general feedback teaches the claim in two or three sentences: what is true, and why the tempting wrong answers are tempting.

## Language

- **LANG-SELF** · lint · error — Learner-facing text stands on its own: it never refers to "el material", the notes, a notebook or the slides; any fact the item needs is stated in it.
- **LANG-CLEAR** · C · warning — The item is hard because of the concept, not the prose: plain, direct Spanish, short sentences, no ornate or over-formal wording, and no story or speaker the question doesn't need (if removing the wrapper changes neither the answer nor the difficulty, remove it).
- **LANG-TRUST** · lint · error — No "confiar en que…": technical systems work in a defined way, not on hope.
- **LANG-GLOSSARY** · C · warning — Technical terms follow the course glossary, with one term per concept in every option. A term kept in English goes in italics and takes the gender of its Spanish equivalent; acronyms and product names don't go in italics.

## Format

- **FMT-SCHEMA** · lint · error — A batch matches the item schema, [`qb/schemas/item-batch.schema.json`](../qb/schemas/item-batch.schema.json).
- **FMT-ANSWERS** · lint · error — One key (fraction 100) and the expected number of distractors: 4 while writing (3 plus a spare), 3 once the item is ready to export.
- **FMT-EMPTY** · lint · error — No empty stem, option or option feedback.
- **FMT-DUPLICATE** · lint · error — No two options with the same visible text.
- **FMT-HTML** · lint · error — Learner-facing HTML uses only whitelisted tags (paragraphs, lists, tables, `strong`, `em`, `u`, `code`, `pre`, `sub`, `sup`, links, images) and no inline styles. `qb export` cleans the editor's Qt markup.

## When rules conflict

Fix in this order, and never keep an elegant item that fails the second or third step:

1. Format: an item that doesn't load can't be judged.
2. Correctness: KEY-UNIQUE, DIS-FALSE, GROUND-SUPPORT.
3. Cues: the rules tested in step A.
4. Feedback.
5. Language and style.

## Dropped rules

Earlier rule files contained these; they are gone on purpose.

- **Master's level (EQF 7).** The course is FP de Grado Superior (CINE 5); the audience comes from the course profile.
- **One key and six distractors.** Experts rarely find more than three functional distractors (Rodriguez 2005), and the quota produced filler and bundled options. Items now carry three distractors plus a spare.
- **Correct-answer position.** Moodle shuffles the options: the export marks every question for shuffling, and the quiz's "shuffle within questions" setting does it.
- **`conceptual-only`.** The course profile lists the question types, including numbers, code, tables and diagnosis of a pipeline.
- **Two or more axes in every item.** Depth comes from the course profile and the item's tier; a one-axis item is right for a core concept.
- **Distractor strategy templates** (Semantic Inversion, Concept Blend and the rest). Semantic Inversion produces options that contradict the stem; distractors now start from a misconception (DIS-BELIEF).
- **"Replace a hard-to-refute distractor with one that is unambiguously false and easy to refute."** It protected against ambiguity but pushed toward trivial distractors; DIS-FALSE and the A rules now hold both sides.
- **"Combine with a related concept when distractors run short."** It produced bundled and off-topic options. Write fewer distractors and report the target as short of misconceptions.
