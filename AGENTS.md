# Moodle Tests — Agent Instructions

## Project Overview

This repository contains tools and prompts for generating, editing, and analyzing Moodle XML quiz exams using AI assistance.

## Repository Structure

| Path | Purpose | Instructions |
| ---- | ------- | ------------ |
| `prompts/` | Canonical prompt files (`.prompt.md`) and prompt design/decomposition notes | [`prompts/AGENTS.md`](prompts/AGENTS.md) |
| `.github/instructions/` | VS Code file-scoped instruction adapters (`.instructions.md`) | [`AGENTS.md`](AGENTS.md) |
| `.github/` | VS Code-specific compatibility files and workflows | [`AGENTS.md`](AGENTS.md) |
| `editor/` | PyQt-based Moodle XML quiz editor | [`editor/AGENTS.md`](editor/AGENTS.md) |
| `results/` | Exam result analysis notebooks | [`results/AGENTS.md`](results/AGENTS.md) |
| `docs/` | Domain knowledge and design documentation; see [`docs/agentic_enforcement_layers.md`](docs/agentic_enforcement_layers.md) for the enforcement layer pattern | — |
| `resources/` | Utility scripts (XML conversion, merging) | — |
| `samples/` | Example Moodle XML files | — |

## Language Convention

- **Development language:** English — all code, documentation, instructions, agent prompts, and filenames are written in English.
- **Test output language:** Generated exams are in **Castellano** (Spanish) by default, with technical terms in English in parentheses. This is specified in the `## Output Language` sections of `prompts/generate-questions.prompt.md` and `prompts/generate-test.prompt.md`.
- **Sample files:** `samples/` XMLs contain Spanish content as examples of expected output — their content is intentionally Spanish.
- **Result notebooks:** Analysis notebooks (`results/`) are in English. Column names from the raw Spanish CSV export are kept as-is in code.

## Critical Rules (All Agents)

1. **Student data privacy**: Never output, commit, or log student names, emails, or grades. The `results/data/` directory is gitignored.
2. **Notebook outputs**: For same reason, `.ipynb` files must be committed without cell outputs. The repo uses `nbstripout` as a git filter (`.gitattributes`).
3. **Domain docs**: Consult `docs/` before generating or reviewing quiz content. Particularly `docs/adversarial_logic_filters.md` for distractor design.

## Prompt Files

| File | Description |
| ---- | ----------- |
| `prompts/inventory.prompt.md` | Active prompt: source file inventory and concept extraction |
| `prompts/generate-questions.prompt.md` | Active prompt: one-subcategory question generation in editor-native JSON |
| `prompts/generate-test.prompt.md` | Deprecated monolithic prompt retained for reference |
| `prompts/metaprompting.prompt.md` | Prompt design guidelines — invoke when creating/reviewing any prompt |

## Prompt Pipeline Status

The repository now uses a decomposed prompt pipeline. Treat `inventory.prompt.md` and `generate-questions.prompt.md` as the active generation workflow, and treat `generate-test.prompt.md` as legacy reference material only. Full workflow details, rationale, and file responsibilities are documented in [`prompts/AGENTS.md`](prompts/AGENTS.md).

## Practical Commands

- Sync Python dependencies with `uv sync`.
- Run the editor with `uv run python editor/v3/main.py`.
- Export reviewed JSON state to Moodle XML with `python resources/json_to_moodle_xml.py <input.json> <output.xml>`.
- Verify the notebook output filter is active with `nbstripout --status`.

## VS Code Customization Layout

- Keep `AGENTS.md` files as the canonical cross-agent instruction surface. Root and subfolder `AGENTS.md` files are both loaded by VS Code (`chat.useNestedAgentsMdFiles`).
- Keep `prompts/*.prompt.md` as the canonical prompt files; discovered via `chat.promptFilesLocations` in `.vscode/settings.json`.
- Use `.github/instructions/*.instructions.md` for file-type-scoped rules; current files and their `applyTo` targets:
  - `editor.instructions.md` → `editor/**`
  - `results.instructions.md` → `results/**`
  - `prompt-authoring.instructions.md` → `**/*.prompt.md`
  - `python.instructions.md` → `**/*.py`
  - `notebooks.instructions.md` → `**/*.ipynb`
  - `markdown.instructions.md` → `**/*.md`
- Markdown links in `.instructions.md` files to canonical sources are resolved automatically (`chat.includeReferencedInstructions`).
- Use `.github/hooks/*.json` + scripts for deterministic agent-time enforcement (PostToolUse, PreToolUse); current hooks:
  - `strip-notebook-outputs.json` → strips `.ipynb` outputs after any agent file write
- Use `.github/skills/<name>/SKILL.md` for portable, on-demand multi-step workflows; current skills:
  - `notebook-hygiene` → installs the full four-layer notebook output enforcement stack

---

## General Chat Rules

- **PROMPTING IMPROVEMENTS**: At the very beginning of your final, user-facing response, you MUST include a section titled '### Prompting Improvements'. Do not include this section in any internal thoughts, tool calls, or intermediate reasoning steps.
- **REFLECTION PROTOCOL:** If I ever point out a mistake, bug, or oversight you made, your response MUST begin with a `### Why This Happened` section. You MUST rigorously explain the internal limitation, attention lapse, or logic error that led you to make that specific mistake. Do not just apologize or blindly fix the problem without this analysis.
- **Continuous Improvement:** Constantly suggests improvements to this own instructions to make them better.
- **Self-Criticism:** Be always critical with your own answers, and point out possible limitations or errors.
- **Instruction Criticism:** Be also critical with my instructions. Don't hesitate to point out possible mistakes or improvements.
- **Paramount Rigour:** Rigour is paramount. It's important that all explanations are technically correct.
- **Minimal Changes:** Keep changes minimal and focused on the active task.

## Jupyter Notebooks Guidelines

- It's important to go step by step, using each cell to show its own output and using markdown cells to explain the steps.
- Headings should be alone in their own cells (Markdown) so they can easily fold/unfold.
- Don't number the headings, so they can be easily reordered.
- Imports should be done in the first cell that requires them, not in a separate cell at the top. That way, if a notebook is split in different parts, each part will have its own imports. It also helps with understanding dependencies.
- Explanations should be in markdown cells, never in prints or comments in python cells.
- Comments in code cells should be used to explain specific lines or blocks of code, not for general explanations.
- Small cells should be used to go step by step. Avoid big cells with long outputs. Particularly, avoid several figures as output of the same cell.

## Markdown Guidelines

- Use continuous lines for Markdown prose. Do not hard-wrap paragraphs manually.
- Rely on editor soft wrap for readability when writing or reviewing Markdown.
- Preserve Markdown structure explicitly: headings, lists, tables, code fences, block quotes, and front matter keep their own line-based syntax.
- Leave exceptionally long literals such as URLs, inline code, and table rows on a single line when wrapping them would hurt clarity.

## Python guidelines

- Use in general the most modern practices for Python code (project requires Python ≥3.13).
- Type hints: Use modern syntax for Python 3.13+
- Use `str | None` (not `Optional[str]`).
- Built-in generics: list[str], dict[str, int], tuple[int, ...] (not List, Dict, Tuple)
- Collections: collections.abc.Callable, collections.abc.Iterator (not typing.Callable, typing.Iterator)
- Environment: use `uv` for virtual environments and dependency management (using `uv sync` to keep the environment updated).
- Treat warnings as errors as much as possible.
- Formatting: YAPF (configured in `pyproject.toml`, 120 char limit)
- Imports: Explicit only, don't use "**init**.py" files
- Code should be self-documenting as much as possible, with verbose variable names. Use docstrings only when necessary.
- Use comments to explain only the most complex parts of the code.
- No logging: No logger statements
