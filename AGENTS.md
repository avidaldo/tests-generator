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
| `resources/` | Utility scripts (XML conversion, merging) | [`.github/instructions/resources.instructions.md`](.github/instructions/resources.instructions.md) |
| `samples/` | Example Moodle XML files | [`.github/instructions/xml-moodle.instructions.md`](.github/instructions/xml-moodle.instructions.md) |

## Language Convention

- **Development language:** English — all code, documentation, instructions, agent prompts, and filenames are written in English.
- **Test output language:** Generated exams are in **Castellano** (Spanish) by default, with technical terms in English in parentheses. This is configurable via the **Subject Profile** in both prompt files — the user can override the output language at invocation time.
- **Sample files:** `samples/` XMLs contain Spanish content as examples of expected output — their content is intentionally Spanish.
- **Result notebooks:** Analysis notebooks (`results/`) are in English. Column names from the raw Spanish CSV export are kept as-is in code.

## Critical Rules (All Agents)

1. **Student data privacy**: Never output, commit, or log student names, emails, or grades. The `results/data/` directory is gitignored.
2. **Notebook outputs**: For same reason, `.ipynb` files must be committed without cell outputs. The repo uses `nbstripout` as a git filter (`.gitattributes`).
3. **Domain docs**: Consult `docs/` before generating or reviewing quiz content. Particularly `docs/adversarial_logic_filters.md` for the adversarial filter mechanism and `docs/distractor_design.md` for distractor strategies and psychometric techniques.

## Prompt Pipeline

See [`prompts/AGENTS.md`](prompts/AGENTS.md) for the active prompt inventory, pipeline diagram, design rationale, and file responsibilities.

Active workflow: `summarize-sources.prompt.md` (rich content extraction, one per repo) → `merge-summaries.prompt.md` (subcategory files with cross-cutting context) → `generate-questions.prompt.md` (one subcategory file per invocation) → editor review → XML export.

Each step is run manually. See the [Usage guide in README.md](README.md#usage-generating-exam-questions) for step-by-step instructions.

## Practical Commands

- Sync Python dependencies with `uv sync`.
- Run the editor with `uv run python editor/v3/main.py`.
- Export reviewed JSON state to Moodle XML with `python resources/json_to_moodle_xml.py <input.json> <output.xml>`.
- Verify the notebook output filter is active with `nbstripout --status`.

## VS Code Customization Layout

- Keep `AGENTS.md` files as the canonical cross-agent instruction surface. Root and subfolder `AGENTS.md` files are both loaded by VS Code (`chat.useNestedAgentsMdFiles`).
- Keep `prompts/*.prompt.md` as the canonical prompt files; discovered via `chat.promptFilesLocations` in `.vscode/settings.json`.
- Use `.github/instructions/*.instructions.md` for file-type-scoped rules; current files and their `applyTo` targets:
  - `customization-authoring.instructions.md` → `.github/instructions/*.instructions.md`, `.github/agents/*.agent.md`, `.github/skills/**/SKILL.md`
  - `editor.instructions.md` → `editor/**`
  - `documentation-sync.instructions.md` → sync surfaces plus prompt/customization files that commonly create drift
  - `markdown.instructions.md` → `**/*.md`
  - `notebooks.instructions.md` → `**/*.ipynb`
  - `prompt-authoring.instructions.md` → `**/*.prompt.md`, `**/*.instructions.md` (includes prompt design research guidance, formerly `metaprompting.prompt.md`)
  - `question-design.instructions.md` → `prompts/generate-questions.prompt.md` (auto-attaches psychometric domain knowledge)
  - `python.instructions.md` → `**/*.py`
  - `resources.instructions.md` → `resources/**`
  - `results.instructions.md` → `results/**`
  - `xml-moodle.instructions.md` → `**/*.xml`
- Markdown links in `.instructions.md` files to canonical sources are resolved automatically (`chat.includeReferencedInstructions`).
- Use `.github/hooks/*.json` + scripts for deterministic agent-time enforcement (PostToolUse, PreToolUse); current hooks:
  - `strip-notebook-outputs.json` → strips `.ipynb` outputs after any agent file write
  - `prompt-doc-drift-check.json` → warns when prompt/customization changes may need documentation-sync updates
- Use `.github/skills/<name>/SKILL.md` for portable, on-demand multi-step workflows; current skills:
  - `notebook-hygiene` → installs the full four-layer notebook output enforcement stack
  - `editor-export` → exports reviewed editor JSON state to Moodle XML with explicit status control
