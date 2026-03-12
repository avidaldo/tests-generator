# Moodle Quiz Editor v2

Terminal-based editor for Moodle XML quiz files using [Textual](https://textual.textualize.io/).

## Features

- **Multi-file import**: Load questions from multiple XML files
- **Category organization**: Group and filter questions by category
- **Two-state workflow**: Questions are either "Lista" (done) or "Revisar" (to review)
- **Full undo/redo**: Ctrl+Z / Ctrl+Y with history
- **Keyboard-driven**: Fast navigation with familiar shortcuts
- **JSON persistence**: Save/restore editor state between sessions

## Running

```bash
# From the workspace root
uv run python moodle-tests/editor/v2/app.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open XML files |
| `Ctrl+S` | Save state |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Delete` | Delete question |
| `Space` | Toggle status (Lista/Revisar) |
| `↑/↓` | Navigate questions |
| `F1` | Show help |
| `Q` | Quit |

## Architecture

```
v2/
├── app.py              # Main TUI application
├── models/
│   ├── question.py     # Question, Answer, Category dataclasses
│   └── quiz_store.py   # State management with undo/redo
└── file_io/
    ├── xml_parser.py   # Moodle XML parsing
    └── xml_writer.py   # Moodle XML generation
```
