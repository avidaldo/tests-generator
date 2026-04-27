---
name: Editor Architecture
description: Architecture and maintenance rules for the PyQt Moodle XML editor.
applyTo: editor/**
---

- Canonical editor instructions live in [editor/AGENTS.md](../../editor/AGENTS.md). Follow that file as the source of truth for the `editor/` module.
- Preserve the layer boundary `views → models ← file_io`. Views and file I/O modules should not import each other directly.
- Start local debugging from the layer that owns the behavior: persistence issues in `file_io/`, data shape issues in `models/`, and widget orchestration in `views/`.
- When adding or materially changing editor components, update [editor/AGENTS.md](../../editor/AGENTS.md) and `editor/v3/README.md` together.