# Customization Architecture

## Purpose

This repository uses chat customizations as part of a simple SDD and living-documentation loop. The goal is not to impose a heavy methodology. The goal is to keep idea capture cheap, planning explicit, implementation focused, and documentation updated as the codebase changes.

This design was aligned against the current VS Code customization docs reviewed on 2026-04-22.

## Sources Of Truth

| Surface | Role | Update cadence |
| --- | --- | --- |
| `TODO:` comments | Raw capture for ideas, doubts, bugs, and debt | Captured near the affected file with minimal ceremony; triaged later |
| `docs/implementation_plan.md` | Curated active plan and clarification queue | Before and after implementation |
| `docs/*.md` | Stable human-facing rationale and design decisions | When decisions settle |
| `AGENTS.md` and `*.instructions.md` | Agent behavior, routing, and always-on policy | When the agent should behave differently |

None of these surfaces replaces the others.

- TODOs are intentionally provisional and lightweight.
- The implementation plan is curated and current.
- Documentation explains why the system is shaped the way it is.
- Instructions tell agents how to behave when they operate inside that system.

## Terminology

- A `primitive` is a VS Code customization type such as an instruction file, prompt, skill, custom agent, hook, or MCP server.
- A `customization` is one concrete repo artifact that uses a primitive, for example `.github/skills/todo-analysis/SKILL.md` or `.github/hooks/living-docs-drift-check.json`.
- A `surface` is a place where behavior or truth is stored and discovered, such as `docs/implementation_plan.md`, `AGENTS.md`, or the `.github/hooks/` folder.

## Primitive Allocation

| Primitive | Role in this repo | Why it lives there |
| --- | --- | --- |
| Always-on instructions | Repo policy, routing, and behavior constraints | These rules should be present automatically in agent context |
| File instructions | File-type and module-specific rules | They are conditional and should not burn context everywhere |
| Skill | Reusable planning workflow (`todo-analysis`) | The workflow is task-specific, portable, and should be callable on demand |
| Custom agents | Planning persona and implementation persona | Persona, handoff, and agent-scoped hook behavior belong with agents |
| Hooks | Deterministic reminders and guard rails | Hooks should enforce or remind, not perform judgment-heavy authoring |
| Prompts | Quiz-generation pipeline tasks | These are single reusable workflows for domain tasks, not always-on behavior |

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
2. Run the `todo-planner` custom agent to read the current plan, scan TODOs, and refresh `docs/implementation_plan.md`.
3. Resolve Clarification Queue items with the user before coding.
4. Choose one approved plan item.
5. Implement it with `sdd-implementer` or the standard coding agent.
6. Update `docs/implementation_plan.md` and sync the relevant docs and instructions in the same change.

## Docs Versus Instructions

Use documentation when the primary consumer is a human who needs rationale, tradeoffs, or a durable design record.

Use instructions when the primary consumer is the agent and the information should influence behavior automatically during work.

Practical rule:

- If the content explains why a design exists, it belongs in `docs/`.
- If the content says how the agent should behave, route, or prioritize while working, it belongs in `AGENTS.md` or an instruction file.
- If the content is a reusable multi-step workflow, it belongs in a skill.
- If the content depends on a persona, handoff, or hook scope, it belongs in a custom agent.

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

- `todo-analysis` is a skill, not a prompt, because it is a reusable multi-step workflow that can be invoked directly or loaded by another agent.
- `todo-planner` is a custom agent, not just part of the skill, because it needs a planning persona, a handoff to the implementer, and planner-only hooks.
- `sdd-implementer` is a custom agent because implementation behavior is persistent and should start from the plan every time, not from a one-off prompt.
- The planner handoff keeps an explicit prompt even though `sdd-implementer` already has instructions. The handoff prompt carries the specific next-step context into the new chat state; it complements the target agent instructions instead of replacing them.
- The living-docs reminder is a workspace hook JSON because it should apply repo-wide after relevant source edits.

## Current Mapping

| Surface | Current file(s) | Responsibility |
| --- | --- | --- |
| Planning workflow | `.github/skills/todo-analysis/SKILL.md` | Triages TODOs into a lightweight implementation plan |
| Planning persona | `.github/agents/todo-planner.agent.md` | Planning-only agent with plan refresh and implementation handoff |
| Implementation persona | `.github/agents/sdd-implementer.agent.md` | Implements one approved item at a time and syncs docs |
| Planner guard rails | `.github/hooks/src/todo_planner_context.py`, `.github/hooks/src/todo_planner_write_guard.py` | Agent-scoped context injection and write restriction for planner sessions |
| Prompt/customization drift reminder | `.github/hooks/prompt-doc-drift-check.json`, `.github/hooks/src/prompt_doc_drift_check.py` | Reminds when prompt/customization changes are not reflected in the root docs |
| Living-docs reminder | `.github/hooks/living-docs-drift-check.json`, `.github/hooks/src/living_docs_drift_check.py` | Reminds when source edits have no matching plan or documentation updates |

## Design Decisions Recorded On 2026-04-29

- `TODO:` is the canonical inline marker.
- Question-style TODOs are first-class planning inputs, not implementation items.
- The reusable planning workflow lives in the `todo-analysis` skill.
- Persona, handoff, and planner-only guard rails live in custom agents.
- Hooks provide deterministic reminders and constraints only; they do not author docs.
