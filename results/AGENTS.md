# Results Analysis — Agent Instructions

## Canonical Scope

This file is the canonical, tool-agnostic instruction surface for the `results/` module.

- Keep `.github/instructions/results.instructions.md` as a VS Code routing adapter only, not as a second source of results policy.

## Critical Rule: Student Data Privacy

**NEVER commit, output, or include student personal data** (names, emails, grades, identifiers) in any generated content, commit message, pull request, or conversation output.

## Notebook Hygiene

- All notebooks in this folder MUST have their outputs stripped before commit.
- The repository uses `nbstripout` as a git filter (configured in `.gitattributes`). Verify it is active with: `nbstripout --status`.
- A GitHub Actions workflow (`.github/workflows/check-notebooks.yml`) **blocks pushes and PRs** that contain notebook outputs. This is the server-side safety net.
- If you create or modify a notebook, ensure no cell outputs containing student data survive into version control.
- The `data/` subdirectory is gitignored entirely. Never remove it from `.gitignore`.

## Scope

These notebooks analyze exam results (question difficulty, pass-rate scenarios, penalty analysis). They consume CSV exports from Moodle located in `data/` (gitignored).

## Conventions

- Notebooks are numbered sequentially by analysis stage.
- Each notebook should be self-contained with a Markdown header explaining its purpose and expected input files.
- Follow the Jupyter Notebooks Guidelines defined in the root `AGENTS.md`.

## Notebook Authoring Rules

- Build notebooks step by step with small cells, markdown explanations, and headings in their own markdown cells.
- Import dependencies in the first cell that needs them rather than in a global imports cell.
- Keep raw Spanish CSV column names unchanged in analysis code unless there is an explicit migration task.
