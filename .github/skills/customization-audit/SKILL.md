---
name: customization-audit
description: Fetch current VS Code customization docs and audit this repo's `.github` customization layer for deprecated patterns, missing recommended fields, and newly available primitives.
argument-hint: 'Optional: scope or specific customization surface to audit'
---

# Customization Audit Workflow

This skill audits the repository's VS Code customization layer against the current VS Code customization docs. Canonical local policy lives in [AGENTS.md](../../AGENTS.md), [customization-authoring.instructions.md](../../instructions/customization-authoring.instructions.md), and [prompts/AGENTS.md](../../prompts/AGENTS.md).

## When To Use

- Check whether this repo's `.github` customization files still match the current VS Code customization model.
- Look for deprecated frontmatter fields, missing recommended fields, or new supported primitives worth adopting.
- Review the customization layer after a VS Code major release or after unexplained customization regressions.

## Inputs To Confirm

1. Whether the audit should cover the full `.github` customization layer or only a narrower surface such as prompts, agents, instructions, hooks, or skills.
2. Whether the user wants only a report or also wants follow-up implementation proposals.
3. Any known VS Code release, regression, or documentation page that should receive extra attention.

## Procedure

1. Fetch the current docs with `#tool:web/fetch`.
   Start from `https://code.visualstudio.com/docs/copilot/customization/overview`, then fetch the primitive pages relevant to the requested scope (for example prompt files, custom instructions, chat modes / agents, and skills).
2. Read the live repo customization files.
   Inspect the relevant files under `.github/` with `#tool:glob`, `#tool:view`, and `#tool:rg`, including inventories, prompts, agents, instructions, hooks, skills, and any settings files that control discovery.
3. Compare docs against the repo.
   Look for deprecated fields still in use, recommended fields or guardrails the repo omits, supported primitives the repo could adopt, and local docs that no longer match the actual VS Code behavior described by the docs.
4. Report findings with evidence.
   Group the audit into: deprecated patterns in use, missing recommended metadata or guardrails, new primitives or capabilities not yet adopted, and documentation drift inside this repo.
5. Stop at the audit boundary unless the user asks for changes.
   Recommend the smallest safe follow-up item for each confirmed finding instead of editing files by default.

## Guardrails

- Treat the fetched VS Code docs as the external reference and this repo's local `AGENTS.md` files as the local policy baseline.
- If `#tool:web/fetch` cannot reach the docs, say that the audit is incomplete instead of guessing what changed.
- Do not broaden the audit into quiz-generation prompts outside the `.github` customization layer unless the user explicitly asks for that extra scope.
