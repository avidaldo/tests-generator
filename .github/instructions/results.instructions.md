---
name: Results Privacy And Notebook Rules
description: Privacy and notebook authoring rules for exam analysis work.
applyTo: results/**
---

- Canonical results instructions live in [results/AGENTS.md](../../results/AGENTS.md). Follow that file as the source of truth for the `results/` module.
- Student data privacy is the controlling constraint. Never commit notebook outputs or surface personal data from `results/data/`.
- Notebook-specific authoring rules also come from [notebooks.instructions.md](notebooks.instructions.md); keep outputs stripped and prefer small, explanation-first cells.
- Keep raw Spanish CSV column names unchanged unless the task explicitly includes a migration step.