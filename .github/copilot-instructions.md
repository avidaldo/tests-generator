# Moodle Tests — VS Code Adapter

This file is a thin GitHub Copilot and VS Code compatibility adapter.

[AGENTS.md](../AGENTS.md) is the primary instruction source for project-wide policy. [AGENTS.md](AGENTS.md) is the primary instruction source for the customization layer. Subfolder `AGENTS.md` files (`editor/`, `results/`, `prompts/`) are also loaded automatically via `chat.useNestedAgentsMdFiles`.

File-scoped instructions for Python, notebooks, Markdown, editor, results, prompts, resources, Moodle XML, customization authoring, and the project/customization documentation-sync rules live in [instructions/](instructions/) and are applied automatically based on `applyTo` glob patterns.

Durable customization rationale lives in [docs/](docs/). Plan larger changes against [../todos.md](../todos.md); there is no separate maintenance plan file.

- Keep changes minimal and focused on the active task.