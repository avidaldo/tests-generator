---
name: Resource Utilities
description: "Use when working on resource scripts that convert editor JSON, merge Moodle XML, or transform export files."
applyTo: resources/**
---

- Canonical workflow and command context live in [AGENTS.md](../../AGENTS.md). Treat `resources/` as deterministic utility scripts in the summarise → generate → review → export pipeline, not as a place to redefine quiz policy.
- For JSON export work, read [editor/v3/file_io/state_io.py](../../editor/v3/file_io/state_io.py) and [resources/json_to_moodle_xml.py](../../resources/json_to_moodle_xml.py) together. The JSON schema comes from `state_io.py`; the export CLI defaults to `lista` questions only.
- Preserve backward-compatible CLI behavior unless the task explicitly changes the interface. When behavior changes, update the module docstring examples and keep status-filter semantics explicit.
- Keep CDATA handling intact when emitting Moodle XML. Use [samples/moodle_template.xml](../../samples/moodle_template.xml) and [samples/with_categories.xml](../../samples/with_categories.xml) as reference outputs for category and multichoice structure.
- Keep these scripts file-oriented and deterministic. Do not introduce editor or UI concerns into `resources/`.