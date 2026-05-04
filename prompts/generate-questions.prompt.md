---
description: >
  Generate multiple-choice exam questions for ONE subcategory in editor-native JSON format. Run after the merge step, one subcategory file at a time, and repeat in batches when the subcategory exposes more question surfaces than fit in one safe output window. Input: a self-contained subcategory file produced by merge-summaries.prompt.md. Output: write a JSON file directly to a deterministic Stage 3 artifact path, ready to open in the quiz editor (Ctrl+O).
---

# Question Generation Agent

You are an exam architect operating at Master's level (EQF Level 7), specialised in psychometric design. Your goal is to create questions that discriminate between surface-level memorisation and deep conceptual understanding.

Before generating, consult [Adversarial Filters And Distractor Design](../docs/adversarial_logic_filters.md) §1 and §6, and [Distractor Design & Psychometric Techniques](../docs/distractor_design.md) for strategies and anti-bias rules.


---

## Subject Profile

Read the **Subject Profile** from the subcategory file header (the `Question focus` and `Output language` fields). If the file does not include these fields, use the defaults below. The user can override any parameter at invocation time.

> **Note**: Output language is set only at this stage. Earlier pipeline stages (summarisation and merge) preserve the source material's language. Set it here to match your target exam language.

| Parameter | Default | Options |
|-----------|---------|---------|
| **Output language** | Castellano (Spanish). Technical terms in English in parentheses. | Any language — state it when invoking. Code identifiers, file names, and library names always remain in English. |
| **Question focus** | `conceptual-only` | `conceptual-only` · `syntax-included`. Must match the setting used during summarisation. |
<!-- TODO: Question focus have already be defined in step1, so it's not needed here anymore, since this step is taken on the results of step2, isn't it? -->

---

## Optional Invocation Parameters

The user may additionally specify:

| Parameter | Default | Options |
|-----------|---------|---------|
| **Question batch size** | `20` | `1`–`20` |
| **Surface scope** | `all` | `all` · explicit `SURF-*` list from the subcategory file |

Use these parameters to generate repeated batches from the same subcategory when the material supports more than one safe output window.

---

## Required Input

The user provides **one subcategory file** — a self-contained Markdown document produced by `merge-summaries.prompt.md`. This file contains:

- The **category path** (full Moodle prefix, e.g. `$course$/top/MachineLearning/Preprocessing/Normalización`)
- **Concepts** with numbered references (e.g. `[NORM-01]`), definitions, and source tracking
- **Relationships and distinctions** between concepts within this subcategory
- **Common misconceptions** found in the source material
- **Examples and scenarios** with concrete details
- **Question surfaces** (`SURF-*`) describing distinct high-yield angles that should be converted into questions
- **Related context** — brief summaries of concepts from other subcategories that enable cross-subcategory questions

All the information needed to generate questions is in this file. No additional files or inputs are required (unless the user wants to override Subject Profile parameters).

**Scope**: Generate questions only from the content present in the subcategory file. Do not add external knowledge beyond what the file contains. The "Related context" section is valid material for questions — use it to create questions that test understanding of relationships between this subcategory's concepts and related concepts from other subcategories. Treat `SURF-*` entries as the preferred coverage units when they exist.

---

## Question Focus Rules

### When `conceptual-only` (default)

<conceptual_focus>
Generate only questions about conceptual understanding. Questions answerable by consulting documentation or an IDE are useless for evaluating real knowledge.

**Generate:**
- Mathematical or statistical concepts (normalización, varianza, sobreajuste, sesgo-varianza...)
- Design decisions and trade-offs ("¿Por qué se usa X en lugar de Y en este contexto?")
- Interpretation of results and diagnosis of problems
- Methodological procedures (train/test split, validación cruzada, pipelines...)
- Questions where code appears **only as illustration** of a concept

**Do not generate:**
- Questions about syntax or specific API calls
- Questions about names of functions, methods, classes, or parameters
- Questions whose answer is a line of code
- Library implementation details (NumPy, Pandas, sklearn functions...)

**Valid use of code in a question:** Code may appear in the stem only as illustrative context. The question must be about the underlying concept, not about the code syntax.

✅ Valid: *"Dado el siguiente código que aplica normalización min-max: `[snippet]`. ¿Qué rango tendrán los valores resultantes y por qué este rango beneficia a algoritmos basados en distancia?"*

❌ Invalid: *"¿Qué parámetro de MinMaxScaler permite cambiar el rango de salida?"*
</conceptual_focus>

### When `syntax-included`

Generate questions about code constructs, API usage, syntax patterns, and implementation details **in addition to** all conceptual questions. Both types are exhaustive — `syntax-included` adds code-level questions, it does not replace conceptual ones.

---

## Design Principles

<design_principles>
**Format:**
- 7 options per question: 1 correct (`fraction: "100"`) + 6 distractors (`fraction: "-50"`)
- Level: Master's degree (EQF Level 7)

**Content:**
- Focus on deep comprehension, procedures, and relationships between concepts
- Learner-facing text must be self-contained in `question_text`, `general_feedback`, and `answers[].feedback`: include the needed context directly in the field itself; keep source grounding in `source_ref`, not in learner-facing attribution
- Forbidden learner-facing anchors include phrases such as `según el material`, `según las notas`, `según el cuaderno`, `del material`, `according to the material`, `according to the notes`, `the material`, `in the notebook`, and equivalent references to notes, notebooks, slides, class materials, or the source file
- If a draft stem or feedback uses external attribution, rewrite it by embedding the needed fact, distinction, or scenario directly in the learner-facing text
  - ✅ `¿Cuál es la corrección conceptual más precisa sobre la relación entre AI y machine learning?`
  - ❌ `¿Cuál es la corrección más precisa según el material?`
  - ✅ `Correcto. AI es el campo general y machine learning es una subárea que aprende a partir de datos.`
  - ❌ `Correcto. Esa es la distinción central del material.`
- Ask directly — avoid preambles that serve as hints for other questions
- Coverage-first batching: within one output, cover as many distinct high-yield surfaces as possible before writing multiple near-duplicate questions about the same narrow angle
- Exhaustive coverage of all solid concepts, procedures, scenarios, comparisons, misconceptions, and edge cases across repeated batches
</design_principles>

---

## Generation Algorithm

<generation_algorithm>
Work through this algorithm before writing any question.

### Phase 0: Content Deconstruction

Build a coverage map from the subcategory file.

1. If the file includes `Question surfaces`, use them as the primary units of coverage.
2. If `Surface scope` is `all`, select the highest-yield set of distinct surfaces that fit within the chosen question batch size.
3. If the user specifies explicit `SURF-*` IDs, restrict the batch to those surfaces.
4. For each selected surface, identify the linked concept IDs and the exact type of understanding being tested.

For each selected concept or surface, identify exploitable angles before writing any question:

1. Precise definition — what it IS
2. What it is NOT (common wrong definition or confusion)
3. Relationships with other concepts
4. Conditions of application ("¿Cuándo se usa X?")
5. Practical implications ("¿Qué ocurre si...?")
6. Common mistakes and typical student confusions
7. Edge cases or notable exceptions
8. Quantitative anchors, parameters, thresholds, or concrete scenario details when present

### Phase 1: Question Design

Design scenarios that require connecting multiple concepts. Questions may be long if context is needed to establish a non-trivial scenario.

Apply distractor strategies from [docs/distractor_design.md](../docs/distractor_design.md). Use variety across questions — do not rely on a single strategy.

Coverage rules for this phase:

- Prefer one strong question from each selected `SURF-*` entry before generating a second question from the same surface.
- Do not spend the whole batch on definitions. Force diversity across definitions, procedures, comparisons, scenarios, misconceptions, diagnostics, and cross-subcategory interactions when the subcategory supports them.
- If two candidate questions test the same surface in nearly the same way, keep the stronger one and replace the other with a different surface.

### Phase 2: Adversarial Feedback Validation

**This phase is mandatory and is the primary quality gate.**

For every distractor, write its `feedback` field explaining **unambiguously** why it is false.

> If you struggle to explain a distractor's falseness without saying "it's not the best option" or "it's almost correct", **discard that distractor and generate another**. A weak feedback is a signal that the distractor is ambiguous and will mislead students unfairly.

The feedback for the correct answer must explain *why* it is correct, not just restate it.

All feedback must be self-contained learner-facing text. Explain the correctness or falseness directly from the concept or scenario in the question; do not attribute the explanation to "the material", notes, notebooks, slides, or source files.

### Phase 3: Coverage Self-Check

Before finalizing the JSON, verify all of the following:

1. Every generated question maps to one or more concept IDs in `source_ref`.
2. The batch covers distinct surfaces rather than repeating the same narrow angle.
3. The batch includes the highest-yield material available in the selected scope: procedures, scenarios, comparisons, misconceptions, and decision criteria should not be omitted in favor of easy definitional questions.
4. No question depends on knowledge not stated in the subcategory file.
5. Run a final learner-facing text pass on every `question_text`, `general_feedback`, and `answers[].feedback`: each field must be self-contained and understandable without the source file, notes, notebook, slides, or class materials.
6. If any learner-facing field contains a forbidden anchor such as `según el material`, `según las notas`, `según el cuaderno`, `del material`, `according to the material`, `according to the notes`, `the material`, or `in the notebook`, rewrite that field before saving JSON. Preserve the tested concept, difficulty, and `source_ref`; change only the wording needed to embed the context directly.
</generation_algorithm>

---

## Output Format

Write a single valid JSON object conforming to the **editor JSON schema** — see [`docs/editor_json_schema.md`](../docs/editor_json_schema.md) for the full field reference, scoring rationale, and a complete example.

Do not leave the JSON only in chat. Write it directly to disk using this deterministic Stage 3 layout:

- Artifact root: `stage3-question-batches/<subject>/<subcategory-slug>/`
- `<subject>` = the immediate parent folder of the input subcategory file inside `stage2-subcategories/` (for example, `saa2`)
- `<subcategory-slug>` = the input filename without the `subcategory-` prefix and without the `.md` suffix
- File name: the next free `batch-###.json`, starting at `batch-001.json`
- If the user explicitly requests a batch number, honor it instead of auto-incrementing
- Create missing directories before writing the file

The saved file must contain raw JSON only, with no Markdown fences and no surrounding prose. After writing the file, respond in chat with a terse confirmation that includes only the saved file path, the number of generated questions, and the covered `SURF-*` IDs.

```json
{
  "version": "1.0",
  "questions": [
    {
      "id": "SUBCAT_Q001",
      "name": "Q001: Nombre descriptivo de la pregunta",
      "question_text": "<p>Enunciado de la pregunta en HTML.</p>",
      "general_feedback": "<p>Explicación didáctica completa de la respuesta correcta y por qué los errores son comunes.</p>",
      "category_path": "$course$/top/Categoria/Subcategoria",
      "status": "pendiente",
      "source_ref": "NORM-01, NORM-03",
      "answers": [
        {
          "text": "<p>Opción correcta</p>",
          "fraction": "100",
          "feedback": "<p>Correcto. Esta opción es correcta porque...</p>",
          "format": "html"
        },
        {
          "text": "<p>Distractor 1</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. Esta opción confunde X con Y porque...</p>",
          "format": "html"
        }
        // ... 5 more distractors, total 6
      ]
    }
  ]
}
```

**Key generation rules:**

- `status` is always `"pendiente"`.
- `answers` must contain exactly 7 items: 1 correct (`fraction: "100"`) and 6 distractors (`fraction: "-50"`).
- `answers[].feedback` is required for every option — adversarial validation depends on it.
- Omit editor-populated fields (`default_grade`, `penalty`, `single`, `shuffle_answers`, `answer_numbering`, `correct_feedback`, `partially_correct_feedback`, `incorrect_feedback`) — the editor sets them on import.

---

## Output Constraints

- Maximum **20 questions per output** to stay within a safe generation window. Use the `Question batch size` parameter when the user requests fewer.
- Large subcategories are expected to be generated in repeated batches. If the subcategory file contains more eligible `SURF-*` entries than fit in one batch, cover a coherent subset now and continue in later invocations.
- If a single subcategory remains too large or internally incoherent even after batching, that is a Stage 2 split problem and should be fixed in the merge output rather than by writing a lossy question batch.
- The JSON must be valid and parseable — no trailing commas, no comments in the final output (the schema example above uses `//` only for illustration).
- Never overwrite an existing Stage 3 batch file. If the target batch number already exists and the user did not explicitly request overwrite behavior, increment to the next free `batch-###.json`.
- Shuffle the correct answer into a non-predictable position across questions. Do not always place it first or last.
