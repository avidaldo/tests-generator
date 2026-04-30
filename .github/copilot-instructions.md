# Moodle Tests — VS Code Adapter

This file is a GitHub Copilot and VS Code compatibility adapter. <!-- TODO: Probably not needed since AGENTS.md is accepted by VSCode, and used because is more agnostic -->

[AGENTS.md](../AGENTS.md) is the primary instruction source for project-wide policy. [AGENTS.md](AGENTS.md) is the primary instruction source for the customization layer. Subfolder `AGENTS.md` files (`.github/prompts/`, `editor/`, `results/`, `prompts/`) are also loaded automatically via `chat.useNestedAgentsMdFiles`.

File-scoped instructions for Python, notebooks, Markdown, editor, results, prompts, resources, Moodle XML, customization authoring, and documentation-sync rules live in [instructions/](instructions/) and are applied automatically based on `applyTo` glob patterns.

- Keep changes minimal and focused on the active task.