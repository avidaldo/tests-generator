# Moodle Quiz Editor

Desktop editor for Stage 4 human review of generated quiz questions using PyQt6. The primary input is one or more Stage 3 batch JSON files, saved into one editor-owned review-session JSON, and exported to Moodle XML at the end of the process. Legacy XML import remains available for older banks. Previous versions (v1 Streamlit, v2 Textual TUI) are in `deprecated/` for reference.

## Features

- **Stage 3 batch import**: Load one or more generated JSON batch files directly into the editor
- **Stage 3 folder import**: Load every recursive `batch-*.json` file under a selected Stage 3 root
- **Review-session save/load**: Persist the consolidated Stage 4 working set as JSON
- **Legacy XML import**: Bring older Moodle XML banks into the same review workflow when needed
- **Category organization**: Filter by category tree
- **Three-state workflow**: "Pendiente" / "Revisar" / "Lista" (approved for exam)
- **Difficulty flag**: Mark approved questions as "Fácil" for difficulty-filtered export
- **Theme selection**: Switch between system, light, and dark themes from `Vista -> Tema`; the choice is persisted between sessions
- **Full undo/redo**: Native Qt QUndoStack
- **HTML preview**: View rendered HTML, edit raw

## Primary Workflow

1. Start a new review session in the editor.
2. Import one or more Stage 3 batch JSON files with `Ctrl+O`, or import a whole Stage 3 root recursively with `Archivo -> Importar carpeta Stage 3...`.
3. Review and edit questions, then save the consolidated review session as JSON.
4. Export only the approved `Lista` questions to Moodle XML.

Use `Archivo -> Abrir sesión de revisión...` to reopen a saved Stage 4 session. Use `Archivo -> Importar XML...` only when working with older XML banks.

## Appearance

Use `Vista -> Tema` to switch between `Sistema`, `Claro`, and `Oscuro`.
The editor remembers the last selected theme through `QSettings` and restores it on the next launch.
Dark mode now applies explicit readable colors to question editors and answer/distractor cards instead of relying on whatever palette the host desktop provides.

## Running

```bash
uv sync  # Install dependencies
uv run python editor/main.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Import Stage 3 batch JSON |
| `Ctrl+S` | Save review session |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete question |

## Open Work

- (P10 completed — difficulty sub-categorization implemented)
