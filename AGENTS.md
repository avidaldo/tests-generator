# Moodle Tests — Agent Instructions

## General Instructions

- Be critical. Don't praise the user. Point out issues, mistakes, and problems in their messages and actions. Provide analysis of pros and cons of different options. If the user asks for advice, provide it with detailed reasoning.
- Be proactive. If you identify a problem or an opportunity for improvement, suggest it to the user. Don't wait for the user to ask for help or advice.
- Write in a direct, dense style. Avoid fluff, filler, and unnecessary politeness. Be clear and concise.
- When asked to produce content, focus on quality over quantity. It's better to produce a few high-quality items than many low-quality ones.
- Careful analysis or architecture and software design good practices is paramount in order to create a modular and scalable project and therefore avoid context problems in the future.
- Same applies for the customization architecture. It is important to keep it clean and well defined in order to avoid confusion, miscommunication, and technical debt in the future. Constant reminders of the rationale behind it and the working agreements are key for keeping it healthy.

## Planning And Living Documentation

- `TODO:` is the default inline capture marker. Prefer low-friction capture over elaborate inline taxonomies.
- `docs/implementation_plan.md` is the curated active plan. Question-style TODOs must be moved there as Clarification Queue entries before implementation starts.
- Use the `todo-planner` custom agent to refresh the plan and surface unresolved questions before larger changes.
- Use the `sdd-implementer` custom agent or the standard coding agent only after the relevant plan item is approved.
- When a change affects architecture, workflow, or agent behavior, update the relevant docs and instruction files in the same change.
- Canonical rationale for this split lives in [docs/customization_architecture.md](docs/customization_architecture.md).

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
| `docs/` | Domain knowledge, design documentation, and living customization records; see [`docs/customization_architecture.md`](docs/customization_architecture.md) and [`docs/agentic_enforcement_layers.md`](docs/agentic_enforcement_layers.md) | — |
| `resources/` | Utility scripts (XML conversion, merging) | [`.github/instructions/resources.instructions.md`](.github/instructions/resources.instructions.md) |
| `samples/` | Example Moodle XML files | [`.github/instructions/xml-moodle.instructions.md`](.github/instructions/xml-moodle.instructions.md) |

## Language Convention

- **Development language:** English — all code, documentation, instructions, agent prompts, and filenames are written in English.
- **Test output language:** Generated exams are in **Castellano** (Spanish) by default, with technical terms in English in parentheses. This is configurable via the **Subject Profile** in both prompt files — the user can override the output language at invocation time.
<!-- TODO: Even when I'll generate them in spanish, I think is more coherent for reusability of this repo that the default is generating questions in the same language. Anyway, that will be defined by the instructions of that step, so is it needed here? -->
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

## Planning Workflow

- Capture open work locally with `TODO:` markers.
- Refresh `docs/implementation_plan.md` with the `todo-planner` custom agent before coding when the task touches multiple files, unresolved design questions, or existing TODOs.
- Resolve Clarification Queue items with the user before implementation.
- Implement one approved item at a time, then sync the plan and any affected docs or instructions before finishing.

## VS Code Customization Layout

- Keep `AGENTS.md` files as the canonical cross-agent instruction surface. Root and subfolder `AGENTS.md` files are both loaded by VS Code (`chat.useNestedAgentsMdFiles`).
- Keep `prompts/*.prompt.md` as the canonical prompt files; discovered via `chat.promptFilesLocations` in `.vscode/settings.json`.
- `chat.useCustomAgentHooks` is enabled in `.vscode/settings.json` so planner-only guard rails can live with the custom agent that needs them.
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
- Use `.github/agents/*.agent.md` for custom agents; current agents:
  - `todo-planner` → planning-only agent for TODO triage, clarification, and `docs/implementation_plan.md` refresh
  - `sdd-implementer` → implementation agent for one approved plan item at a time, with doc sync before finish
- Use `.github/hooks/*.json` + scripts for deterministic agent-time enforcement (PostToolUse, PreToolUse); current hooks:
  - `strip-notebook-outputs.json` → strips `.ipynb` outputs after any agent file write
  - `prompt-doc-drift-check.json` → warns when prompt/customization changes may need documentation-sync updates
  - `living-docs-drift-check.json` → warns when source edits have no matching plan or documentation updates
- Use `.github/skills/<name>/SKILL.md` for portable, on-demand multi-step workflows; current skills:
  - `todo-analysis` → triages TODOs into a lightweight implementation plan with a clarification queue
  - `notebook-hygiene` → installs the full four-layer notebook output enforcement stack
  - `editor-export` → exports reviewed editor JSON state to Moodle XML with explicit status control
