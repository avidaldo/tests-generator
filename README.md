# moodle-tests

AI-assisted generation, editing, and analysis of Moodle XML quiz exams.

## Components

### Test Generation (`prompts/`)

Prompt-based system for generating multiple-choice exam questions from course materials. The workflow reads source files (`.md`, `.ipynb`, `.py`) from any repository, produces rich content summaries, merges them into self-contained subcategory files, and then generates questions one subcategory at a time in editor-native JSON. Human review in the editor is mandatory before Moodle XML export.

Active workflow: [`prompts/summarize-sources.prompt.md`](prompts/summarize-sources.prompt.md) → [`prompts/merge-summaries.prompt.md`](prompts/merge-summaries.prompt.md) → [`prompts/generate-questions.prompt.md`](prompts/generate-questions.prompt.md)

See [`prompts/AGENTS.md`](prompts/AGENTS.md) for the full pipeline diagram, design rationale, and deprecated prompts.

### Quiz Editor (`editor/`)

Desktop application (PyQt) for viewing and editing Moodle XML question banks. Generated questions are created with 6 distractors each, since the distractor design strategy is to generate more than needed and then review. The editor allows reviewing, editing, and categorizing questions before export. It supports undo/redo, drag-and-drop reordering, and category management.

See: [`editor/README.md`](editor/README.md)

### Results Analysis (`results/`)

Jupyter notebooks for analyzing exam outcomes: difficulty indices, score distributions, penalty impact, and pass-rate scenarios.

> **Warning:** Raw student data (`results/data/`) is **gitignored** and must
> never be committed. Notebooks must be committed **without outputs**.

## Usage: Generating Exam Questions

### Prerequisites

- An AI coding assistant with prompt file support (VS Code + Copilot, or equivalent)
- Course materials in one or more repositories (`.md`, `.ipynb`, `.py` files)
- This repository cloned locally

### Step 1: Summarise source materials (one per repo)

Open `prompts/summarize-sources.prompt.md` as a prompt. Provide:

- **Path(s) to course materials** — can be directories or files in external repos outside this workspace:

  ```text
  #prompt:prompts/summarize-sources.prompt.md

  Summarise the following course materials:
  - /path/to/ml-course/notebooks/01-preprocessing/
  - /path/to/ml-course/notebooks/02-evaluation/
  - /path/to/ml-theory/docs/bias-variance.md
  ```
<!-- TODO: Shouldn't a subagent be used for each material, to avoid overloading the context and paralelize? wouldn't that be better for performance and scalability? -->

- **Subject Profile overrides** (optional) — if not stated in the message, the agent will ask.

The agent produces a rich content summary preserving all explanations, processes, cases, and examples. **Save it as a `.md` file** (e.g. `summary-ml-preprocessing.md`).

> **Tip — multiple repos**: Run once per repo or topic area. Each run gets a clean context window. You'll have one summary file per repo.
> **Tip — large repos**: If the source material is very large (>100 pages), split by topic area.

### Step 2: Merge summaries into subcategory files

Open `prompts/merge-summaries.prompt.md` as a prompt. Provide all summary files from Step 1 and the Moodle category root path (e.g. `$course$/top/MachineLearning`).

The agent proposes a subcategory taxonomy — review and adjust, then it produces **one `.md` file per subcategory**. Each file is self-contained and includes a "Related context" section enabling cross-subcategory questions.

### Step 3: Generate questions (one subcategory at a time)

Open `prompts/generate-questions.prompt.md` as a prompt. Provide one subcategory `.md` file from Step 2.

The agent generates questions from the file's full content, including scenario-based and cross-subcategory relationship questions. Output is a JSON file — save it (e.g. `ml-normalisation.json`).

> **One subcategory per invocation** — each gets a fresh context window, no drift.

### Step 4: Human review in the editor

```bash
uv run python editor/main.py
```

Open the JSON file (`Ctrl+O`). Review each question:

- **Pendiente** → not yet reviewed
- **Revisar** → needs changes
- **Lista** → approved for export

### Step 5: Export to Moodle XML

```bash
python resources/json_to_moodle_xml.py ml-normalisation.json ml-normalisation.xml
```

Only questions marked `lista` are exported. Import the XML into Moodle.

## Setup

### Mandatory: notebook output stripping

This repository contains analysis of student exam results. **Raw outputs must never be committed.** A GitHub Actions CI check will reject any push or PR containing notebook cell outputs.

The project uses a two-layer defense:

1. Local filtering with `nbstripout` to strip outputs before commit.
2. Server-side CI verification to block outputs that still reach a push or PR.

To auto-strip outputs locally on every commit:

```bash
pip install nbstripout
nbstripout --install --attributes .gitattributes
```

Verify the filter is active: `nbstripout --status`

### Editor dependencies (optional)

```bash
pip install PyQt6 lxml
```

## Documentation

- [Customization Architecture](docs/customization_architecture.md)
- [Implementation Plan](docs/implementation_plan.md)
- [Adversarial Filters & Prompting Techniques](docs/adversarial_logic_filters.md)
- [Distractor Design & Psychometric Techniques](docs/distractor_design.md)
- [Summary Document Format](docs/summary_format.md)
- [Agentic Enforcement Layers](docs/agentic_enforcement_layers.md)
- [Editor Architecture](editor/AGENTS.md)
- [Results Privacy Policy](results/AGENTS.md)
- [Prompt Pipeline Design](prompts/AGENTS.md)

## AI-Assisted Development

This repository uses AI coding assistants as development tools. See [`AGENTS.md`](AGENTS.md) for cross-agent instructions, [`docs/customization_architecture.md`](docs/customization_architecture.md) for the current customization design, [`.github/instructions/prompt-authoring.instructions.md`](.github/instructions/prompt-authoring.instructions.md) for prompt design standards, and [`.vscode/settings.json`](.vscode/settings.json) for the workspace-level VS Code customization settings.

### Planning Loop

The development workflow is intentionally simple:

1. Capture local doubts or pending work as `TODO:` comments.
2. Refresh [`docs/implementation_plan.md`](docs/implementation_plan.md) with [`prompts/refresh-plan.prompt.md`](prompts/refresh-plan.prompt.md).
3. Resolve Clarification Queue items before coding.
4. Implement one approved item at a time with [`prompts/implement-plan-item.prompt.md`](prompts/implement-plan-item.prompt.md).
5. Update the plan and the relevant docs or instructions in the same change.

The underlying `todo-planner`, `sdd-implementer`, and `todo-analysis` customizations still exist, but they are runtime layers behind the prompt launchers rather than the primary UI entry points.
