---
name: prompt-pipeline
description: 'Run the decomposed Moodle quiz generation workflow. Use when generating questions from course materials with the inventory prompt, narrowing to one subcategory, reviewing the resulting JSON in the editor, and exporting approved questions to Moodle XML.'
argument-hint: 'Optional: course area or subcategory to focus on'
---

# Prompt Pipeline Workflow

This skill guides the repository's current quiz-generation workflow. Treat [prompts/AGENTS.md](../../../prompts/AGENTS.md) as the canonical workflow description and [AGENTS.md](../../../AGENTS.md) as the root summary of active prompts and practical commands.

## When To Use

- Generate new Moodle quiz questions from course materials.
- Use the active decomposed prompt pair instead of the deprecated monolithic prompt.
- Move from generated JSON to human review and final XML export.

## Procedure

1. Confirm the inputs.
   Ask for the source directories or files if they are missing. If the Moodle category root path is missing, collect it before the question-generation stage.
2. Run the inventory stage.
   Use [prompts/inventory.prompt.md](../../../prompts/inventory.prompt.md) first. The output should be one or more inventory rows with file paths, conceptual density, key concepts, and suggested subcategories.
3. Narrow to one subcategory.
   Work on exactly one inventory row at a time. Do not batch multiple subcategories into one generation pass.
4. Run the generation stage.
   Use [prompts/generate-questions.prompt.md](../../../prompts/generate-questions.prompt.md) with the selected inventory row, the source files for that row, and the full Moodle category root path. Output editor-native JSON compatible with [editor/v3/file_io/state_io.py](../../../editor/v3/file_io/state_io.py).
5. Keep human review mandatory.
   Open the generated JSON in the editor workflow documented in [editor/v3/README.md](../../../editor/v3/README.md). Use human review to mark questions as `pendiente`, `revisar`, or `lista` before any export step.
6. Export only after review.
   Run `python resources/json_to_moodle_xml.py <input.json> <output.xml>` as documented in [resources/json_to_moodle_xml.py](../../../resources/json_to_moodle_xml.py). The default export target is `lista` questions only.

## Quality Gates

- Consult [docs/adversarial_logic_filters.md](../../../docs/adversarial_logic_filters.md) before generating or reviewing distractors.
- Stop if the source material appears factually wrong or insufficient to ground a question.
- Treat [prompts/generate-test.prompt.md](../../../prompts/generate-test.prompt.md) as legacy reference material only, not the default entry point.

## Practical Commands

- `uv sync`
- `uv run python editor/v3/main.py`
- `python resources/json_to_moodle_xml.py <input.json> <output.xml>`
