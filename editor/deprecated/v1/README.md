# Moodle XML Quiz Editor

Streamlit web interface for reviewing and editing Moodle XML quiz files.

## Purpose

Streamlines quiz curation workflows:
1. **Remove excess distractors** from questions deliberately created with extras
2. **Select best questions** by marking reviewed ones and deleting poor candidates

## Installation

Ensure `streamlit` is installed (already in workspace dependencies):

```bash
uv sync
```

## Running the Editor

**Local development (auto-opens browser):**
```bash
streamlit run CSPy/examen/quiz_editor.py
```

**Headless mode (no browser auto-open):**
```bash
streamlit run CSPy/examen/quiz_editor.py --server.headless true
```

Use headless mode when:
- Running on remote servers
- You want manual control over browser launch
- Working via SSH/terminal-only environments

The app will display URLs like:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## Usage Guide

### 1. Load Quiz File

1. Paste the XML file path in the sidebar (defaults to `comprehensive_exam.xml`)
2. Click **Load File**
3. Questions appear in two sections:
   - **✅ Reviewed** (top, collapsed)
   - **⏳ Pending** (bottom, expanded)

### 2. Review Questions

For each question you can:

- **Review ✓** — Mark as reviewed (moves to top section, collapses)
- **🗑️ Delete** — Remove question entirely
- **🗑️ per answer** — Delete individual wrong distractors (correct answer protected)
- **Expand/collapse** — Click "Show details" on reviewed questions

### 3. Save Changes

**Save to disk:**
- Click **💾 Save XML** in sidebar
- Overwrites original file
- Preserves review state in `.review_state.txt` sidecar

**Download copy:**
- Click **⬇️ Download XML**
- Gets current state without overwriting

**Reload from disk:**
- Click **🔄 Reload from Disk**
- Discards unsaved changes
- Reloads both XML and review state

## Review State Persistence

Review status saves to `<filename>.review_state.txt` alongside the XML file. This persists between sessions so you can resume work later.

## Metrics

Sidebar shows:
- **Total Questions** — Count in current file
- **✅ Reviewed** — Questions marked as done
- **⏳ Pending** — Questions still to review

## Technical Notes

- Uses `xml.etree.ElementTree` for parsing
- Preserves all Moodle XML attributes (fractions, feedback, settings)
- Maintains CDATA wrapping for HTML content
- Only supports `multichoice` question types (the format used in these exams)
