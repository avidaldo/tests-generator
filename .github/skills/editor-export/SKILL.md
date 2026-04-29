---
name: editor-export
description: 'Export reviewed quiz-editor JSON state to Moodle XML. Use when opening generated JSON in the editor, checking question statuses, and running the status-filtered json_to_moodle_xml.py script.'
argument-hint: 'Optional: output path or status filter to use'
---

# Editor Export Workflow

This skill covers the final stage of the quiz pipeline: reviewed JSON state to Moodle XML. The canonical workflow lives in [prompts/AGENTS.md](../../../prompts/AGENTS.md), the editor context in [editor/AGENTS.md](../../../editor/AGENTS.md), and the export behavior in [resources/json_to_moodle_xml.py](../../../resources/json_to_moodle_xml.py).

## When To Use

- Export reviewed editor state to Moodle XML.
- Check which statuses should be included in an export.
- Re-run export after human review changes in the editor.

## Procedure

1. Confirm the input format.
   Use this skill only with JSON state compatible with [editor/file_io/state_io.py](../../../editor/file_io/state_io.py).
2. Review before export.
   If the JSON has not been reviewed yet, open it in the editor workflow documented in [editor/README.md](../../../editor/README.md) and complete human review first.
3. Choose the status scope.
   Default export behavior is `lista` only. Include `revisar` explicitly only when the user asks for a broader export, and use `--all-statuses` only for exceptional cases.
4. Run the export script.
   Use one of the documented commands from [resources/json_to_moodle_xml.py](../../../resources/json_to_moodle_xml.py):
   - `python resources/json_to_moodle_xml.py session.json exam.xml`
   - `python resources/json_to_moodle_xml.py session.json exam.xml --status lista revisar`
   - `python resources/json_to_moodle_xml.py session.json exam.xml --all-statuses`
   - `python resources/json_to_moodle_xml.py session.json . --verbose`
5. Validate the result.
   Confirm the output path is correct, the export completed without JSON parse errors, and the status filter matches the user's intent.

## Guardrails

- Do not bypass the editor review step by default.
- Do not assume `pendiente` or `revisar` should ship to Moodle unless the user explicitly requests that scope.
- Keep the export script as the canonical XML path instead of hand-editing XML unless the task specifically requires XML changes.
