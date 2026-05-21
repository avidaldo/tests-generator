# moodle-tests

AI-assisted generation, editing, and analysis of Moodle XML quiz exams.

## Components

### Test Generation (`prompts/`)

Prompt-based system for generating multiple-choice exam questions from course materials. The workflow reads source files (`.md`, `.ipynb`, `.py`) from any repository, produces loss-minimizing Stage 1 extraction files, merges them into self-contained subcategory files with explicit question surfaces, and then generates questions one subcategory batch at a time in editor-native JSON. Human review in the editor is mandatory before Moodle XML export.

Active workflow: [`prompts/summarize-sources.prompt.md`](prompts/summarize-sources.prompt.md) → [`prompts/merge-summaries.prompt.md`](prompts/merge-summaries.prompt.md) → [`prompts/generate-questions.prompt.md`](prompts/generate-questions.prompt.md)

See [`prompts/AGENTS.md`](prompts/AGENTS.md) for the full pipeline diagram, design rationale, and deprecated prompts. See [`docs/pipeline_execution_modes.md`](docs/pipeline_execution_modes.md) for when to use the regular prompt-by-prompt lane versus the Stage 1 and Stage 3 orchestration skills, and for the user-owned artifact path contract.

### Quiz Editor (`editor/`)

Desktop application (PyQt) for Stage 4 review of generated question batches. The primary workflow imports one or more Stage 3 JSON batches into a consolidated review session, then exports approved questions to Moodle XML. Legacy XML import remains available for older banks. Stage 3 generation intentionally starts with 6 distractors per question so review has room to prune weak ones; reviewed Stage 4 questions often finish with 3 distractors before export. The editor allows reviewing, editing, and categorizing questions before export. It supports undo/redo, drag-and-drop reordering, and category management.

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

Preferred for multi-repo or multi-folder subjects:
- **In-session**: invoke the [`.github/skills/summarize-all-sources/SKILL.md`](.github/skills/summarize-all-sources/SKILL.md) workflow. It fans out one isolated Stage 1 summarization per path and still returns one summary artifact per path.
- **Background / Copilot CLI**: select the [`stage1-runner` agent](.github/agents/stage1-runner.agent.md). It delegates each path to an isolated `source-summarizer` subagent in small parallel batches and persists when VS Code closes.

- **Subject Profile overrides** (optional) — if not stated in the message, the agent will ask.
- **Stage 1 output location** — provide either a subject-owned Stage 1 output root or an explicit output file path for the current unit. If you omit it, the agent should ask before writing.

Each Stage 1 run produces a loss-minimizing extraction file preserving all explanations, processes, cases, comparisons, decision criteria, misconceptions, and examples. Save each output as a `.md` file in a user-owned artifact location, for example `/path/to/exam-artifacts/ml/stage1/summary-preprocessing.md`.

> **Tip — multiple repos**: Prefer the `summarize-all-sources` skill when you already have a list of paths. It keeps one clean context window per path and still yields one summary file per repo or topic area.
> **Rule — large repos**: If the source material is very large or heterogeneous, split by coherent topic area before extraction. Do not accept a repo-level synopsis as a valid Stage 1 output.

Recommended Stage 1 operating procedure:

- Keep a simple manifest in the same Stage 1 root, for example `/path/to/exam-artifacts/ml/stage1/manifest.md`, with one row per Stage 1 unit and a status such as `pending`, `running`, `done`, or `needs-fix`.
- Fan out only 2 to 4 Stage 1 units at a time. Validate the first batch before launching more work.
- After each batch, run the lightweight checks from [docs/summary_format.md](docs/summary_format.md). In practice this usually means exact H1 section headings, a valid inventory table, and no fenced code blocks.
- If one summary fails validation, stop and repair that file before continuing. Do not send unvalidated Stage 1 artifacts into the merge step.

### Step 2: Merge summaries into subcategory files

Open `prompts/merge-summaries.prompt.md` as a prompt. Provide all summary files from Step 1, the Moodle category root path (e.g. `$course$/top/MachineLearning`), and a Stage 2 output root for the generated subcategory files.

The agent proposes a subcategory taxonomy — review and adjust, then it produces **one `.md` file per subcategory** in that Stage 2 output location. Each file is self-contained and includes concept IDs, a "Related context" section enabling cross-subcategory questions, and explicit `SURF-*` question surfaces to drive exhaustive downstream generation.

### Step 3: Generate question batches (one subcategory at a time)

Open `prompts/generate-questions.prompt.md` as a prompt when you want one subcategory at a time. Provide one subcategory `.md` file from Step 2 and either a Stage 3 output root or an explicit batch file path.

The agent generates one coverage-first JSON batch from the file's full content, including scenario-based and cross-subcategory relationship questions, and writes it directly to a user-owned Stage 3 location such as `/path/to/exam-artifacts/saa2/stage3/ai-foundations-and-learning-paradigms/batch-001.json`. If the run already knows one stable model label for that batch, provide it once and the batch should write that same value into `generated_by_model` for every question. Repeat on the same subcategory with additional `SURF-*` scopes when you want more coverage than fits in one batch; the next run should create the next free batch file in that same subfolder.

Preferred for delegated or background breadth-first runs across many subcategories:
- **In-session breadth-first**: invoke the [`.github/skills/generate-question-batches/SKILL.md`](.github/skills/generate-question-batches/SKILL.md) workflow. It creates at most one new batch per subcategory per pass, keeps checkpointed progress under the Stage 3 root, and can reuse one shared model label per written batch.
- **In-session exhaustive**: open [`prompts/finish-stage3-coverage.prompt.md`](prompts/finish-stage3-coverage.prompt.md) — accepts `@file:` folder attachment or the form field.
- **Background / Copilot CLI**: select the [`stage3-runner` agent](.github/agents/stage3-runner.agent.md). It delegates each subcategory to an isolated `batch-generator` subagent (one clean context window per subcategory) and persists when VS Code closes.

Preferred single-step autopilot for an already approved Stage 2 scope (in-session): open [`prompts/finish-stage3-coverage.prompt.md`](prompts/finish-stage3-coverage.prompt.md). It is the project-facing launcher for exhaustive Stage 3 runs, can reuse one shared model label per written batch, and keeps generating successive batches until tracked `SURF-*` coverage is exhausted.

The underlying implementation lane for that launcher remains [`.github/skills/finish-question-coverage/SKILL.md`](.github/skills/finish-question-coverage/SKILL.md). It is still Stage-3-only: it does not invent missing Stage 2 files, and it relies on a coverage manifest under the Stage 3 root.

> **One subcategory per invocation** — each gets a fresh context window, no drift.
> **One batch per invocation** — keep each output within a safe reviewable window, then continue with more surfaces as needed.

### Step 4: Human review in the editor

```bash
uv run python editor/main.py
```

Start a new review session, add one or more generated Stage 3 batch JSON files with `Archivo -> Añadir -> Archivos Stage 3...` or `Ctrl+O`, or add a whole Stage 3 root recursively with `Archivo -> Añadir -> Carpeta Stage 3...`. Open saved Stage 4 work with `Archivo -> Abrir sesión de revisión...`, save it with `Guardar sesión` or `Guardar sesión como...`, and use `Archivo -> Añadir -> Legado -> Banco XML de Moodle...` only for older XML banks. Review each question:

- **Pendiente** → not yet reviewed
- **Revisar** → needs changes
- **Lista** → approved for export

Imported Stage 3 questions start with 7 answers total. During Stage 4 review it is valid to prune distractors; a reviewed 4-answer question is a normal final state, not a schema error.

If a Stage 3 batch includes `generated_by_model`, the editor preserves that question-level model label through the review session and shows it in the question provenance metadata.

The editor also shows non-blocking warning markers when the correct option looks substantially longer or shorter than the distractors after visible-text normalization. Treat those warnings as review aids, not as export blockers.

### Step 5: Export to Moodle XML

The normal manual path is `Archivo -> Exportar -> Moodle XML...` inside the editor. Only questions marked `lista` are exported.

For scripted conversion of a saved review-session JSON file, you can also use:

```bash
python resources/json_to_moodle_xml.py review-session.json exam.xml
```

Import the resulting XML into Moodle.

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
- [Editor Workflow](editor/docs/WORKFLOW.md)
- [Editor Import And Export Guide](editor/docs/IMPORT_EXPORT.md)
- [Pipeline Execution Modes](docs/pipeline_execution_modes.md)
- [Editor Architecture](editor/AGENTS.md)
- [Results Privacy Policy](results/AGENTS.md)
- [Prompt Pipeline Design](prompts/AGENTS.md)

## AI-Assisted Development

This repository uses AI coding assistants as development tools.

- Project-facing instructions live in [AGENTS.md](AGENTS.md).
- Customization-layer docs and maintenance workflows live in [`.github/README.md`](.github/README.md), [`.github/AGENTS.md`](.github/AGENTS.md), and [`.github/docs/README.md`](.github/docs/README.md).
- Prompt design standards live in [`.github/instructions/prompt-authoring.instructions.md`](.github/instructions/prompt-authoring.instructions.md).
- Workspace-level discovery settings live in [`.vscode/settings.json`](.vscode/settings.json).


