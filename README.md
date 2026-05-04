# moodle-tests

AI-assisted generation, editing, and analysis of Moodle XML quiz exams.

## Components

### Test Generation (`prompts/`)

Prompt-based system for generating multiple-choice exam questions from course materials. The workflow reads source files (`.md`, `.ipynb`, `.py`) from any repository, produces loss-minimizing Stage 1 extraction files, merges them into self-contained subcategory files with explicit question surfaces, and then generates questions one subcategory batch at a time in editor-native JSON. Human review in the editor is mandatory before Moodle XML export.

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

### Step 1: Summarise source materials (one summary per path)

Open `prompts/summarize-sources.prompt.md` as a prompt. Provide:

- **Path(s) to course materials** — can be directories or files in external repos outside this workspace:

  ```text
  #prompt:prompts/summarize-sources.prompt.md

  Summarise the following course materials:
  - /path/to/ml-course/notebooks/01-preprocessing/
  - /path/to/ml-course/notebooks/02-evaluation/
  - /path/to/ml-theory/docs/bias-variance.md
  ```

Preferred for multi-repo or multi-folder subjects: invoke the [`.github/skills/summarize-all-sources/SKILL.md`](.github/skills/summarize-all-sources/SKILL.md) workflow. It fans out one isolated Stage 1 summarization per path and still returns one summary artifact per path.

- **Subject Profile overrides** (optional) — if not stated in the message, the agent will ask.

Each Stage 1 run produces a loss-minimizing extraction file preserving all explanations, processes, cases, comparisons, decision criteria, misconceptions, and examples. Save each output as a `.md` file in a deterministic subject-scoped artifact folder, for example `stage1-summaries/ml/summary-preprocessing.md`.

> **Tip — multiple repos**: Prefer the `summarize-all-sources` skill when you already have a list of paths. It keeps one clean context window per path and still yields one summary file per repo or topic area.
> **Rule — large repos**: If the source material is very large or heterogeneous, split by coherent topic area before extraction. Do not accept a repo-level synopsis as a valid Stage 1 output.

Recommended Stage 1 operating procedure:

- Keep a simple manifest in the same subject folder, for example `stage1-summaries/ml/manifest.md`, with one row per Stage 1 unit and a status such as `pending`, `running`, `done`, or `needs-fix`.
- Fan out only 2 to 4 Stage 1 units at a time. Validate the first batch before launching more work.
- After each batch, run the lightweight checks from [docs/summary_format.md](docs/summary_format.md). In practice this usually means exact H1 section headings, a valid inventory table, and no fenced code blocks.
- If one summary fails validation, stop and repair that file before continuing. Do not send unvalidated Stage 1 artifacts into the merge step.

### Step 2: Merge summaries into subcategory files

Open `prompts/merge-summaries.prompt.md` as a prompt. Provide all summary files from Step 1 and the Moodle category root path (e.g. `$course$/top/MachineLearning`).

The agent proposes a subcategory taxonomy — review and adjust, then it produces **one `.md` file per subcategory**. Each file is self-contained and includes concept IDs, a "Related context" section enabling cross-subcategory questions, and explicit `SURF-*` question surfaces to drive exhaustive downstream generation.

### Step 3: Generate question batches (one subcategory at a time)

Open `prompts/generate-questions.prompt.md` as a prompt. Provide one subcategory `.md` file from Step 2.

The agent generates one coverage-first JSON batch from the file's full content, including scenario-based and cross-subcategory relationship questions, and writes it directly to a deterministic Stage 3 artifact path such as `stage3-question-batches/saa2/ai-foundations-and-learning-paradigms/batch-001.json`. Repeat on the same subcategory with additional `SURF-*` scopes when you want more coverage than fits in one batch; the next run should create the next free batch file in that same subfolder.

> **One subcategory per invocation** — each gets a fresh context window, no drift.
> **One batch per invocation** — keep each output within a safe reviewable window, then continue with more surfaces as needed.

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

- [Adversarial Filters & Prompting Techniques](docs/adversarial_logic_filters.md)
- [Distractor Design & Psychometric Techniques](docs/distractor_design.md)
- [Summary Document Format](docs/summary_format.md)
- [Editor JSON Schema](docs/editor_json_schema.md)
- [Editor Architecture](editor/AGENTS.md)
- [Results Privacy Policy](results/AGENTS.md)
- [Prompt Pipeline Design](prompts/AGENTS.md)

## AI-Assisted Development

This repository uses AI coding assistants as development tools.

- Project-facing instructions live in [AGENTS.md](AGENTS.md).
- Customization-layer docs and maintenance workflows live in [`.github/README.md`](.github/README.md), [`.github/AGENTS.md`](.github/AGENTS.md), and [`.github/docs/README.md`](.github/docs/README.md).
- Prompt design standards live in [`.github/instructions/prompt-authoring.instructions.md`](.github/instructions/prompt-authoring.instructions.md).
- Workspace-level discovery settings live in [`.vscode/settings.json`](.vscode/settings.json).
