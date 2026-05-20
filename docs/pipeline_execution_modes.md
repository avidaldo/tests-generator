# Pipeline Execution Modes

This document explains how to run the quiz-generation pipeline in this repository without mixing the precise manual path with the advanced bulk lanes. The canonical pipeline summary remains in [prompts/AGENTS.md](../prompts/AGENTS.md). This file answers a different question: which execution surface to use for a given situation, where generated artifacts should live, and why the precise prompt-per-stage workflow is still the default.

## Default Principle

The default workflow is still the precise manual lane: one prompt invocation for one well-scoped unit of work. Bulk orchestration exists only where it materially improves unattended execution without weakening the human review boundaries.

Stage 1 and Stage 3 can benefit from orchestration because they naturally decompose into independent units. Stage 2 does not: it is still one merge pass where the taxonomy is reviewed deliberately before downstream generation continues.

## Decision Guide

| Situation | Recommended surface | Why this is the right lane |
| --- | --- | --- |
| One repo, folder, or coherent topic area for Stage 1 | [`prompts/summarize-sources.prompt.md`](../prompts/summarize-sources.prompt.md) | Keeps the extraction focused and easy to validate before scaling out |
| Many repos or folders for Stage 1 — in-session | [`.github/skills/summarize-all-sources/SKILL.md`](../.github/skills/summarize-all-sources/SKILL.md) | Fans out isolated Stage 1 runs while still producing one summary per path |
| Many repos or folders for Stage 1 — background/Copilot CLI | [`.github/agents/stage1-runner.agent.md`](../.github/agents/stage1-runner.agent.md) | Delegates each path to an isolated `source-summarizer` subagent; coordinator context stays small; persists when VS Code closes |
| Merge validated Stage 1 summaries into subcategories | [`prompts/merge-summaries.prompt.md`](../prompts/merge-summaries.prompt.md) | Stage 2 remains a single deliberate taxonomy pass — always human-gated |
| One subcategory for Stage 3, or any run where you want tight surface control | [`prompts/generate-questions.prompt.md`](../prompts/generate-questions.prompt.md) | Keeps one fresh context window per subcategory and one reviewable batch per invocation |
| Folder or multiple subcategory files attached to `generate-questions.prompt.md` | Redirect → [`stage3-runner` agent](../.github/agents/stage3-runner.agent.md) or [`finish-stage3-coverage.prompt.md`](../prompts/finish-stage3-coverage.prompt.md) | `generate-questions.prompt.md` will detect the multi-input and refuse. Use a bulk lane instead. |
| Many subcategories for Stage 3 — in-session breadth-first pass | [`.github/skills/generate-question-batches/SKILL.md`](../.github/skills/generate-question-batches/SKILL.md) | Advances multiple subcategories safely, at most one new batch per subcategory, with checkpointed progress |
| Approved Stage 2 scope, exhaustive Stage 3 — in-session | [`prompts/finish-stage3-coverage.prompt.md`](../prompts/finish-stage3-coverage.prompt.md) | One visible launcher; reuses the exhaustive coverage workflow and manifest discipline underneath |
| Approved Stage 2 scope, exhaustive Stage 3 — background/Copilot CLI | [`.github/agents/stage3-runner.agent.md`](../.github/agents/stage3-runner.agent.md) | Delegates each subcategory to an isolated `batch-generator` subagent; coordinator context stays small; persists when VS Code closes |

## Artifact Path Contract

Generated subject artifacts do not live canonically inside this repository. Every run should use user-provided paths or roots owned by the subject or course workspace.

| Stage | What the user provides | Deterministic artifact rule |
| --- | --- | --- |
| Stage 1 | Stage 1 output root or explicit file path | Write `summary-<repo-or-topic>.md` under the provided root unless the user gave an explicit path |
| Stage 2 | Stage 2 output root | Write one `subcategory-<name>.md` file per approved subcategory |
| Stage 3 | Stage 3 output root or explicit file path | Derive `<subcategory>/batch-###.json` under the provided root, or use the explicit path verbatim |

Implications of this contract:

- Do not assume repo-owned `stage1-*`, `stage2-*`, or `stage3-*` folders as the default destination.
- Keep lightweight manifests or checkpoint files next to the user-owned artifact roots, not buried inside this repository.
- Never overwrite an existing Stage 3 batch implicitly. Create the next free `batch-###.json` unless the user explicitly requests a specific batch number.

## Regular Vs Bulk Execution

The regular lane is prompt-first and intentionally narrow. It is the right default when the user wants tight control, when the scope is small enough to inspect directly, or when the next step depends on human review before more work is justified.

The bulk lanes are advanced and opt-in. They exist for unattended progress where orchestration materially helps, whether that means breadth-first movement across many independent units or repeated Stage 3 batching over an already approved Stage 2 scope. They are not a replacement for review points, and they should not hide complexity behind a single vague command.

### Stage 1 Bulk

Use [`.github/skills/summarize-all-sources/SKILL.md`](../.github/skills/summarize-all-sources/SKILL.md) when a subject spans multiple repos, folders, or files and you want one isolated summary per path. The skill should:

- normalize the inputs into explicit Stage 1 units,
- keep a manifest under the user-provided Stage 1 root,
- fan out only in small batches,
- validate each summary immediately against [summary_format.md](summary_format.md), and
- stop the wave on the first invalid artifact.

This is a bulk convenience lane, not a change in Stage 1 policy. Each produced summary still has to satisfy the same extraction and validation rules as the regular prompt invocation.

### Stage 3 Bulk

Use [`.github/skills/generate-question-batches/SKILL.md`](../.github/skills/generate-question-batches/SKILL.md) when you want a delegated or background breadth-first pass across many Stage 2 subcategory files. The skill should:

- treat each subcategory file as one Stage 3 unit,
- reuse the shared Stage 3 settings for the pass, including one stable batch-wide model label when the run knows it,
- keep a checkpoint manifest under the user-provided Stage 3 root,
- create at most one new batch per subcategory in a single pass,
- validate each written JSON batch before continuing, including the batch-wide `generated_by_model` value when requested, and
- stop on the first invalid artifact instead of silently pushing ahead.

This lane is intentionally breadth-first. If one subcategory needs repeated batching with exact `SURF-*` control, the regular [`generate-questions.prompt.md`](../prompts/generate-questions.prompt.md) invocation is usually the better tool.

### Stage 3 Exhaustive Coverage

The preferred user-facing surface is [`prompts/finish-stage3-coverage.prompt.md`](../prompts/finish-stage3-coverage.prompt.md). It launches the exhaustive Stage 3 lane for an already approved Stage 2 scope while reusing [`.github/skills/finish-question-coverage/SKILL.md`](../.github/skills/finish-question-coverage/SKILL.md) as the implementation workflow. That underlying workflow should:

- require an approved Stage 2 scope rather than inventing missing taxonomy,
- keep a coverage manifest under the user-provided Stage 3 root,
- reuse the shared Stage 3 settings for the run, including one stable batch-wide model label when the run knows it,
- track which `SURF-*` entries each validated batch was meant to cover,
- treat legacy batches without a manifest as existing artifacts but not as automatically tracked coverage,
- continue wave by wave until the selected subcategories are `done`, `needs-fix`, `blocked-upstream`, or `skipped`, and
- stop on the first invalid artifact instead of silently pushing ahead.

Advanced users can still invoke the skill directly, but the prompt launcher is the simpler project-facing entrypoint because it keeps exhaustive Stage 3 discoverable next to the canonical Stage 1–3 prompts.

This lane is still Stage-3-only. It does not replace Stage 2, and it does not make the editor review gate optional.

### Background / Copilot CLI Execution

The coordinator agents are designed for runs that should continue after VS Code closes, or where you want guaranteed context isolation per subcategory (no accumulation across units in the coordinator's window).

**How context isolation works:** The coordinator (e.g., `stage3-runner`) only accumulates one-line manifest entries — one per subcategory. The actual question generation runs in a `batch-generator` subagent that gets its own clean context window and returns only a summary line. The coordinator never sees the full generation output.

**Stage 3 background run:**

```sh
# Select the stage3-runner agent in Copilot CLI
gh copilot suggest --agent stage3-runner \
  "stage2_scope: /path/to/stage2/saa2/ stage3_root: /path/to/stage3-new/ output_language: Castellano"
```

Enable in VS Code settings: `"github.copilot.chat.cli.customAgents.enabled": true`.

Use `/remote on` inside the CLI session to mirror progress to GitHub and monitor from any device.

Use worktree isolation mode (`--worktree-isolation`) for unattended runs — auto-approves all tool calls, no confirmation prompts.

**Stage 1 background run:**

```sh
gh copilot suggest --agent stage1-runner \
  "source_paths: /path/to/repo1, /path/to/repo2 stage1_root: /path/to/stage1-summaries/"
```

**Stage 2 is always manual.** There is no background lane for Stage 2. The taxonomy review is a deliberate human gate; do not attempt to automate or skip it.

**`context: fork` as future upgrade path.** VS Code supports `context: fork` on skills (experimental, requires `github.copilot.chat.skillTool.enabled`). This would allow skills to run in isolated subagents without needing agent files. The custom agent coordinator-worker pattern used here is non-experimental and production-stable. If `context: fork` stabilizes, the worker agents (`batch-generator`, `source-summarizer`) could be replaced by forked skills, removing the need for the `.github/agents/` files. Until then, the agent-based architecture is the correct approach.

## Why Precise Prompts Stay The Default

The prompt-per-stage workflow remains the default because it preserves the strongest review boundaries:

- Stage 1 stays close to the source material, so loss-minimizing extraction can be validated before anything is merged.
- Stage 2 remains one deliberate taxonomy pass instead of being fragmented into automation that hides classification decisions.
- Stage 3 keeps one subcategory per precise run, which reduces drift and keeps JSON batches reviewable.
- The editor remains the mandatory human validation gate before Moodle XML export.

Bulk orchestration is exposed only where it adds real value: Stage 1 fan-out across many independent material paths, Stage 3 breadth-first progress across many independent subcategories, and Stage 3 exhaustive coverage across an already approved Stage 2 scope. Outside those cases, a bulk surface adds more ambiguity than value.
