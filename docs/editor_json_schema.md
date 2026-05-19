# Editor JSON Schemas

 > Version: 1.0
 > This document is the canonical single source of truth for the JSON payloads shared between `generate-questions.prompt.md` (Stage 3 output), the editor (`editor/file_io/state_io.py`), and the Moodle XML exporter (`resources/json_to_moodle_xml.py`).

 The Stage 3 to Stage 5 workflow now uses two JSON envelopes that share the same `questions[]` payload:

 - **Stage 3 batch JSON**: immutable generation output, written by `generate-questions.prompt.md`
 - **Stage 4 review-session JSON**: editor-owned working artifact, written by the editor after one or more Stage 3 imports or legacy XML imports

 ## Stage 3 Batch JSON

 ```json
 {
   "version": "1.0",
   "questions": [ ... ]
 }
 ```

 Use this envelope for freshly generated batches only. It is the primary import format for the editor and should remain immutable once written.

 Editor contract: the Stage 3 import actions accept this envelope only. If the user selects a saved review-session JSON through the Stage 3 import path, the editor should reject it and ask the user to open it as a review session instead.

 | Field | Type | Description |
 | --- | --- | --- |
 | `version` | string | Schema version. Currently always `"1.0"`. |
 | `questions` | array | Ordered list of question objects. |

 ## Stage 4 Review-Session JSON

 ```json
 {
   "artifact_type": "review_session",
   "version": "1.0",
   "imported_sources": [ ... ],
   "questions": [ ... ]
 }
 ```

 Use this envelope for the editor-owned Stage 4 working artifact. The editor may aggregate questions from multiple Stage 3 batch files and XML imports into one review session.

 The `Abrir sesión de revisión...` action accepts this envelope. Older editor-state JSON files without an explicit `artifact_type` remain readable for backward compatibility, but new saves must always use the explicit review-session envelope.

 | Field | Type | Description |
 | --- | --- | --- |
 | `artifact_type` | string | Always `"review_session"` for editor-owned sessions. |
 | `version` | string | Schema version. Currently always `"1.0"`. |
 | `imported_sources` | array | Optional session-level provenance summary. See [Imported Source Object](#imported-source-object). |
 | `questions` | array | Ordered list of question objects. Export continues to read this top-level array directly. |

 ## Editor Action Contract

 - `Archivo -> Importar -> Archivos Stage 3...` and `Archivo -> Importar -> Carpeta Stage 3...` accept only the raw Stage 3 batch envelope.
 - `Archivo -> Abrir sesión de revisión...` accepts the Stage 4 review-session envelope and backward-compatible legacy editor-state JSON, but rejects raw Stage 3 batches.
 - `Archivo -> Guardar sesión` and `Archivo -> Guardar sesión como...` always write the Stage 4 review-session envelope.

 ## Imported Source Object

 ```json
 {
   "origin_kind": "stage3_batch",
   "origin_path": "/path/to/batch-001.json",
   "label": "batch-001.json"
 }
 ```

 | Field | Type | Description |
 | --- | --- | --- |
 | `origin_kind` | string | Provenance type such as `stage3_batch`, `xml_import`, or `legacy_state`. |
 | `origin_path` | string | Source path recorded by the editor when available. |
 | `label` | string | Human-readable source label, usually the basename of `origin_path`. |

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
 | --- | --- | --- | --- |
 | `id` | string | yes | Sequential code within the subcategory: `SUBCAT_Q001`, `SUBCAT_Q002`, … Use a short uppercase abbreviation of the subcategory. |
 | `name` | string | yes | Human-readable label: `"Q001: Concepto principal de la pregunta"`. |
 | `question_text` | string | yes | HTML. Wrap code samples in `<code>` or `<pre>`. No inline styles. |
 | `general_feedback` | string | yes | HTML. Full didactic explanation of the correct answer and why distractors are wrong. Shown to the student after the attempt. |
 | `category_path` | string | yes | Full Moodle category path: `$course$/top/CategoryRoot/Subcategory`. |
 | `status` | string | yes | Review state. One of `"pendiente"` · `"revisar"` · `"lista"`. Generated questions always start as `"pendiente"`. |
 | `is_easy` | boolean | no | Difficulty flag. `true` marks the question as easy. Only meaningful on `"lista"` questions; used for difficulty-filtered exports. Defaults to `false` if omitted. |
 | `source_ref` | string | Stage 3 yes | One or more concept IDs from the Stage 2 subcategory file, such as `"NORM-01"` or `"NORM-01, CV-03"`. XML-derived questions may leave this empty. |
 | `source_file` | string | no | Legacy compatibility field retained for imported XML or old saved states. New Stage 3 batches should omit it. |
 | `origin_kind` | string | editor-managed | Provenance type written by the editor when importing or saving a Stage 4 review session. |
 | `origin_path` | string | editor-managed | Path of the imported source artifact when known. |
 | `origin_question_id` | string | editor-managed | Stable source identifier used by the editor for duplicate suppression across imports. |
 | `answers` | array | yes | Exactly 7 answer objects: 1 correct + 6 distractors. See [Answer Object](#answer-object). |

 ### Editor-populated Moodle fields

 The editor fills these with correct defaults on import. Stage 3 generation should omit them.

 | Field | Editor default | Notes |
 | --- | --- | --- |
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
 | --- | --- | --- | --- |
 | `text` | string | yes | HTML answer text. |
 | `fraction` | string | yes | `"100"` for the correct answer and `"-50"` for each distractor. See [Scoring](#scoring). |
 | `feedback` | string | yes | HTML. Explanation shown to the student after the attempt. Required on every option because the adversarial validation step depends on it. |
 | `format` | string | yes | Always `"html"`. |

 ### Answer count

 Every question must have exactly 7 answers: 1 correct option and 6 distractors.

 ## Scoring

 `fraction` values implement a 1/2-penalty scheme:

 - **Correct answer** `"100"` → student scores +100% of the question grade.
 - **Each wrong answer** `"-50"` → student scores −50%.

 This is the answer-level penalty. Do not confuse it with the `penalty` field, which is a Moodle adaptive/interactive multi-try concept and is always `"0.0000000"` in this workflow.

 ## Export Note

 `resources/json_to_moodle_xml.py` reads the top-level `questions` array and ignores review-session metadata such as `artifact_type` and `imported_sources`. This is intentional: Stage 4 review-session JSON is the living artifact, while Moodle XML remains the final export format.
