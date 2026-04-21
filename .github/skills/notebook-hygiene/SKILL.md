---
name: notebook-hygiene
description: Install all four enforcement layers for notebook output hygiene in a new project. Use when setting up notebook privacy controls, nbstripout integration, CI output checks, or agent hooks for .ipynb files.
---

# Notebook Hygiene Installer

This skill installs the full four-layer enforcement stack for notebook output hygiene (see [`docs/agentic_enforcement_layers.md`](../../../docs/agentic_enforcement_layers.md) for the full architectural rationale and tradeoff analysis).

## What This Skill Installs

1. **Always-on instruction** — tells the AI agent about the privacy rule and notebook authoring conventions whenever a `.ipynb` file is in scope.
2. **Agent-time hook** — auto-strips cell outputs whenever the agent writes a `.ipynb` file (`PostToolUse`).
3. **Local git filter** — strips outputs at commit time for human developers (requires one-time setup per developer).
4. **CI check** — blocks pushes and pull requests that contain notebook outputs.

## Installation Steps

### Step 1 — Always-on instruction

Copy `.github/instructions/notebooks.instructions.md` into the target repository. Update the `applyTo` pattern if notebooks are only in a subfolder. Update the link to the privacy policy canonical source if your project uses a different file.

### Step 2 — Agent-time hook

Copy `.github/hooks/strip-notebook-outputs.json` and `.github/hooks/strip_notebook_outputs.py` into the target repository, preserving the directory structure.

Ensure `nbstripout` is available in the agent's runtime:

```bash
pip install nbstripout
```

### Step 3 — Local git filter

Add to `.gitattributes` (create if it does not exist):

```
*.ipynb filter=nbstripout
*.ipynb diff=ipynb
```

Instruct every developer to run once after cloning:

```bash
pip install nbstripout
nbstripout --install --attributes .gitattributes
```

Verify the filter is active:

```bash
nbstripout --status
```

### Step 4 — CI check

Copy `.github/workflows/check-notebooks.yml` into the target repository. No changes are needed for a standard GitHub Actions setup. Adjust the `paths` filter if notebooks live in a specific subfolder.

## Verification

- Run `nbstripout --status` to confirm the local git filter is active.
- Open a notebook in the agent, make an edit, and confirm the file has no outputs after the agent writes it (Layer 2 hook).
- Commit a notebook that has outputs and confirm it is stripped before reaching the staging area (Layer 3).
- Push a notebook with outputs (temporarily bypass the filter with `git add --no-filters`) and confirm CI rejects it (Layer 4).
