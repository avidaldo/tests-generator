# Moodle Quiz Editor - Specifications v3

## Context

Editor for reviewing and curating exam questions in Moodle XML format. Evolution of `text_editor_old` (Streamlit) and `v2` (Textual TUI).

---

## Functional Requirements

### Data Import
- [ ] Import multiple XML files simultaneously
- [ ] Intelligent merge (avoid duplicates by name)
- [ ] Track the source file for each question

### Organisation and Navigation
- [ ] Group questions by category (hierarchical tree: `$course$/top/...`)
- [ ] Sort by category, status, name
- [ ] Filter by:
  - Category (tree selection)
  - Status: **Ready** / **Review** (only 2 states)
- [ ] Navigation with scroll (mouse/trackpad) and/or keyboard

### Editing
- [ ] **Edit each field manually**:
  - Question name
  - Question text: **rendered HTML to visualise**, raw to edit
  - General feedback
  - Answers: text, fraction, feedback
- [ ] Add/remove answers
- [ ] Change status Ready ↔ Review

### Smooth Deletion
- [ ] Delete question with quick confirmation (or no confirmation + undo)
- [ ] After deletion, focus automatically moves to the next question
- [ ] No full UI reload

### Undo/Redo
- [ ] Ctrl+Z to undo (minimum 5 actions)
- [ ] Ctrl+Shift+Z or Ctrl+Y to redo
- [ ] Persistent history during the session

### Persistence
- [ ] Automatic save of temporary state (JSON)
- [ ] Robust against unexpected closures (periodic autosave)
- [ ] Export to Moodle XML (respecting original format)

### UX
- [ ] Responsive and fast interface (no perceptible lag, < 100ms)
- [ ] Standard shortcuts (Ctrl+O, Ctrl+S, Ctrl+Z) — secondary, not critical

---

## Non-Functional Requirements

| Requirement | Preference |
|-------------|-----------|
| Backend language | Python (preferred) |
| Interaction speed | < 100ms for common actions |
| Framework learning curve | Low–medium |
| Code scalability | Modular, clean architecture |
| Dependencies | Minimal, easy to install |

---

## Lessons from v2 (Textual TUI)

**Problems encountered:**
1. Unstable API across versions (changed events)
2. Complex modal navigation (`push_screen_wait` → workers)
3. Limitations for displaying/editing HTML
4. No natural mouse scrolling in some terminals
5. Learning curve for custom widgets

---

## Alternatives to Evaluate for v3

### Option A: PyQt6 / PySide6 (Native Desktop)

| Pros | Cons |
|------|------|
| Native GUI, very fast | More boilerplate |
| Built-in undo/redo stack (`QUndoStack`) | More complex packaging |
| Rich widgets (trees, tables, editors) | Heavy dependency (~150MB) |
| Excellent documentation | |

### Option B: NiceGUI (Python + Modern Web)

| Pros | Cons |
|------|------|
| Pure Python, elegant API | Newer (small community) |
| Hot reload, reactive | Performance with many elements |
| Runs in browser | |
| Easy two-way bindings | |

### Option C: Streamlit improved + st-aggrid

| Pros | Cons |
|------|------|
| Already familiar | Full reruns (slow) |
| Easy to iterate | Manual undo/redo |
| AgGrid for editable tables | Limited for complex UX |

### Option D: FastHTML + HTMX

| Pros | Cons |
|------|------|
| Pure Python | Still very new |
| Partial updates (no full reload) | Requires knowing HTMX |
| Lightweight | |

### Option E: Tauri + Svelte (hybrid)

| Pros | Cons |
|------|------|
| Lightweight native app | Requires Rust + JS |
| Modern web UI | Two languages |
| Cross-platform | |

---
