---
name: todo-analysis
description: >
  Analyze repository TODOs, separate clarification questions from action items,
  and maintain a lightweight docs/implementation_plan.md for the repo's
  SDD/living-documentation workflow. Use when triaging pending work before
  coding or when refreshing the plan after new discoveries.
argument-hint: "[scope: optional path or topic]"
user-invocable: true
disable-model-invocation: false
---

# TODO Analysis

This skill is the canonical planning workflow for this repository.

It is a skill, not an instruction file or prompt, because it is a reusable, task-specific workflow that can be invoked directly, loaded by an agent, and maintained separately from always-on policy.
<!-- TODO: Does the skill itself need to know that? wouldn't be better to documented for human consumption in customization_architecture.md and remove this paragraph here for token efficiency? -->

## Working Model

- `TODO:` is the canonical capture marker for this repository. Prefer it for new notes because low-friction capture matters more than inline taxonomy.
- Continue reading `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` when they already exist, but treat them as optional legacy hints rather than required categories.
<!-- TODO: what's going to imply treating them as legacy? once they exist, seems appropriate to treat them also as TODOs at least. -->
- Classify items by intent, not only by prefix. The useful buckets are: `question`, `decision`, `action`, `bug`, and `debt`.
- A question-style TODO does not become an implementation item until it has been clarified with the user. Put it in the Clarification Queue first.
- The implementation plan is the curated source of truth for active work. Raw TODOs remain the capture surface. Stable rationale belongs in docs and instructions after decisions are made.

## Workflow

### 1. Read the current plan first

If `docs/implementation_plan.md` exists, read it before scanning the codebase. Preserve useful history instead of overwriting it blindly.

### 2. Discover markers

Search the codebase for `TODO:` first. Then run a compatibility sweep for `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` so older notes are not lost.

Record for each marker:

- file path
- line number
- full marker text
- enclosing function, class, section, or module
- whether the text is phrased as a question

### 3. Enrich locally

<!-- TODO: Plenty of TODOs are going to be architecture or design questions / change proposals, so a broader analysis will be important. Recurrent architecture questioning is important in SDD for keeping the project modular and scalable and therefore avoid context problems in the future. -->

For every marker, read the surrounding scope and the nearest relevant docs. Do not classify from the comment text alone.

Minimum context bar:

- read the full enclosing scope
- identify the direct callers or neighboring files when the note affects behavior
- check whether the note overlaps with another TODO or doc section

### 4. Classify by intent

Use this decision rule:

- `question`: asks why, whether, where a workflow belongs, or what primitive should own something
- `decision`: architectural or workflow choice that needs approval before coding
- `action`: clear implementation step with a plausible next edit
- `bug`: current behavior is wrong and the fix direction is understood
- `debt`: cleanup, migration, or structural improvement with no immediate bug

If one marker contains both a question and an action, split it in the plan: clarification first, action second.

<!-- TODO: deep analysis or architecture and software design good practices is paramount, so the first steps os dealing with questions and debating critically with the user is key -->

### 5. Update `docs/implementation_plan.md`

Keep the plan lightweight enough to update after every meaningful step. Do not turn it into a second codebase inventory.

Use this template:

```markdown
# Implementation Plan

> Updated: {ISO date}
> Branch: {git branch}
> Status: active | blocked-for-clarification | archived

## Working Agreements

- TODO is the canonical capture marker.
- Question-style TODOs stay in the Clarification Queue until resolved.
- Implement one approved item at a time.
- Sync docs and instructions after implementation, not during speculation.

## Clarification Queue

| ID | Status | Source | Question | Next step |
|---|---|---|---|---|
| Q1 | open | path/to/file.md:12 | Should this workflow live in a skill or an agent? | Discuss and record the decision |

## Planned Work

| ID | Status | Type | Summary | Source | Depends on |
|---|---|---|---|---|---|
| P1 | planned | decision | Define the customization architecture for the SDD loop | AGENTS.md:3 | Q1 |

## Next Sequence

1. Resolve the open clarification items that block planning.
2. Implement the smallest approved decision or action item.
3. Update this file, then sync docs and instructions touched by that change.

## Item Details

### P1 — Define the customization architecture for the SDD loop

**Type**: decision
**Source TODOs**:
- path/to/file.md:12 — TODO text

**Current understanding**:
- Short, concrete summary of what the codebase currently does.

**Decision or change to make**:
- Concrete outcome, not vague aspiration.

**Docs to sync after implementation**:
- AGENTS.md
- README.md

## Recently Resolved

- Q1 — Resolved on 2026-04-29. The reusable workflow lives in a skill; the persona and handoff live in a custom agent.

```

### 6. Stop at the right boundary

This skill plans. It does not implement source changes. Its output is the refreshed `docs/implementation_plan.md` and a concise summary of:

- open clarification items
- approved next implementation item
- docs and instructions likely to need sync after implementation

## Notes For The Implementing Agent

- Read `docs/implementation_plan.md` before editing anything.
- Do not start a blocked item while its clarification entry is still open.
- Update the plan status after each completed item.
- When a change affects workflow, architecture, or repo conventions, update the relevant docs and instructions in the same change.
  confirmation that this plan has been reviewed.


---

## Guardrails for This Skill

- **Read-only**: this skill reads source files but does not modify them.
- **Single output**: the only file written is `docs/implementation_plan.md`.
- **No implementation**: the skill produces a plan. Actual implementation is
  a separate step, done by the user or a dedicated implementation agent.
- **Completeness over speed**: if context is missing, read more files before
  writing the plan. A thorough plan written slowly is far more valuable than
  a shallow plan written fast.
