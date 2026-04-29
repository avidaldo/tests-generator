---
name: todo-analysis
description: >
  Analyzes all TODO, ARCH, DESIGN, and FIXME comments across the codebase to
  produce a structured implementation plan saved as docs/implementation_plan.md.
  Use this skill when asked to: review or prioritize technical debt, plan
  architectural changes, understand cross-file impact of pending work, or
  create an implementation roadmap before writing any code.
argument-hint: "[scope: all|arch|design|fixme|todo] [path: optional subfolder]"
user-invocable: true
disable-model-invocation: false
---

<!-- TODO: why is this an skill? Let's be rigurous in following VSCode current standards -->

# TODO Analysis Skill

This skill performs a deep, context-aware analysis of all pending work markers
in a codebase and produces a prioritized, actionable implementation plan. It
reads but never modifies source files. The only file it writes is
`docs/implementation_plan.md`.

---

## Phase 1 — Discovery

Search the codebase for all pending work markers. Use `Grep` or `Bash` with
patterns that cover common variants. Cast the net wide — look for markers both
in source code and in documentation files.

**Markers to find (case-insensitive):**

| Prefix   | Meaning                                         | Priority signal |
|----------|-------------------------------------------------|-----------------|
| `ARCH:`  | Architectural decision — cross-cutting change   | High            |
| `DESIGN:`| Interface/API/module boundary change            | High            |
| `TODO:`  | Tactical change, scope may vary                 | Medium          |
| `FIXME:` | Bug with a known cause                          | High (bugs)     |
| `HACK:`  | Workaround that needs a proper solution         | Medium          |
| `NOTE:`  | Non-actionable context note — read but skip     | Info only       |

<!-- TODO: Consider simplifying to only TODO / creating shortcuts for other markers  -->

**Search commands to run:**

```bash
# Primary sweep — all source files
grep -rn --include="*.py" --include="*.ts" --include="*.js" \
  --include="*.tsx" --include="*.jsx" --include="*.java" \
  --include="*.go" --include="*.rs" --include="*.rb" \
  --include="*.md" \
  -E "(TODO|ARCH|DESIGN|FIXME|HACK|NOTE)\s*:" . 2>/dev/null

# Secondary sweep — any file type, catch stragglers
grep -rn --exclude-dir=".git" --exclude-dir="node_modules" \
  --exclude-dir=".venv" --exclude-dir="__pycache__" \
  -E "(TODO|ARCH|DESIGN|FIXME|HACK)\s*:" . 2>/dev/null
```

Collect every result. Record: **file path**, **line number**, **full comment
text**, and **surrounding function/class name** (read ±15 lines of context).

---

## Phase 2 — Contextual Enrichment

For each discovered marker, do NOT just read the comment in isolation. Perform
active context gathering:

1. **Read the surrounding scope** — the function, class, or module containing
   the marker. Understand what the code currently does and why the marker was
   placed where it was.

2. **Trace usages** — if the marker mentions a class, function, or data
   structure, find all usages with `Grep` or `Glob`. Build a list of files
   that would be affected by this change.

3. **Read related documentation** — look for `README.md`, `ARCHITECTURE.md`,
   `docs/`, `ADR/`, or `CHANGELOG` files that provide architectural context.
   If the TODO references a library or external system, fetch its documentation
   URL if available.

4. **Find cross-references** — check if multiple markers reference the same
   concept, data model, or component. These are likely coupled changes.

5. **Check git history** — run `git log --oneline -10 -- <file>` for heavily
   annotated files to understand recent evolution.

---

## Phase 3 — Analysis and Dependency Mapping

After enrichment, analyze the full picture:

**Scope classification:**

| Label          | Definition                                                     |
|----------------|----------------------------------------------------------------|
| `local`        | Change is contained within a single function/method           |
| `cross-file`   | Change requires touching 2–5 files                            |
| `cross-module` | Change spans a module or package boundary                      |
| `architectural`| Change affects public APIs, data models, or system boundaries  |

**Dependency analysis:**
- Which TODOs must be resolved *before* others can start?
- Which TODOs conflict (e.g., two markers proposing incompatible designs)?
- Which TODOs are independent and can be parallelized?

**Complexity estimation (t-shirt sizing):**

| Size | Meaning                                                  |
|------|----------------------------------------------------------|
| S    | < 30 min — single-file, clear path, no dependencies     |
| M    | 30 min–2 h — a few files, straightforward refactor      |
| L    | 2–8 h — cross-module, needs design decisions             |
| XL   | > 1 day — architectural, requires review before starting |

---

## Phase 4 — Output: `docs/implementation_plan.md`

Write the plan to `docs/implementation_plan.md`. Create the `docs/` directory
if it does not exist. Use the exact template below. Do not truncate or
summarize — every discovered marker must appear in the inventory.

```markdown
# Implementation Plan

> **Generated**: {ISO date}
> **Branch**: {git branch}
> **Scope**: {N} markers analyzed across {M} files
> **Status**: DRAFT — review before implementing

---

## Executive Summary

{2–4 sentences describing the overall shape of the pending work: what major
themes emerge, which areas of the codebase carry the most debt, and a
high-level recommended order of attack.}

---

## Inventory

### 🔴 Architectural (`ARCH:`) — {count}

| # | File | Line | Summary | Scope | Size |
|---|------|------|---------|-------|------|
| A1 | path/to/file.py | 42 | Short description | architectural | XL |

### 🟡 Design-level (`DESIGN:`) — {count}

| # | File | Line | Summary | Scope | Size |
|---|------|------|---------|-------|------|

### 🟢 Tactical (`TODO:`) — {count}

| # | File | Line | Summary | Scope | Size |
|---|------|------|---------|-------|------|

### 🔴 Bugs (`FIXME:`) — {count}

| # | File | Line | Summary | Scope | Size |
|---|------|------|---------|-------|------|

### 🟠 Workarounds (`HACK:`) — {count}

| # | File | Line | Summary | Scope | Size |
|---|------|------|---------|-------|------|

---

## Dependency Graph

{ASCII or Mermaid diagram showing which items block others.}

```
A1 (auth redesign)
 └── D3 (update user model)
      └── T7 (fix login flow)
      └── T12 (update tests)
```

---

## Recommended Implementation Sequence

Ordered by: unblock others first → bugs → ARCH → DESIGN → TODO.
Items on the same indentation level can be parallelized.

```
Sprint 1 (unblock everything):
  1. F2 — Fix null pointer in user loader [S, isolated]
  2. A1 — Auth redesign [XL, blocks D3, T7, T12]

Sprint 2 (design work, after A1 review):
  3. D3 — Update user model [M, needs A1 merged]
  4. D5 — API response envelope [M, independent]

Sprint 3 (tactical work):
  5. T7 — Fix login flow [M, needs D3]
  6. T12 — Update tests [M, needs D3]
  7. H4 — Replace session hack [L, independent]
```

---

## Item Details

### A1 — {Short title}

**File**: `path/to/file.py` · Line 42
**Marker**: `# ARCH: Redesign the auth layer to support OAuth2 providers`
**Scope**: architectural · **Size**: XL
**Blast radius**: {list every file that must change}

**Current behavior**:
{What the code currently does — 2–4 sentences based on code reading.}

**Why this matters**:
{Context from docs/code comments explaining the motivation.}

**Proposed approach**:
{Concrete steps, not vague suggestions. If the marker itself gives direction,
expand on it. If not, propose the most conservative option.}

**Key questions to resolve before starting**:
- {Question 1}
- {Question 2}

**Tests to write or update**:
- {Test area 1}

**Blocks**: D3, T7, T12
**Blocked by**: none

---

{Repeat Item Details section for every marker in the inventory.}

---

## Open Questions

{List any ambiguities discovered during analysis that need human input before
the plan can be executed. Number them so they can be referenced in discussion.}

1. {Question about conflicting markers, unclear ownership, missing docs, etc.}

---

## Notes for the Implementing Agent

- Implement ONE item at a time. Do not batch changes across multiple items.
- Run the test suite after each item before moving to the next.
- Update this plan file to mark completed items (add ✅ to the inventory row).
- If implementation reveals new information that changes the plan, stop and
  update this document before continuing.
- Do not implement `architectural` (XL) items without an explicit human
  confirmation that this plan has been reviewed.
```

---

## Guardrails for This Skill

- **Read-only**: this skill reads source files but does not modify them.
- **Single output**: the only file written is `docs/implementation_plan.md`.
- **No implementation**: the skill produces a plan. Actual implementation is
  a separate step, done by the user or a dedicated implementation agent.
- **Completeness over speed**: if context is missing, read more files before
  writing the plan. A thorough plan written slowly is far more valuable than
  a shallow plan written fast.
