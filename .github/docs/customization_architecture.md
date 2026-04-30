# Customization Architecture

## Purpose

This repository uses chat customizations as part of a simple SDD and living-documentation loop. The goal is not to impose a heavy methodology. The goal is to keep idea capture cheap, planning explicit, implementation focused, and documentation updated as the codebase changes.

This design was aligned against the current VS Code customization docs reviewed on 2026-04-22.

## Sources Of Truth

| Surface | Role | Update cadence |
| --- | --- | --- |
| `TODO:` comments | Raw capture for ideas, doubts, bugs, and debt | Captured near the affected file with minimal ceremony; triaged later |
| `.github/implementation_plan.md` | Curated active plan and clarification queue | Before and after implementation |
| `.github/docs/*.md` | Stable customization rationale and design decisions | When decisions settle |
| `AGENTS.md`, `.github/AGENTS.md`, and `*.instructions.md` | Agent behavior, routing, and always-on policy | When the agent should behave differently |

None of these surfaces replaces the others.

- TODOs are intentionally provisional and lightweight.
- The implementation plan is curated and current.
- Documentation explains why the system is shaped the way it is.
- Instructions tell agents how to behave when they operate inside that system.

## Terminology

- A `primitive` is a VS Code customization type such as an instruction file, prompt, skill, custom agent, hook, or MCP server.
- A `customization` is one concrete repo artifact that uses a primitive, for example `.github/agents/todo-planner.agent.md` or `.github/hooks/living-docs-drift-check.json`.
- A `surface` is a place where behavior or truth is stored and discovered, such as `.github/implementation_plan.md`, `.github/AGENTS.md`, or the `.github/hooks/` folder.

## Primitive Allocation

| Primitive | Role in this repo | Why it lives there |
| --- | --- | --- |
| Always-on instructions | Repo policy, routing, and behavior constraints | These rules should be present automatically in agent context |
| File instructions | File-type and module-specific rules | They are conditional and should not burn context everywhere |
| Skill | Reusable supporting workflows outside the core SDD loop | Use a skill only when the workflow is genuinely reused or needs bundled resources |
| Custom agents | Planning and implementation execution surfaces | Persona, scoped hooks, and persistent workflow contracts belong with agents |
| Hooks | Deterministic reminders and guard rails | Hooks should enforce or remind, not perform judgment-heavy authoring |
| Prompts | Preferred workflow entry points | Prompts stay lightweight and improve slash-menu discovery for both the SDD loop and the quiz-generation pipeline |

## Marker Policy

`TODO:` is the canonical inline marker for this repository.

That is a reasonable choice. It keeps capture friction low, works with a single editor shortcut, and avoids false precision while you are still thinking. The cost is that priority and intent are no longer encoded inline. The mitigation is deliberate planning: the planner classifies markers later by intent and impact.

The repo still reads `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` when they already exist. They are treated as equivalent planning inputs for compatibility, but `TODO:` is the preferred marker for new notes.

## Question-Style TODOs

Question-style TODOs are encouraged here because they capture uncertainty rather than pretending the design is already known.

They must not be treated as implementation tasks immediately. The planning step moves them into a Clarification Queue first. Only after the question is resolved should the result become a planned decision or action item.

This keeps the workflow honest:

- capture can stay exploratory
- planning stays explicit
- implementation starts only after the relevant uncertainty is resolved

## Recommended Loop

1. Capture new doubts or ideas as `TODO:` comments close to the code or document they affect.
2. Run `.github/prompts/refresh-plan.prompt.md` to enter the guarded planning workflow and refresh `.github/implementation_plan.md`.
3. Resolve Clarification Queue items with the user before coding.
4. Choose one approved plan item.
5. Run `.github/prompts/implement-plan-item.prompt.md` to enter the implementation workflow for one approved item.
6. Update `.github/implementation_plan.md` and sync the relevant docs and instructions in the same change.

## Entry Point Tiers

VS Code now has a deliberate preferred-entry model for this repo:

1. **Prompts are the preferred entry points.** The recommended slash commands are `.github/prompts/refresh-plan.prompt.md` and `.github/prompts/implement-plan-item.prompt.md` for repo maintenance, plus the quiz-generation prompts in `prompts/`.
2. **Agents are the execution surfaces.** `todo-planner` and `sdd-implementer` own persona, hook scope, and the durable workflow contracts that the maintenance prompts target directly.
3. **Skills are auxiliary reusable modules.** Skills still exist in the repo for other workflows, but the SDD loop no longer depends on a separate planning skill layer.

This keeps the preferred UX prompt-first while using direct configuration, not prompt-body indirection, to select the execution surface.

## Docs Versus Instructions

Use documentation when the primary consumer is a human who needs rationale, tradeoffs, or a durable design record.

Use instructions when the primary consumer is the agent and the information should influence behavior automatically during work.

Practical rule:

- If the content explains why a design exists, it belongs in `.github/docs/` for customization rationale.
- If the content says how the agent should behave, route, or prioritize while working, it belongs in `AGENTS.md` or an instruction file.
- If the content is a reusable multi-step workflow with a concrete second consumer or bundled resources, it belongs in a skill.
- If the content depends on a persona or hook scope, it belongs in a custom agent.

## Hook Policy

Hooks are appropriate here only for deterministic work:

- block or constrain planner writes
- auto-strip notebook outputs
- remind the agent that docs or the plan may be stale after edits

Hooks are not the right place to author living documentation automatically. Updating plans and docs requires judgment about what changed, what matters, and which rationale is now canonical. That belongs in the agent workflow, not in shell automation.

## Hook Mechanics In This Repo

Workspace-wide hooks live in `.github/hooks/*.json`. They are appropriate when the behavior should apply across the repository regardless of which agent is active. The notebook-output hook and the living-docs reminder fit that pattern.

Planner guard rails do not live in a workspace hook JSON. They are declared in `.github/agents/todo-planner.agent.md` under the agent's `hooks` frontmatter so they only run while `todo-planner` is active. That is why `todo_planner_context.py` and `todo_planner_write_guard.py` have no matching `.json` file.

The hook scripts communicate with the agent runtime through JSON on stdin and stdout.

**Why Python hook scripts rather than markdown instructions in the agent file?**

The primary reason is **dynamic data injection**: hook scripts run at agent startup and can compute and inject data that is only known at runtime — the current git branch, the live count of open TODO markers, or the current plan status. A static markdown instruction cannot do this; it can only express fixed rules.

A secondary reason is **enforcement boundary**: the agent runtime executes the hook regardless of what the agent instruction says, giving a harder guarantee than a markdown instruction that the agent could implicitly ignore.

For purely static rules, a markdown instruction in the agent file is simpler and equally effective. Hook scripts are justified only when runtime data is needed or a hard enforcement boundary is required. Both conditions apply to the planner guard rails; neither applies to, for example, a simple style reminder.

## Why These Primitive Choices

- `.github/prompts/refresh-plan.prompt.md` and `.github/prompts/implement-plan-item.prompt.md` are prompts because they are thin, user-facing launchers. They optimize slash-menu discovery and bind directly to the execution agents.
- `todo-planner` is a custom agent because it owns the planning persona, the planning workflow, and planner-only hooks.
- `sdd-implementer` is a custom agent because implementation behavior is persistent, plan-driven, and intentionally limited to one approved item per run.
- The maintenance prompts bind directly to visible custom agents because that is the cleanest mechanically supported design in this VS Code setup.
- Visible agents are acceptable here as advanced or secondary entry points. The prompts remain the preferred UX, but not the only surface.
- The separate `todo-analysis` skill was removed because it did not have a real second consumer. Inlining it into `todo-planner` reduced indirection without losing workflow clarity.
- The maintenance prompts live in `.github/prompts/`, which is the default workspace prompt root. The root `prompts/` folder stays dedicated to the quiz-generation pipeline and is enabled separately in `.vscode/settings.json`.
- Durable customization rationale lives in `.github/docs/`, while the `.github/` root keeps operational entry surfaces such as `README.md`, `AGENTS.md`, and `implementation_plan.md`.
- The living-docs reminder is a workspace hook JSON because it should apply repo-wide after relevant source edits.

## Current Mapping

| Surface | Current file(s) | Responsibility |
| --- | --- | --- |
| Planning launcher | `.github/prompts/refresh-plan.prompt.md` | Preferred slash-command entry for the guarded planning workflow |
| Implementation launcher | `.github/prompts/implement-plan-item.prompt.md` | Preferred slash-command entry for plan-driven implementation |
| Planning persona and workflow | `.github/agents/todo-planner.agent.md` | Planning agent with plan refresh workflow and planner-only hooks |
| Implementation persona and workflow | `.github/agents/sdd-implementer.agent.md` | Implementation agent that executes one approved item at a time |
| Planner guard rails | `.github/hooks/src/todo_planner_context.py`, `.github/hooks/src/todo_planner_write_guard.py` | Agent-scoped context injection and write restriction for planner sessions |
| Prompt/customization drift reminder | `.github/hooks/prompt-doc-drift-check.json`, `.github/hooks/src/prompt_doc_drift_check.py` | Reminds when prompt/customization changes are not reflected in the root docs |
| Living-docs reminder | `.github/hooks/living-docs-drift-check.json`, `.github/hooks/src/living_docs_drift_check.py` | Reminds when source edits have no matching plan or documentation updates |

## Design Decisions Recorded On 2026-04-29

- `TODO:` is the canonical inline marker.
- Question-style TODOs are first-class planning inputs, not implementation items.
- Maintenance prompts are the preferred VS Code entry points for the SDD loop.
- The planning workflow now lives directly in `todo-planner` rather than in a separate skill.
- Persona and planner-only guard rails live in custom agents.
- Durable customization docs live under `.github/docs/` and maintenance prompts live under `.github/prompts/`, while root `docs/` and root `prompts/` stay project-facing.
- Hooks provide deterministic reminders and constraints only; they do not author docs.
