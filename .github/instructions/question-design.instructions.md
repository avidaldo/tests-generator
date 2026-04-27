---
name: Question Design
description: "Use when generating or reviewing exam questions."
applyTo: 'prompts/generate-questions.prompt.md'
---

- Consult [docs/distractor_design.md](../../docs/distractor_design.md) for distractor strategies, anti-bias rules, and scenario triangulation techniques before designing questions.
- Consult [docs/adversarial_logic_filters.md](../../docs/adversarial_logic_filters.md) §1 and §6 for the adversarial feedback validation mechanism that must be applied to every distractor.
- Use variety in distractor strategies across questions — do not rely on a single strategy.
- All distractors must be plausible to a student with partial knowledge. If you cannot write an unambiguous feedback explaining why a distractor is false, discard it and generate another.
