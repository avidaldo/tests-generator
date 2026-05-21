# Moodle Quiz Editor

Desktop editor for Stage 4 human review of generated quiz questions using PyQt6. The normal workflow is:

1. import generated Stage 3 questions,
2. review and edit them inside one Stage 4 review session,
3. save that review session as JSON,
4. export approved questions to Moodle XML.

Legacy XML import remains available for older banks, but it is a secondary path. Previous versions (v1 Streamlit, v2 Textual TUI) remain in `deprecated/` for reference.

## Mental Model

The editor works with three artifact types that should not be confused:

- **Stage 3 batch JSON**: generated question batches. Import them into the current review session.
- **Stage 4 review-session JSON**: the editor-owned working file. Open it to replace the current session, or save the current session into it.
- **Moodle XML**: final export format for approved questions.

If you use the wrong action for a JSON file, the editor now rejects it and tells you which action to use instead.

## Main Actions

### Add generated Stage 3 questions

- `Archivo -> Añadir -> Archivos Stage 3...`
- `Archivo -> Añadir -> Carpeta Stage 3...`

Both actions **append** questions into the current review session. Folder import is recursive and only reads `batch-*.json` files. Duplicate questions are skipped using the stored provenance keys.

Stage 3 `id` values do not need to be globally unique across a merged review session. The editor tracks imported duplicates by provenance and applies edits to the currently selected question instance.

Imported Stage 3 batches start with 7 answers total: 1 correct option + 6 distractors. During Stage 4 review it is valid to prune distractors; approved questions often finish with 4 answers total before export.

If a Stage 3 batch includes `generated_by_model`, the detail panel keeps that question-level model label in the existing provenance line and preserves it when the review session is saved.

### Open a saved review session

- `Archivo -> Abrir sesión de revisión...`

This action opens one saved Stage 4 session file and **replaces** the questions currently loaded in the editor. If there are unsaved changes, the editor asks whether to **Guardar**, **Descartar**, or **Cancelar** before replacing it.

### Save the current review session

- `Archivo -> Guardar sesión`
- `Archivo -> Guardar sesión como...`

Use these actions to persist the current Stage 4 working set. `Guardar sesión` reuses the current file when one already exists. `Guardar sesión como...` always asks for a new path.

### Export to Moodle XML

- `Archivo -> Exportar -> Moodle XML...`

This exports only questions marked as `Lista`. The secondary `Moodle XML (solo fáciles)...` action exports only questions marked both `Lista` and `Fácil`.

## Secondary Actions

- `Archivo -> Añadir -> Legado -> Banco XML de Moodle...`: import older XML banks into the review workflow.
- `Nueva sesión de revisión`: clear the current working set after the same confirmation flow, but only when there are unsaved changes.

## Review States

- `Pendiente`: not reviewed yet.
- `Revisar`: seen, but still needs work.
- `Lista`: approved for export.

The `Fácil` flag is an optional secondary marker for approved questions.

## Review Warnings

The editor shows non-blocking warning markers when the correct answer looks substantially longer or shorter than the distractors after visible-text normalization. These warnings are advisory only. They exist to catch a common multiple-choice bias where answer detail, rather than conceptual accuracy, gives away the correct option.

## Appearance

Use `Vista -> Tema` to switch between `Sistema`, `Claro`, and `Oscuro`.
The editor remembers the last selected theme through `QSettings` and restores it on the next launch.

## Running

```bash
uv sync
uv run python editor/main.py
```

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `Ctrl+O` | Import Stage 3 files |
| `Ctrl+S` | Save review session |
| `Ctrl+Shift+S` | Save review session as |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete question |

## Further Reading

- [Workflow guide](docs/WORKFLOW.md)
- [Import and export guide](docs/IMPORT_EXPORT.md)
- [Editor architecture](AGENTS.md)
- [Shared JSON schema](../docs/editor_json_schema.md)
