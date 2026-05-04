# Quiz Editor — Agent Instructions

> **Note:** Previous editor versions (v1 Streamlit, v2 Textual) are in
> `editor/deprecated/` for reference. All new development targets v3.

## Canonical Scope

This file is the canonical, tool-agnostic instruction surface for the `editor/` module.

- Keep `.github/instructions/editor.instructions.md` as a VS Code routing adapter only, not as a second source of editor policy.
- Target editor v3 for all new development. Treat `editor/deprecated/` as reference material only.
- When introducing or materially changing editor components, update this file and `editor/README.md` together.

## Architecture Principles

This is a PyQt-based Moodle XML quiz editor. All contributions MUST follow these principles rigorously:

### Separation of Concerns (SoC)

- **models/**: Pure data classes and business logic. Zero UI imports.
- **views/**: UI widgets only. No file I/O, no business logic beyond display formatting.
- **file_io/**: XML parsing and writing. No UI, no business logic beyond serialization.

### Single Responsibility Principle (SRP)

- Each class has exactly one reason to change.
- If a class handles both data transformation and persistence, split it.

### Low Coupling / High Cohesion

- Modules communicate through well-defined interfaces (signals/slots for Qt, typed method signatures for models).
- No module should import from more than one other layer.
- Dependency direction: `views → models ← file_io`. Views and file_io never import each other.

### Interface Documentation

- Every public class and method must have a docstring stating:
  - What it does (one line)
  - Parameters and return types
  - Side effects (if any)
- When adding a new module, update this file's Component Reference below.

## Scalability for AI-Assisted Development

To keep AI agent context small and focused:

1. **Each module must be understandable in isolation.** An agent fixing a bug in `xml_parser.py` should not need to read `main_window.py`.
2. **Document interfaces, not implementations.** This file lists what each component exposes publicly, so agents can be pointed only to relevant files.
3. **When creating a new feature**, create or update a doc section below AND update this AGENTS.md.

## Component Reference (v3 — current)

### `models/question.py`

Data classes for quiz content.

- `QuestionStatus(Enum)`: `PENDIENTE`, `REVISAR`, `LISTA`
- `Answer(dataclass)`: Single answer option (`text`, `fraction`, `feedback`, `format`). Property: `is_correct`.
- `Question(dataclass)`: Full question with answers, category, status, and `is_easy` flag (difficulty). Static: `generate_id()`. Properties: `category_name`, `correct_count`, `wrong_count`.
- `Category(dataclass)`: Category path and info. Property: `name`.

### `models/quiz_model.py`

Qt model holding the question list.

- `QuizModel(QAbstractListModel)`: Manages a `list[Question]`.
  - `add_questions(questions) -> int`
  - `remove_question(index) -> Question | None`
  - `insert_question(index, question)`
  - `update_question(index)` — emits `dataChanged`
  - `get_question(index)`, `get_question_by_id(id)`, `get_index_by_id(id)`
  - Properties: `questions`, `categories`

Imports from: `models.question`

### `models/undo_commands.py`

Qt undo commands for edit operations.

- `DeleteQuestionCommand`, `ToggleStatusCommand`, `SetStatusCommand`, `EditQuestionFieldCommand`, `DeleteAnswerCommand`, `EditAnswerCommand`, `ToggleEasyCommand`
- All extend `QUndoCommand` with `redo()`/`undo()`.

Imports from: `models.question`, `models.quiz_model`

### `file_io/xml_parser.py`

Moodle XML deserialization.

- `parse_xml_file(path: Path) -> tuple[list[Category], list[Question]]`
- `parse_multiple_files(paths: list[Path]) -> tuple[list[Category], list[Question]]`

Imports from: `models.question`

### `file_io/xml_writer.py`

Moodle XML serialization.

- `generate_xml(questions: Sequence[Question]) -> str`
- `wrap_cdata(text: str) -> str`

Imports from: `models.question`

### `file_io/state_io.py`

Autosave / state persistence (JSON-based).

- `save_state(questions: list[Question], filepath: Path)`
- `load_state(filepath: Path) -> list[Question]`

**Import contract**: the JSON format is defined in [`docs/editor_json_schema.md`](../docs/editor_json_schema.md). That document is the canonical source of truth for field names, types, required values, and editor-populated defaults. Update it whenever the schema changes; do not rely solely on reading this file or `state_io.py`.

Imports from: `models.question`

### `views/main_window.py`

Top-level window with toolbar, question list, filter sidebar, detail panel.

- `StatusFilterProxyModel(QSortFilterProxyModel)`: Filters by status, category, and easy-only mode.
- `MainWindow(QMainWindow)`: Owns all UI, orchestrates model ↔ views, persists view settings, and applies the user-selected theme.

Imports from: `models.*`, `views.question_detail`, `views.theme`, `file_io.*`

### `views/theme.py`

Shared view-layer theme helpers.

- Theme ids: `system`, `light`, `dark`
- `THEME_OPTIONS`: menu labels for theme selection
- `apply_app_theme(app, theme_mode, system_palette, system_style_name)`
- `effective_theme_variant(theme_mode, palette=None)`
- Style builders for QTextEdit, QLineEdit, muted labels, and answer cards

Imports from: Qt only

### `views/question_detail.py`

Detail editing panel for a single question.

- `AnswerWidget(QFrame)`: Displays/edits one answer. Signals: `delete_requested`, `text_changed`, `feedback_changed`.
- `QuestionDetailPanel(QWidget)`: Edits question fields. Signals: `question_changed`, `delete_question_requested`.
  - `set_question(question: Question | None)`
  - `set_theme_mode(theme_mode: str)`

Imports from: `models.question`, `models.quiz_model`, `models.undo_commands`, `views.theme`

## Adding a New Component

1. Place it in the correct layer (`models/`, `views/`, `file_io/`).
2. Ensure no cross-layer imports violate the dependency direction (`views → models ← file_io`).
3. Add a section to the Component Reference above with its public interface.
4. If it introduces a new concept, document it in `editor/README.md` too.
