# Moodle Tests — VS Code Adapter

This file is a GitHub Copilot / VS Code compatibility adapter.

[AGENTS.md](../AGENTS.md) is loaded automatically as always-on instructions by VS Code and is the primary instruction source for project-wide policy, architecture, privacy, and workflow rules. Subfolder `AGENTS.md` files (`editor/`, `results/`, `prompts/`) are also loaded automatically via `chat.useNestedAgentsMdFiles`.

File-scoped instructions for Python, notebooks, Markdown, editor, results, and prompts live in [instructions/](instructions/) and are applied automatically based on `applyTo` glob patterns.

- Keep changes minimal and focused on the active task.