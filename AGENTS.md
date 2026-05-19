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
- `.github/implementation_plan.md` is the curated active plan. Question-style TODOs must be moved there as Clarification Queue entries before implementation starts.
- Use [`.github/prompts/refresh-plan.prompt.md`](.github/prompts/refresh-plan.prompt.md) to refresh the plan and surface unresolved questions before larger changes.
- Use [`.github/prompts/implement-plan-item.prompt.md`](.github/prompts/implement-plan-item.prompt.md) after the relevant plan item is approved.
- When a change affects architecture, workflow, or agent behavior, update the relevant docs and instruction files in the same change.
- Canonical rationale for this split lives in [`.github/docs/customization_architecture.md`](.github/docs/customization_architecture.md).

## Project Overview

This repository contains tools and prompts for generating, editing, and analyzing Moodle XML quiz exams using AI assistance.

## Repository Structure

| Path | Purpose | Instructions |
| ---- | ------- | ------------ |
| `prompts/` | Canonical question-generation prompt files (`.prompt.md`) | [`prompts/AGENTS.md`](prompts/AGENTS.md) |
| `.github/prompts/` | Repository-maintenance prompt launchers for the SDD loop | [`.github/prompts/AGENTS.md`](.github/prompts/AGENTS.md) |
| `.github/instructions/` | VS Code file-scoped instruction adapters (`.instructions.md`) | [`AGENTS.md`](AGENTS.md) |
| `.github/` | VS Code customization layer: agents, prompts, hooks, and living customization docs | [`.github/AGENTS.md`](.github/AGENTS.md) |
| `editor/` | PyQt-based Stage 4 review editor with secondary legacy XML import | [`editor/AGENTS.md`](editor/AGENTS.md) |
| `results/` | Exam result analysis notebooks | [`results/AGENTS.md`](results/AGENTS.md) |
| `docs/` | Domain knowledge and project-facing documentation; see [`docs/editor_json_schema.md`](docs/editor_json_schema.md), [`docs/summary_format.md`](docs/summary_format.md), [`docs/adversarial_logic_filters.md`](docs/adversarial_logic_filters.md), and [`docs/distractor_design.md`](docs/distractor_design.md) | — |
| `resources/` | Utility scripts (XML conversion, merging) | [`.github/instructions/resources.instructions.md`](.github/instructions/resources.instructions.md) |
| `samples/` | Example Moodle XML files | [`.github/instructions/xml-moodle.instructions.md`](.github/instructions/xml-moodle.instructions.md) |

## Language Convention

- **Development language:** English — all code, documentation, instructions, agent prompts, and filenames are written in English.
- **Test output language:** Set at question-generation time via the **Output language** parameter in the `generate-questions.prompt.md` Subject Profile. Default is the **source corpus language** (inferred from the Stage 2 subcategory file). When the user did not specify a language, Stage 3 should explicitly offer **Castellano** (Spanish) as the usual target before generating. Summarisation and merge stages preserve the source material's language. For translated Stage 3 output, keep domain-standard technical terms in English, or include the English term in parentheses when translated.
- **Sample files:** `samples/` XMLs contain Spanish content as examples of expected output — their content is intentionally Spanish.
- **Result notebooks:** Analysis notebooks (`results/`) are in English. Column names from the raw Spanish CSV export are kept as-is in code.

## Critical Rules (All Agents)

1. **Student data privacy**: Never output, commit, or log student names, emails, or grades. The `results/data/` directory is gitignored.
2. **Notebook outputs**: For same reason, `.ipynb` files must be committed without cell outputs. The repo uses `nbstripout` as a git filter (`.gitattributes`).
3. **Domain docs**: Consult `docs/` before generating or reviewing quiz content. Particularly `docs/adversarial_logic_filters.md` for the adversarial filter mechanism and `docs/distractor_design.md` for distractor strategies and psychometric techniques.

## Prompt Pipeline

See [`prompts/AGENTS.md`](prompts/AGENTS.md) for the active prompt inventory, pipeline diagram, design rationale, and file responsibilities. See [`docs/pipeline_execution_modes.md`](docs/pipeline_execution_modes.md) for the execution-mode decision guide and the user-owned artifact path contract.

Active workflow: `summarize-sources.prompt.md` (loss-minimizing Stage 1 extraction, one per repo or coherent topic area; split large corpora first) → `merge-summaries.prompt.md` (subcategory files with concept IDs, question surfaces, and cross-cutting context) → `generate-questions.prompt.md` (one subcategory batch per invocation) → editor review session → XML export.

For multi-repo subjects, the optional [`summarize-all-sources` skill](.github/skills/summarize-all-sources/SKILL.md) can fan out Stage 1 into one isolated summarization per path before the merge step.

For delegated or background Stage 3 breadth-first runs, the optional [`generate-question-batches` skill](.github/skills/generate-question-batches/SKILL.md) can traverse multiple subcategory files and create at most one new batch per subcategory while keeping checkpointed progress under a user-provided Stage 3 root.

For approved Stage 2 scopes that need repeated successive Stage 3 batches until tracked `SURF-*` coverage is exhausted, the preferred user-facing surface is [`prompts/finish-stage3-coverage.prompt.md`](prompts/finish-stage3-coverage.prompt.md). It reuses the optional [`finish-question-coverage` skill](.github/skills/finish-question-coverage/SKILL.md) as the execution lane while keeping a coverage manifest under the user-provided Stage 3 root.

Stage 1 operational policy in this repo:

- Prompts should ask for missing input/output paths instead of assuming artifacts live under this repository.
- Prefer deterministic filenames under a user-provided subject-owned root, such as `summary-<unit>.md` for Stage 1 and `<subcategory>/batch-001.json` for Stage 3.
- Keep a manifest or checkpoint file in the user-provided Stage 1 root for each subject run.
- Fan out in small batches and validate each written artifact against [docs/summary_format.md](docs/summary_format.md) before launching more units or starting Stage 2.

Each step is run manually. See the [Usage guide in README.md](README.md#usage-generating-exam-questions) for step-by-step instructions.

## Practical Commands

- Sync Python dependencies with `uv sync`.
- Run the editor with `uv run python editor/main.py`.
- Export a reviewed Stage 4 review-session JSON to Moodle XML with `python resources/json_to_moodle_xml.py <input.json> <output.xml>`.
- Verify the notebook output filter is active with `nbstripout --status`.

## Planning Workflow

- Capture open work locally with `TODO:` markers.
- Refresh `.github/implementation_plan.md` with [`.github/prompts/refresh-plan.prompt.md`](.github/prompts/refresh-plan.prompt.md) before coding when the task touches multiple files, unresolved design questions, or existing TODOs.
- Resolve Clarification Queue items with the user before implementation.
- Implement one approved item at a time with [`.github/prompts/implement-plan-item.prompt.md`](.github/prompts/implement-plan-item.prompt.md), then sync the plan and any affected docs or instructions before finishing.
- For long unattended delegated or cloud-oriented runs, [`.github/prompts/run-batch-maintenance.prompt.md`](.github/prompts/run-batch-maintenance.prompt.md) is the advanced optional lane. It processes approved and unblocked items iteratively but does not replace the canonical safe loop.

## VS Code Customization Layer

- The optional [`customization-audit` skill](.github/skills/customization-audit/SKILL.md) compares this repo's `.github` customization files against current VS Code customization docs and reports drift or deprecated patterns.
- The optional [`finish-question-coverage` skill](.github/skills/finish-question-coverage/SKILL.md) provides the advanced Stage 3 exhaustive-coverage lane for approved Stage 2 scopes that need repeated successive batches.
- The optional [`generate-question-batches` skill](.github/skills/generate-question-batches/SKILL.md) provides the advanced Stage 3 bulk lane for delegated or background question generation across multiple subcategories.
- The detailed customization inventory now lives in [`.github/AGENTS.md`](.github/AGENTS.md).
- The human-oriented customization guide now lives in [`.github/README.md`](.github/README.md).
- Maintenance prompt policy now lives in [`.github/prompts/AGENTS.md`](.github/prompts/AGENTS.md).
- Stage 3 question-design rules live in [`prompts/generate-questions.prompt.md`](prompts/generate-questions.prompt.md) and the linked domain docs rather than in a prompt-specific `.github/instructions/` adapter.
- Root `prompts/` remains reserved for the quiz-generation pipeline and stays enabled through `.vscode/settings.json`.
- Keep this root file focused on project-facing policy and discovery; do not duplicate the full customization inventory here.
