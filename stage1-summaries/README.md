# Stage 1 Summary Artifacts

This folder stores saved outputs from `prompts/summarize-sources.prompt.md`.

Recommended layout:

- one subfolder per subject, for example `stage1-summaries/ia25/`
- one Stage 1 artifact per coherent source unit, for example `summary-ia25-background.md`
- one lightweight manifest per subject run, for example `manifest.md`

Recommended manifest statuses:

- `pending`
- `running`
- `done`
- `needs-fix`

Batch guardrails:

- fan out only 2 to 4 Stage 1 units at a time
- validate every written artifact before launching more units
- stop on the first invalid artifact and fix it before continuing

Minimum validation commands:

- `rg -n '^# (File Inventory|Content|Cross-References)$' stage1-summaries/<subject>/summary-*.md`
- `rg -c '^\| [0-9]+ \| ' stage1-summaries/<subject>/summary-*.md`
- `rg -n '^```' stage1-summaries/<subject>/summary-*.md`

See [docs/summary_format.md](../docs/summary_format.md) for the canonical Stage 1 format.
