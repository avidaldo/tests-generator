# Moodle Quiz Editor

Desktop editor for Moodle XML quiz files using PyQt6. Previous versions (v1 Streamlit, v2 Textual TUI) are in `deprecated/` for reference.

## Features

- **Multi-file import**: Load questions from multiple XML files
- **Category organization**: Filter by category tree
- **Three-state workflow**: "Pendiente" / "Revisar" / "Lista" (approved for exam)
- **Difficulty flag**: Mark approved questions as "Fácil" for difficulty-filtered export
- **Theme selection**: Switch between system, light, and dark themes from `Vista -> Tema`; the choice is persisted between sessions
- **Full undo/redo**: Native Qt QUndoStack
- **HTML preview**: View rendered HTML, edit raw

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
| `Ctrl+O` | Open XML files |
| `Ctrl+S` | Save state |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Delete` | Delete question |

## Open Work

- (P10 completed — difficulty sub-categorization implemented)
