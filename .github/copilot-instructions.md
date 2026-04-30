# Moodle Tests — VS Code Adapter

This file is a thin GitHub Copilot and VS Code compatibility adapter.

[AGENTS.md](../AGENTS.md) is the primary instruction source for project-wide policy. [AGENTS.md](AGENTS.md) is the primary instruction source for the customization layer. Subfolder `AGENTS.md` files (`.github/prompts/`, `editor/`, `results/`, `prompts/`) are also loaded automatically via `chat.useNestedAgentsMdFiles`.

File-scoped instructions for Python, notebooks, Markdown, editor, results, prompts, resources, Moodle XML, customization authoring, and the project/customization documentation-sync rules live in [instructions/](instructions/) and are applied automatically based on `applyTo` glob patterns.

Durable customization rationale lives in [docs/](docs/). The active maintenance plan remains [implementation_plan.md](implementation_plan.md) at the `.github/` root.

- Keep changes minimal and focused on the active task.