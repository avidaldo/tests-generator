---
name: Prompt Authoring
description: "Use when authoring or updating prompt files or instruction files."
applyTo: '**/*.prompt.md,**/*.instructions.md'
---

- Canonical prompt authoring instructions live in [prompts/AGENTS.md](../../prompts/AGENTS.md). Follow that file as the source of truth for the `prompts/` module.
- Preserve the active two-stage workflow: `summarize-sources.prompt.md` feeds `generate-questions.prompt.md`; deprecated prompts stay reference-only unless the task explicitly revives them.
- For quiz-generation prompts, keep the one-subcategory-at-a-time workflow and preserve the requirement to consult [docs/adversarial_logic_filters.md](../../docs/adversarial_logic_filters.md).
- Keep prompt files scoped to one reusable workflow. If the task needs persistent persona, tool restrictions, or multi-stage handoffs, prefer a custom agent or skill instead of broadening the prompt.

## `.prompt.md` frontmatter spec (VS Code docs: https://code.visualstudio.com/docs/copilot/customization/prompt-files, last reviewed 2026-04-22)

| Field | Required | Notes |
|---|---|---|
| `name` | No | Slash-command name (after `/`). Defaults to file name. |
| `description` | No | Short description of what the prompt does. |
| `argument-hint` | No | Hint text shown in the chat input field when the prompt is active. |
| `agent` | No | Agent to use: `ask`, `agent`, `plan`, or the name of a custom agent. Defaults to the current agent; defaults to `agent` if `tools` is specified. |
| `model` | No | Model to use when running the prompt. Defaults to current model picker selection. |
| `tools` | No | Array of tool or tool-set names available when running this prompt. Takes precedence over the referenced agent's tool list. |

- Reference other workspace files via relative Markdown links.
- Reference tools in the body with `#tool:<tool-name>` syntax.
- Use `${input:varName}` or `${input:varName:placeholder}` for user-supplied input variables.
- Tool list priority (highest to lowest): prompt-file `tools` → referenced agent `tools` → agent defaults.

### Prompt Design Research (mandatory before creating or significantly modifying prompts)

Before designing any prompt, search for relevant, up-to-date prompting guidance. **Nothing prior to beginning of 2026.** Consult current sources such as:

- https://ai.google.dev/gemini-api/docs/prompting-strategies
- https://platform.openai.com/docs/guides/prompt-engineering
- https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
- https://platform.claude.com/docs/en/resources/prompt-library/library