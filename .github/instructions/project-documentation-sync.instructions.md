---
name: Project Documentation Sync
description: 'Use when updating quiz-generation workflow or project-facing docs. Keeps README.md, AGENTS.md, and prompts/AGENTS.md aligned without duplicating canonical project documentation.'
applyTo:
  - "README.md"
  - "AGENTS.md"
  - "prompts/AGENTS.md"
  - "prompts/*.prompt.md"
---

# Project Documentation Sync

- Treat [prompts/AGENTS.md](../../prompts/AGENTS.md) as the canonical description of the quiz-generation prompt pipeline.
- Keep [README.md](../../README.md) aligned with the active question-generation workflow.
- Keep [AGENTS.md](../../AGENTS.md) as the project-facing policy and discovery surface. Customization-layer detail belongs in [AGENTS.md](../AGENTS.md) and [README.md](../README.md).
- When changing project prompt routing, verify that `.vscode/settings.json` still exposes the root `prompts/` folder as intended.
- Prefer links to canonical docs over copying prose from [prompts/AGENTS.md](../../prompts/AGENTS.md), [editor/AGENTS.md](../../editor/AGENTS.md), or [results/AGENTS.md](../../results/AGENTS.md).