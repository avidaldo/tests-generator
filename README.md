# moodle-tests

AI-assisted generation, editing, and analysis of Moodle XML quiz exams.

## Components

### Test Generation (`prompts/`)

Prompt-based system for generating multiple-choice exam questions in Moodle XML format from course materials. Focuses on conceptual understanding over syntax recall, with adversarial validation of distractors.

See: [`prompts/generate-test.prompt.md`](prompts/generate-test.prompt.md)

### Quiz Editor (`editor/`)

Desktop application (PyQt) for viewing and editing Moodle XML question banks. Supports undo/redo, drag-and-drop reordering, and category management.

See: [`editor/v3/README.md`](editor/v3/README.md)

### Results Analysis (`results/`)

Jupyter notebooks for analyzing exam outcomes: difficulty indices, score distributions, penalty impact, and pass-rate scenarios.

> **Warning:** Raw student data (`results/data/`) is **gitignored** and must
> never be committed. Notebooks must be committed **without outputs**.

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

- [Adversarial Filters & Distractor Design](docs/adversarial_logic_filters.md)
- [Editor Architecture](editor/AGENTS.md)
- [Results Privacy Policy](results/AGENTS.md)
- [Prompt Design And Decomposition Notes](prompts/AGENTS.md)

## AI-Assisted Development

This repository uses GitHub Copilot as a development tool. See [`AGENTS.md`](AGENTS.md) for cross-agent instructions, [`prompts/metaprompting.prompt.md`](prompts/metaprompting.prompt.md) for prompt design standards, and [`.vscode/settings.json`](.vscode/settings.json) for the workspace-level VS Code prompt discovery adapter.
