---
name: Customization Documentation Sync
description: 'Use when updating maintenance prompts, custom agents, customization docs, or instruction files. Keeps the .github customization layer aligned without duplicating canonical documentation.'
applyTo:
  - ".github/README.md"
  - ".github/AGENTS.md"
  - ".github/prompts/AGENTS.md"
  - ".github/prompts/*.prompt.md"
  - ".github/agents/*.agent.md"
  - ".github/instructions/*.instructions.md"
  - ".github/skills/**/SKILL.md"
  - ".github/docs/*.md"
  - ".github/*.md"
---

# Customization Documentation Sync

- Treat [AGENTS.md](../AGENTS.md) as the canonical customization inventory and [customization_architecture.md](../docs/customization_architecture.md) as the canonical rationale.
- Treat [prompts/AGENTS.md](../prompts/AGENTS.md) as the canonical maintenance prompt inventory.
- Keep [README.md](../README.md) human-oriented and keep [copilot-instructions.md](../copilot-instructions.md) as a thin VS Code adapter.
- When adding or removing customization files, update [AGENTS.md](../AGENTS.md), the short customization summary in [AGENTS.md](../../AGENTS.md), and any affected prompt-discovery settings in `.vscode/settings.json`.
- Link back to root project docs when you need domain knowledge; do not copy quiz-generation rationale into customization-layer files.