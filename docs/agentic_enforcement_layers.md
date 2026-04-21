# Agentic Enforcement Layers: Notebook Hygiene as a Case Study

## Overview

When a rule must be enforced in an AI-assisted development environment, there are multiple layers at which enforcement can happen. Each layer addresses a different audience, runs at a different moment in the lifecycle, and uses a different VS Code / git primitive.

This document uses **notebook output hygiene** as a concrete case study. The rule being enforced is:

> Jupyter notebook cell outputs must never be committed to version control, because they may contain student exam data.

The same four-layer pattern generalises to any rule you want to apply consistently across human developers and AI agents.

## The Four Layers

### Layer 1 — Always-on Instruction

| Property | Value |
| --- | --- |
| **Primitive** | `.instructions.md` with `applyTo: "**/*.ipynb"` |
| **Audience** | AI agent |
| **Timing** | At edit time — injected into the context window whenever a `.ipynb` file is in scope |
| **File** | `.github/instructions/notebooks.instructions.md` |

This layer tells the AI agent about the rule *before* it acts. The instruction appears automatically in the context window when any notebook file is open, so the agent knows to avoid generating code that produces outputs without warning. It also explains *why* the rule exists (privacy risk), which helps the agent make better decisions in edge cases.

**Strengths:** Zero latency — the agent is aware of the rule before it acts. Explains rationale, enabling better edge-case reasoning. No tooling required; plain Markdown text in the context window. Can cross-reference other layers ("CI will block the PR"), keeping the agent informed of downstream consequences.

**Limitations:** Non-deterministic — the agent may still violate the rule if it forgets or misinterprets the instruction. Costs context-window tokens on every notebook interaction, even when irrelevant. Guides only; does not enforce.

---

### Layer 2 — Agent-time Hook (`PostToolUse`)

| Property | Value |
| --- | --- |
| **Primitive** | Hook — `.github/hooks/*.json` + shell/Python script |
| **Audience** | AI agent |
| **Timing** | After any file write tool completes, before the agent continues |
| **Files** | `.github/hooks/strip-notebook-outputs.json`, `.github/hooks/strip_notebook_outputs.py` |

This layer runs a script immediately after the agent writes any file. If the written file is a `.ipynb`, `nbstripout` is invoked automatically. The agent never has a chance to commit outputs because they are stripped as soon as the file is written.

**Strengths:** Deterministic — runs unconditionally regardless of what the AI was thinking. Silent in the happy path; only surfaces a warning if stripping fails. Removes the need for the agent to remember. Complements Layer 1: even if the instruction is forgotten, the hook catches it.

**Limitations:** Requires `nbstripout` in the agent's runtime environment. The stdin format varies by agent runtime (VS Code Copilot, Claude Code, etc.) so the script must handle multiple field name conventions defensively. Adds minor latency per file write (~100ms). Only fires on agent file writes; does not cover manual edits. In VS Code Copilot, hooks require agent mode — they do not fire in inline edit or non-agentic chat.

---

### Layer 3 — Local Git Filter

| Property | Value |
| --- | --- |
| **Primitive** | Git clean filter via `nbstripout --install` |
| **Audience** | Human developer |
| **Timing** | At `git add` / commit time |
| **Files** | `.gitattributes` (filter declaration) + per-developer `nbstripout --install` |

The git filter runs `nbstripout` as a clean filter on every `git add` for `.ipynb` files. Outputs are stripped transparently before the file reaches the staging area.

**Strengths:** Transparent — the developer never needs to remember to strip manually. Works for any edit, including those made entirely outside the AI agent. Catches the issue client-side before a push is ever made.

**Limitations:** Requires each developer to run `nbstripout --install` once after cloning — it is *not* automatically active. Can be bypassed with `git add --no-filters` or a misconfigured local config. Silent stripping may surprise developers who are unaware the filter is active.

---

### Layer 4 — CI Check

| Property | Value |
| --- | --- |
| **Primitive** | GitHub Actions workflow |
| **Audience** | Human developer (at push/PR time) |
| **Timing** | On `push` or `pull_request` for `**/*.ipynb` files |
| **File** | `.github/workflows/check-notebooks.yml` |

The CI workflow runs `nbstripout --verify` on all notebooks and fails the build if any contain outputs. This is the last line of defence before code reaches the shared repository.

**Strengths:** Authoritative — blocks the push regardless of how the notebook was edited or by whom. Visible to the whole team via PR status checks. Zero per-developer setup required. Cannot be bypassed by a local misconfiguration.

**Limitations:** Reactive — the developer finds out only after pushing. Does not fix the problem automatically; requires a manual re-push. Adds CI time (small but non-zero). Only triggers when `.ipynb` files are included in the push.

---

## Why All Four Layers?

Each layer addresses a failure mode the others cannot catch:

| Failure mode | Caught by |
| --- | --- |
| AI agent generates outputs carelessly | Layer 1 (proactive guidance) |
| AI agent forgets or ignores instructions | Layer 2 (hook auto-strips) |
| Developer edits notebook outside the agent | Layer 3 (git filter) |
| Developer bypasses or forgets git filter | Layer 4 (CI blocks push) |
| All local controls bypassed | Layer 4 (CI blocks push) |

Removing any layer creates a gap. Layer 4 is the only mandatory one if you accept reactive feedback. Layer 3 is the most practical single addition for human workflow. Layer 2 is the most valuable addition for AI-assisted workflows.

## The Overlap Is Intentional

The instructions file (Layer 1) explicitly mentions CI (Layer 4): *"CI will block the PR if outputs are present."* This is not duplication — it is the AI agent being informed about a downstream enforcement mechanism so it can set user expectations correctly and avoid wasting the user's time on a doomed push. Cross-layer references in instruction files are a deliberate design choice.

Similarly, `results/AGENTS.md` mentions both the git filter and the CI workflow. That file is the canonical privacy policy; it describes the full system so any agent or developer reading it understands the complete picture.

## Portability as a Skill

The four-layer setup can be packaged as a reusable VS Code skill (`.github/skills/notebook-hygiene/SKILL.md`). A skill bundles workflow instructions and co-located asset templates so it can be installed in a new project by invoking the skill once, rather than copying files manually.

See `.github/skills/notebook-hygiene/SKILL.md` for the portable installer.

## The General Pattern

The notebook hygiene case illustrates a general pattern applicable to any rule in AI-assisted development:

```text
Rule
├── Always-on instruction (.instructions.md, applyTo glob)   → AI awareness (non-deterministic)
├── PostToolUse hook (.github/hooks/)                        → AI-time enforcement (deterministic)
├── Local tooling (git hooks, formatters, pre-commit)        → Human-time client-side
└── CI check (GitHub Actions)                                → Human-time server-side
```

Different projects need different combinations. A solo project might only need Layers 1 + 4. A team project benefits from all four. A project that relies heavily on AI agents for code generation benefits most from Layer 2.

The right question when adding a new rule is not "which layer should I use?" but "which layers does this rule need to cover all realistic failure modes?"
