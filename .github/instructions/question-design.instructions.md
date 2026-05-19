---
name: Question Design
description: "Use when generating or reviewing exam questions."
applyTo: 'prompts/generate-questions.prompt.md'
---

- Consult [docs/distractor_design.md](../../docs/distractor_design.md) for distractor strategies, anti-bias rules, and scenario triangulation techniques before designing questions.
- Consult [docs/adversarial_logic_filters.md](../../docs/adversarial_logic_filters.md) §1 and §6 for the adversarial feedback validation mechanism that must be applied to every distractor.
- Treat answer-length bias as an explicit validation step, not as general advice only: compare normalized visible option text, ignore HTML wrappers, and rebalance the answers if the correct option is uniquely the longest or shortest by a clear margin.
