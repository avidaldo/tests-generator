# Moodle Quiz Editor

Desktop editor for Moodle XML quiz files using PyQt6. Previous versions (v1 Streamlit, v2 Textual TUI) are in `deprecated/` for reference.

## Features

- **Multi-file import**: Load questions from multiple XML files
- **Category organization**: Filter by category tree
- **Three-state workflow**: "Pendiente" / "Revisar" / "Lista" (approved for exam)
- **Difficulty flag**: Mark approved questions as "Fácil" for difficulty-filtered export
- **Full undo/redo**: Native Qt QUndoStack
- **HTML preview**: View rendered HTML, edit raw

## Running

```bash
uv sync  # Install dependencies
uv run python editor/main.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open XML files |
| `Ctrl+S` | Save state |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete question |

## Open Work

- (P10 completed — difficulty sub-categorization implemented)
