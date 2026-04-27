---
name: Customization Authoring
description: "Use when creating or editing workspace chat customization files such as instructions, agents, and skills."
applyTo:
  - ".github/instructions/*.instructions.md"
  - ".github/agents/*.agent.md"
  - ".github/skills/**/SKILL.md"
---

- Keep canonical project policy in [AGENTS.md](../../AGENTS.md) and module policy in [prompts/AGENTS.md](../../prompts/AGENTS.md), [editor/AGENTS.md](../../editor/AGENTS.md), and [results/AGENTS.md](../../results/AGENTS.md). Link to those sources instead of copying prose into customization files.
- `description` is the discovery surface. Use "Use when..." phrasing with the concrete tasks, file types, or workflows that should cause the customization to load.
- Keep `applyTo` patterns specific. Avoid `**` unless the rule genuinely applies workspace-wide, and re-check the glob after file moves or layout changes.
- Keep adapters thin and workflow-specific files focused on the non-obvious constraints an agent cannot infer quickly from nearby code.
- When adding or removing a customization file, update [AGENTS.md](../../AGENTS.md) in the same change so the inventory stays accurate.