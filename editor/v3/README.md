# Moodle Quiz Editor v3

<!-- TODO: v3 is the currently maintained version. v1 and v2 are kept in the 'deprecated' directory for didactic purposes. This version is expected to be continued without further big migrations so it should be moved to the main directory, with a recheck of the structure and a clear documentation, including the integration with the previous workflow.-->
Desktop editor for Moodle XML quiz files using PyQt6.

## Features

- **Multi-file import**: Load questions from multiple XML files
- **Category organization**: Filter by category tree
- **Two-state workflow**: "Lista" (done) / "Revisar" (to review)
- **Full undo/redo**: Native Qt QUndoStack
- **HTML preview**: View rendered HTML, edit raw

## Running

```bash
uv sync  # Install dependencies
uv run python moodle-tests/editor/v3/main.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open XML files |
| `Ctrl+S` | Save state |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete question |
```

todo:
- Exportar solo las "Listas"
- "Lista pero fácil"