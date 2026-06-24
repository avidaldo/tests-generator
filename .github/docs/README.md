# Customization Docs

This folder contains durable design rationale and decision records for the repository's VS Code and Copilot customization layer.

## Scope

- Keep stable customization rationale here.
- Keep case studies and enforcement-pattern writeups here.
- Add future decision records here when the customization layer grows enough to justify them.

## Operational Surfaces Kept At `.github/` Root

- [`../README.md`](../README.md) — human-oriented entry point for the customization layer.
- [`../AGENTS.md`](../AGENTS.md) — customization-layer policy and inventory.

## Current Documents

- [customization_architecture.md](customization_architecture.md) — rationale for the prompt, agent, skill, hook, and documentation split.
- [agentic_enforcement_layers.md](agentic_enforcement_layers.md) — case study for multi-layer enforcement design.
