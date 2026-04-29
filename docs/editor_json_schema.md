# Editor JSON Schema

> Version: 1.0
> This document is the **canonical single source of truth** for the JSON format used between `generate-questions.prompt.md` (Stage 3 output) and the editor (`editor/file_io/state_io.py`).
>
> Update this file whenever the schema changes, then propagate to the prompt and editor AGENTS.md.

## Top-Level Structure

```json
{
  "version": "1.0",
  "questions": [ ... ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version. Currently always `"1.0"`. |
| `questions` | array | Ordered list of question objects. |

## Question Object

```json
{
  "id": "SUBCAT_Q001",
  "name": "Q001: Nombre descriptivo de la pregunta",
  "question_text": "<p>Enunciado de la pregunta en HTML.</p>",
  "general_feedback": "<p>Explicación didáctica completa.</p>",
  "category_path": "$course$/top/Categoria/Subcategoria",
  "status": "pendiente",
  "source_ref": "NORM-01, NORM-03",
  "answers": [ ... ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Sequential code within the subcategory: `SUBCAT_Q001`, `SUBCAT_Q002`, … Use a short uppercase abbreviation of the subcategory. |
| `name` | string | yes | Human-readable label: `"Q001: Concepto principal de la pregunta"`. |
| `question_text` | string | yes | HTML. Wrap code samples in `<code>` or `<pre>`. No inline styles. |
| `general_feedback` | string | yes | HTML. Full didactic explanation of the correct answer and why distractors are wrong. Shown to the student after the attempt. |
| `category_path` | string | yes | Full Moodle category path: `$course$/top/CategoryRoot/Subcategory`. |
| `status` | string | yes | Review state. One of `"pendiente"` · `"revisar"` · `"lista"`. Generated questions always start as `"pendiente"`. |
| `source_ref` | string | yes | One or more concept IDs from the Stage 2 subcategory file (e.g. `"NORM-01"` or `"NORM-01, CV-03"`). Traces each question back to its source concept and, from there, to the original material. |
| `answers` | array | yes | Exactly 7 answer objects: 1 correct + 6 distractors. See [Answer Object](#answer-object). |

### Editor-populated fields (omit from generated JSON)

The editor fills these with correct defaults on import. Do **not** include them in generated output.

| Field | Editor default | Notes |
|-------|---------------|-------|
| `default_grade` | `"1.0000000"` | Question weight in Moodle. |
| `penalty` | `"0.0000000"` | Adaptive-mode penalty. Always `0` for standard single-attempt exams. |
| `single` | `"true"` | Single-answer multichoice. |
| `shuffle_answers` | `"true"` | Randomise answer order per student. |
| `answer_numbering` | `"abc"` | Answer label style. |
| `correct_feedback` | `"<p>Correcto.</p>"` | Generic Moodle response band. |
| `partially_correct_feedback` | `"<p>Parcialmente correcto.</p>"` | Generic Moodle response band. |
| `incorrect_feedback` | `"<p>Incorrecto.</p>"` | Generic Moodle response band. |

## Answer Object

```json
{
  "text": "<p>Opción correcta</p>",
  "fraction": "100",
  "feedback": "<p>Correcto. Esta opción es correcta porque...</p>",
  "format": "html"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | HTML answer text. |
| `fraction` | string | yes | `"100"` for the correct answer; `"-50"` for each distractor. See [Scoring](#scoring). |
| `feedback` | string | yes | HTML. Explanation shown to the student after the attempt. Required on every option — the adversarial validation step in Stage 3 depends on it. |
| `format` | string | yes | Always `"html"`. |

### Answer count

Every question must have **exactly 7 answers**: 1 correct option and 6 distractors.

## Scoring

`fraction` values implement a ½-penalty scheme:

- **Correct answer** `"100"` → student scores +100% of the question grade.
- **Each wrong answer** `"-50"` → student scores −50% (half the value of a right answer).

This is the *answer-level* penalty. It is the only scoring mechanism used in standard single-attempt mode. Do not confuse it with the `penalty` field, which is a Moodle adaptive/interactive multi-try concept and is always `"0.0000000"` for standard exams.

## Full Example

```json
{
  "version": "1.0",
  "questions": [
    {
      "id": "NORM_Q001",
      "name": "Q001: Efecto de la normalización en modelos basados en distancia",
      "question_text": "<p>¿Qué efecto tiene la normalización Min-Max sobre la función de distancia euclidiana en un modelo KNN?</p>",
      "general_feedback": "<p>La normalización Min-Max reescala cada característica al rango [0, 1], lo que elimina el sesgo que introducen características con rangos numéricos grandes. En KNN, la distancia euclidiana trata todas las características por igual tras la normalización.</p>",
      "category_path": "$course$/top/MachineLearning/Normalizacion",
      "status": "pendiente",
      "source_ref": "NORM-01, NORM-02",
      "answers": [
        {
          "text": "<p>Equipara la influencia de todas las características en el cálculo de distancia.</p>",
          "fraction": "100",
          "feedback": "<p>Correcto. Al reescalar todas las características al mismo rango, ninguna domina el cálculo de distancia por tener valores numéricamente más grandes.</p>",
          "format": "html"
        },
        {
          "text": "<p>Aumenta la influencia de las características con mayor varianza.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. Min-Max no depende de la varianza; reescala según mínimo y máximo observados. La estandarización Z-score sí tiene en cuenta la varianza.</p>",
          "format": "html"
        },
        {
          "text": "<p>Hace que KNN ignore las características con valores pequeños.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. Tras la normalización, todas las características quedan en [0, 1] y ninguna queda ignorada. La falta de normalización es lo que puede marginar características con rangos pequeños.</p>",
          "format": "html"
        },
        {
          "text": "<p>Reduce el número de vecinos necesarios para una clasificación correcta.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. La normalización no afecta al hiperparámetro k ni al número de vecinos consultados.</p>",
          "format": "html"
        },
        {
          "text": "<p>Elimina las características redundantes del espacio de características.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. La normalización reescala los valores existentes; no elimina ni selecciona características. La selección de características es un paso separado.</p>",
          "format": "html"
        },
        {
          "text": "<p>Convierte la distancia euclidiana en distancia coseno.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. Min-Max no cambia el tipo de métrica de distancia utilizada; simplemente cambia la escala de los valores sobre los que se aplica.</p>",
          "format": "html"
        },
        {
          "text": "<p>Garantiza que el modelo converja en menos iteraciones de entrenamiento.</p>",
          "fraction": "-50",
          "feedback": "<p>Incorrecto. KNN no tiene una fase de entrenamiento iterativo; la convergencia es un concepto de modelos paramétricos como redes neuronales o regresión logística con descenso de gradiente.</p>",
          "format": "html"
        }
      ]
    }
  ]
}
```
