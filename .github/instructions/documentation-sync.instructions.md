---
name: Documentation Sync
description: 'Use when updating prompt architecture, quiz-generation workflow, or chat customization files. Keeps README.md, AGENTS.md, prompts/AGENTS.md, and .github/copilot-instructions.md aligned without duplicating canonical documentation.'
applyTo:
  - "prompts/*.prompt.md"
  - ".github/instructions/*.instructions.md"
  - ".github/skills/*/SKILL.md"
  - ".github/agents/*.agent.md"
  - ".github/hooks/*.json"
  - "README.md"
  - "AGENTS.md"
  - "prompts/AGENTS.md"
  - ".github/copilot-instructions.md"
---

# Documentation Sync

- Treat [prompts/AGENTS.md](../../prompts/AGENTS.md) as the canonical description of the prompt pipeline. Update [AGENTS.md](../../AGENTS.md) with a short status summary and discovery links, not a second copy of the full rationale.
- Let this instruction auto-attach both on the sync surfaces and on the prompt/customization files that commonly create drift.
- Keep [README.md](../../README.md) aligned with the active user-facing workflow. If a prompt or workflow becomes deprecated, the README must stop pointing to it as the primary entry point.
- Keep [.github/copilot-instructions.md](../copilot-instructions.md) as a thin compatibility adapter. Update it only when canonical file locations or instruction categories change.
- When adding or removing instructions, skills, hooks, or prompt files, update the customization inventory in [AGENTS.md](../../AGENTS.md) in the same change.
- Prefer links to canonical docs over copying prose from [prompts/AGENTS.md](../../prompts/AGENTS.md), [editor/AGENTS.md](../../editor/AGENTS.md), or [results/AGENTS.md](../../results/AGENTS.md).
