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

## File format specs (VS Code docs: https://code.visualstudio.com/docs/copilot/customization/overview, last reviewed 2026-04-22)

<!-- TODO: would some skill or prompt (not sure which would be better) that from time to time will read the updated documentation in the web and make a complete analysis of customization files in this repo to suggest improvements? something similar to current built-in /init but using the updated documentation -->

### `.instructions.md` (stored in `.github/instructions/`)

Frontmatter fields (all optional):

| Field | Purpose |
|---|---|
| `name` | Display name shown in the UI. Defaults to file name. |
| `description` | Short description shown on hover in the Chat view. Used for semantic matching when `applyTo` is absent. |
| `applyTo` | Glob pattern (relative to workspace root) for auto-applying the file. **If omitted, the file is never applied automatically** — it can only be manually attached. |

- Reference tools in the body with `#tool:<tool-name>` (for example, `#tool:web/fetch`).
- Markdown links to other files are auto-included when `chat.includeReferencedInstructions` is enabled (the default in this repo).

### `.agent.md` (stored in `.github/agents/`)

Replaces the deprecated `.chatmode.md` format. Rename any existing `.chatmode.md` files and move them to `.github/agents/`.

Frontmatter fields:

| Field | Notes |
|---|---|
| `name` | Agent name shown in the agents dropdown. Defaults to file name. |
| `description` | Shown as placeholder text in the chat input field. |
| `argument-hint` | Hint text shown in the chat input to guide users. |
| `tools` | Array of tool or tool-set names available to this agent. |
| `agents` | Array of agent names available as subagents. Use `*` for all, `[]` to disable. |
| `model` | String or priority array of model names. Defaults to current model picker selection. |
| `user-invocable` | Boolean (default `true`). Set `false` to hide from the agents dropdown while still allowing subagent invocation. |
| `disable-model-invocation` | Boolean (default `false`). Set `true` to prevent other agents from invoking this as a subagent. |
| `handoffs` | Array of `{label, agent, prompt, send?, model?}` objects. `send: true` auto-submits the prompt on handoff. |
| `hooks` | Agent-scoped hooks (same format as `.github/hooks/*.json`). Requires `chat.useCustomAgentHooks` enabled. |

**Deprecated:** `infer` — replaced by `user-invocable` + `disable-model-invocation`. Do not use `infer` in new files.

### `SKILL.md` (stored in `.github/skills/<skill-name>/`)

Frontmatter fields:

| Field | Required | Notes |
|---|---|---|
| `name` | **Yes** | **Must exactly match the parent directory name.** Lowercase letters, numbers, and hyphens only — no dots, slashes, or colons. Max 64 characters. Violations cause the skill to **silently fail to load**. |
| `description` | **Yes** | What the skill does and when to use it. Controls Copilot's auto-loading relevance matching. Max 1024 characters. |
| `argument-hint` | No | Hint text shown when the skill is invoked as a slash command. |
| `user-invocable` | No | Boolean (default `true`). Set `false` to hide from the `/` slash command menu while still allowing auto-loading. |
| `disable-model-invocation` | No | Boolean (default `false`). Set `true` to require manual invocation only. |

- Additional resource files (scripts, examples) in the skill directory are **only loaded if Markdown-linked from the `SKILL.md` body**.

### Hooks (`.github/hooks/*.json`)

Format: `{"hooks": {"EventName": [{"type": "command", "command": "..."}]}}`.

Supported lifecycle events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`.

Hook command properties: `type` (must be `"command"`), `command`, `windows`, `linux`, `osx`, `cwd`, `env`, `timeout` (default 30 s).

See [docs/agentic_enforcement_layers.md](../../docs/agentic_enforcement_layers.md) for this project's hook design decisions.