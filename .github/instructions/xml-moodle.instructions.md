---
name: Moodle XML
description: "Use when working on Moodle XML samples, exported quizzes, or XML merge workflows."
applyTo: "**/*.xml"
---

- Canonical workflow context lives in [AGENTS.md](../../AGENTS.md). In this repository, XML is the export and interchange format after question generation and editor review.
- Use [samples/moodle_template.xml](../../samples/moodle_template.xml) and [samples/with_categories.xml](../../samples/with_categories.xml) as local references for valid `<quiz>`, category, and multichoice structure.
- Keep HTML-bearing text fields wrapped in CDATA. The export and merge utilities preserve that behavior intentionally; do not replace it with lossy escaping.
- When tracing how XML is produced or merged, start with [resources/json_to_moodle_xml.py](../../resources/json_to_moodle_xml.py) for editor-state export and [resources/merge_moodle_xml.py](../../resources/merge_moodle_xml.py) for recursive merge semantics.
- Prefer preserving existing ordering and structure over reformatting. `merge_moodle_xml.py` merges files alphabetically by relative path and skips malformed or empty `<quiz>` payloads in verbose mode.