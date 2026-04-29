---
name: todo-analysis
description: >
  Analyze repository TODOs, separate clarification questions from action items, and maintain a lightweight docs/implementation_plan.md for the repo's SDD/living-documentation workflow. Use when triaging pending work before coding or when refreshing the plan after new discoveries.
argument-hint: "[scope: optional path or topic]"
user-invocable: true
disable-model-invocation: false # TODO: In which cases the agent would invoke the model?
---

# TODO Analysis

This skill is the canonical planning workflow for this repository.

Canonical rationale for the workflow lives in [docs/customization_architecture.md](../../../docs/customization_architecture.md). Keep this skill operational: it should tell the agent what to do, not restate the full design rationale.

<!-- TODO: but refering to the doc is not loading that doc in context? wouldn't be more operational to just not quoting it? -->

## Working Model

- `TODO:` is the canonical capture marker for this repository. Prefer it for new notes because low-friction capture matters more than inline taxonomy.
- Continue reading `ARCH:`, `DESIGN:`, `FIXME:`, and `HACK:` as equivalent planning inputs. They stay supported for compatibility, but `TODO:` is the only preferred marker for new notes.
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

After enriching individual markers, do a cross-cutting scan:

- group markers by affected module or workflow boundary
- identify recurring themes (e.g., all language-convention questions, all schema-ownership questions)
- note whether any group of questions implies a deeper architectural ambiguity not captured by any single marker

### 4. Classify by intent

Use this decision rule:

- `question`: asks why, whether, where a workflow belongs, or what primitive should own something
- `decision`: architectural or workflow choice that needs approval before coding
- `action`: clear implementation step with a plausible next edit
- `bug`: current behavior is wrong and the fix direction is understood
- `debt`: cleanup, migration, or structural improvement with no immediate bug

If one marker contains both a question and an action, split it in the plan: clarification first, action second.

When the item is still mostly debate, keep it in the Clarification Queue instead of inventing a premature action item.

### 5. Update `docs/implementation_plan.md`

Keep the plan lightweight enough to update after every meaningful step. Do not turn it into a second codebase inventory.

**Archive completed items.** Completed `P` items must not stay in the Planned Work table or Item Details section. After each run:

- Remove completed rows from the Planned Work table.
- Remove their Item Details blocks.
- Add a one-line summary to the `Recently Completed` section (see template below).

The `Recently Resolved` section is for architectural decisions and agreement records. The `Recently Completed` section is for implemented P items. Keep them separate.

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

## Recently Completed

- P1 — 2026-04-29. Defined the customization architecture for the SDD loop.

## Recently Resolved

- Q1 — Resolved on 2026-04-29. The reusable workflow lives in a skill; the persona and handoff live in a custom agent.

```

### 6. Resolve open questions with the user

After the plan is written, do not stop. Create aWork through each new or still-open Clarification Queue item interactively:

1. For each open Q item, present:
   - the source file and line
   - a concrete analysis of the trade-offs and options (not just a restatement of the TODO text)
   - a recommended answer if one is defensible
2. Ask the user to confirm, reject, or modify the recommendation.
3. Record the decision inline (update the Q row to `resolved`, add a `Recently Resolved` entry, and update any affected P items or Item Details).
4. Repeat for every open question before moving to Step 7.

Do not batch all questions into one message. Present one question at a time so the user can respond with context.

### 7. Surface the handoff

After all open questions are either resolved or explicitly deferred, present:

- a concise summary of what changed in the plan (new Q items, resolved Q items, new P items, approved P items)
- the approved next implementation item (the first unblocked `planned` item in the Planned Work table)
- the handoff to `sdd-implementer` for the user to trigger when ready

## Notes For The Implementing Agent

- Read `docs/implementation_plan.md` before editing anything.
- Do not start a blocked item while its clarification entry is still open.
- Update the plan status after each completed item.
- When a change affects workflow, architecture, or repo conventions, update the relevant docs and instructions in the same change.


---

## Guardrails for This Skill

- **Read-only for source**: this skill reads source files but does not modify them.
- **Single plan output**: the only file written is `docs/implementation_plan.md`.
- **No implementation**: the skill produces a plan and resolves questions with the user. Actual source changes are a separate step done by `sdd-implementer`.
- **Questions before handoff**: do not surface the handoff to `sdd-implementer` until every new Q item is either resolved or explicitly deferred by the user.
- **Completeness over speed**: if context is missing, read more files before writing the plan. A thorough plan written slowly is far more valuable than a shallow plan written fast.
