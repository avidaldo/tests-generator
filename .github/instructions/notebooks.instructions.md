---
name: Notebook Authoring
description: Jupyter notebook authoring conventions and student data privacy rules.
applyTo: "**/*.ipynb"
---

Canonical notebook hygiene and privacy policy live in [results/AGENTS.md](../../results/AGENTS.md).

**Privacy (critical):** Never commit cell outputs — they may contain student data. Run `nbstripout *.ipynb` before pushing. CI will block the PR if outputs are present.

Authoring conventions:

- Go step by step: each cell shows its own output; markdown cells explain the steps.
- Headings in their own dedicated markdown cells (enables fold/unfold). Do not number headings.
- Imports in the first cell that needs them, not a global imports cell at the top.
- Explanations in markdown cells — never in prints or code-cell comments.
- Comments in code cells explain specific lines or blocks only.
- Small, focused cells. Avoid multiple figures as output of the same cell.
