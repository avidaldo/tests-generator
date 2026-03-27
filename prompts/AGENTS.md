# Prompts — Agent Instructions

## Current State

This folder contains the canonical prompt files for the repository, along with prompt design notes and decomposition planning. VS Code is configured to discover prompt files from this folder.

| File | Status | Description |
|------|--------|-------------|
| `inventory.prompt.md` | **Active — Agent 1** | Source file analysis and concept inventory |
| `generate-questions.prompt.md` | **Active — Agent 2** | Question generation in JSON format (one subcategory at a time) |
| `generate-test.prompt.md` | **Deprecated** | Monolithic prompt — superseded by the two-agent pipeline above |
| `metaprompting.prompt.md` | Stable | Prompt design guidelines |

### Pipeline Overview

```
User provides directory paths
        │
        ▼
[inventory.prompt.md]          ← reads all source files once
        │  Output: compact Markdown table (concepts + suggested subcategories)
        ▼
User selects one subcategory row
        │
        ▼
[generate-questions.prompt.md] ← reads only that subcategory's files
        │  Output: JSON file (editor-native, opens with Ctrl+O)
        ▼
[Quiz Editor — human review]   ← mandatory validation gate
        │  Human marks: Pendiente / Revisar / Lista
        ▼
[resources/json_to_moodle_xml.py]  ← deterministic script
        │  Output: Moodle XML (Lista questions only)
        ▼
Moodle import
```

**Intermediate format**: JSON matching `editor/v3/file_io/state_io.py` schema.
- Direct editor import — no conversion step
- Adversarial filter preserved via required `feedback` fields per distractor
- ~30 lines/question vs. ~60–80 for XML → roughly 2× throughput improvement

## Canonical Prompt Authoring Rules

This file is the canonical, tool-agnostic instruction surface for the `prompts/` module.

- Keep `.github/instructions/prompt-authoring.instructions.md` as a VS Code routing adapter only, not as a second source of prompt policy.
- Keep canonical project prompt files under `prompts/` in this repository. Use VS Code settings only to discover that location.
- Use current prompt metadata only. In prompt files, `agent` must be a valid agent identifier such as `ask`, `agent`, `plan`, or a custom agent name available in the workspace.
- Keep prompt instructions focused on a single reusable workflow. If a workflow requires persistent persona, tool restrictions, or handoffs, prefer a custom agent or skill instead of growing one prompt indefinitely.
- When designing or reviewing prompts, consult current official prompting guidance and current VS Code customization docs before changing the file.
- For quiz-generation prompts, preserve the requirement to consult `docs/adversarial_logic_filters.md`.

---

## Design Rationale

### Why Three Separate Agents

The original monolithic `generate-test.prompt.md` performed inventory, generation, and XML formatting in a single agent turn. This caused three failure modes:

- **Context exhaustion**: reading all source files before generating consumed so much context that generation quality degraded for large courses.
- **Output bloat**: Moodle XML + 7 answers × feedback ≈ 50–80 lines/question; after ~15 questions the model began truncating, losing structure, or hallucinating XML syntax.
- **Coupled failures**: a malformed XML tag corrupted otherwise valid question content — format correctness and question quality could not be validated independently.

Splitting into Inventory → Generation → (deterministic) Export isolates each concern.

### Why the Editor is a Mandatory Step

The editor is the human-in-the-loop validation gate, not a convenience tool. It catches domain errors the adversarial filter cannot self-detect, selects the best questions when there is redundancy, adjusts difficulty, and controls what actually reaches students.

### Why JSON as Intermediate Format

Four formats were evaluated (plain GIFT, GIFT + reasoning block, JSON, two-pass XML). JSON with feedback was chosen because:

- **Direct editor import** — generated file opens in the editor immediately with `Ctrl+O`, zero conversion.
- **Adversarial filter preserved** — required `feedback` fields per distractor force the model to validate each one (see `docs/adversarial_logic_filters.md` §1). Removing written feedback removes the primary quality mechanism.
- **~30 lines/question** vs. ~60–80 for XML — roughly 2× throughput improvement.
- **Source traceability** via `source_file` field; versioned schema via `state_io.py`.
- Export to Moodle XML already implemented in `editor/v3/file_io/xml_writer.py`.

Plain GIFT was rejected despite being more compact because the absence of feedback fields removes the adversarial filter entirely.

---

## Files

| File | Description |
|------|-------------|
| `prompts/inventory.prompt.md` | Agent 1: source file inventory and concept extraction |
| `prompts/generate-questions.prompt.md` | Agent 2: question generation in JSON format |
| `resources/json_to_moodle_xml.py` | Export script: JSON → Moodle XML, status-filtered |
