# Import And Export Guide

This document explains which action to use for each file type and what effect that action has on the current session.

## Import Matrix

| Goal | Menu action | Accepted input | Effect on current session |
| ---- | ---- | ---- | ---- |
| Import generated question files | `Archivo -> Importar -> Archivos Stage 3...` | One or more Stage 3 batch JSON files | Appends questions |
| Import a generated question folder | `Archivo -> Importar -> Carpeta Stage 3...` | A directory scanned recursively for `batch-*.json` | Appends questions |
| Open saved editor work | `Archivo -> Abrir sesión de revisión...` | One Stage 4 review-session JSON file, plus backward-compatible legacy editor-state JSON | Replaces questions |
| Import an older XML bank | `Archivo -> Importar -> Legado -> Banco XML de Moodle...` | One or more Moodle XML files | Appends questions |

## Stage 3 Import

Use Stage 3 import when the selected file was produced by the question-generation pipeline.

Characteristics:

- accepts only Stage 3 batch JSON,
- appends questions into the current session,
- skips duplicates using stored provenance fields,
- reports rejected files individually.

### File import

Use `Archivos Stage 3...` when you already know which batch files you want.

### Folder import

Use `Carpeta Stage 3...` when you want the editor to discover batches automatically.

Current contract:

- recursive search,
- only files named `batch-*.json`,
- hidden directories ignored.

## Open Review Session

Use `Abrir sesión de revisión...` only for a saved Stage 4 working file.

Characteristics:

- opens one file,
- replaces the current session,
- asks `Guardar / Descartar / Cancelar` before replacement when unsaved changes exist,
- rejects raw Stage 3 batch JSON and tells the user to use the Stage 3 import actions instead.

Backward compatibility remains for older editor-state JSON files that predate the explicit `artifact_type: review_session` envelope.

## Save Review Session

Use these actions for the editor-owned Stage 4 artifact:

- `Guardar sesión`
- `Guardar sesión como...`

`Guardar sesión` reuses the current file when there is one.

`Guardar sesión como...` always asks for a new path.

These actions write a Stage 4 review-session JSON envelope, not a raw Stage 3 batch.

## Export To Moodle XML

Use `Archivo -> Exportar -> Moodle XML...` for the normal final export.

Rules:

- exports only questions marked `Lista`,
- writes Moodle XML,
- does not modify the current review session.

Use `Archivo -> Exportar -> Moodle XML (solo fáciles)...` only when you want the approved easy subset.

That secondary export requires questions marked both:

- `Lista`
- `Fácil`

## Common Mistakes

### Trying to open a Stage 3 batch as if it were a saved review session

This is the wrong action.

Use `Archivo -> Importar -> Archivos Stage 3...` or `Archivo -> Importar -> Carpeta Stage 3...` instead.

### Trying to import a saved review session through the Stage 3 import path

This is also the wrong action.

Use `Archivo -> Abrir sesión de revisión...` instead.

### Expecting `Abrir sesión de revisión...` to merge files

It does not merge. It replaces the current session.

If you want to keep the current questions and add more generated content, stay on the Stage 3 import actions.
