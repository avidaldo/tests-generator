# Editor Workflow

This editor is the Stage 4 review surface of the quiz pipeline.

The recommended workflow is:

1. import generated Stage 3 batches,
2. review and edit questions,
3. save the current Stage 4 review session,
4. export approved questions to Moodle XML.

## Artifact Roles

Keep these artifact types separate:

- **Stage 3 batch JSON**: generated input. Import it into the current session.
- **Stage 4 review-session JSON**: saved editor work. Open it to replace the current session or save the current session into it.
- **Moodle XML**: final export for Moodle.

Using the wrong action for a JSON file is a workflow error. The editor now rejects that file and points to the correct action.

## Recommended Session Lifecycle

### Start or continue a review session

Use one of these flows:

- Start empty with `Archivo -> Nueva sesión de revisión`
- Continue saved work with `Archivo -> Abrir sesión de revisión...`
- Append new generated questions with `Archivo -> Importar -> Archivos Stage 3...`
- Append a whole Stage 3 root with `Archivo -> Importar -> Carpeta Stage 3...`

### When a session is replaced

`Nueva sesión de revisión` and `Abrir sesión de revisión...` replace the current question set.

If there are unsaved changes, the editor asks whether to:

- `Guardar`
- `Descartar`
- `Cancelar`

`Guardar` writes to the current review-session JSON when one exists. Otherwise it falls back to `Guardar sesión como...`.

## Review Process

Each imported question starts as `Pendiente`.

Raw Stage 3 batches start with 7 answers total. During Stage 4 review it is valid to prune distractors; a reviewed question with 4 total answers is a normal final state for export, not a workflow error.

Use the three review states consistently:

- `Pendiente`: not reviewed yet.
- `Revisar`: reviewed, but not acceptable yet.
- `Lista`: approved for export.

The editor also shows advisory warning markers when the correct answer looks substantially longer or shorter than the distractors after visible-text normalization. These warnings help reviewers catch answer-length bias, but they do not block save or export actions.

Use the `Fácil` flag only as a secondary classification for already approved questions.

## Duplicate Handling

Stage 3 imports append into the current session. They do not replace it.

When the editor finds a question with the same stored import identity, it skips the duplicate instead of importing a second copy. The import summary reports how many questions were added, skipped as duplicates, or rejected because the selected file was not a valid Stage 3 batch.

## Autosave And Recovery

The editor keeps an autosave file for crash recovery.

On startup, if a newer autosave exists, the editor offers to restore it before falling back to the last saved review session. Autosave is a recovery path, not a substitute for explicit `Guardar sesión` or `Guardar sesión como...`.

## Export Rule

Only questions marked as `Lista` are exported through `Archivo -> Exportar -> Moodle XML...`.

The secondary `Moodle XML (solo fáciles)...` export requires both:

- `Lista`
- `Fácil`

## Secondary Legacy Path

`Archivo -> Importar -> Legado -> Banco XML de Moodle...` exists for older XML banks that need to enter the same review flow.

It is intentionally separated from the Stage 3 import path because it is not the normal generated-question workflow.
