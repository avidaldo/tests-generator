---
name: quiz-check
description: Run the independent checker on quiz items - a pass without the key (can an option be eliminated from its wording alone? can the item be solved with the source, and can a distractor be defended?) and an audit with the key (feedback, misconceptions, the rules of docs/item-rules.md) - and merge both into the question file with a verdict per item. Use on a batch or review-session JSON when asked to check, verify or audit quiz items, or to calibrate the checker.
argument-hint: <questions.json> [model: sonnet|opus|haiku|fable] [items: first-last]
disable-model-invocation: true
---

# Check quiz items

The checker is two fresh subagents that never saw the items being written: one judges each item without its key (steps A and B), a second one audits it with the key (step C). Code does all the bookkeeping, `qb blind` and `qb attach-checks`; the subagents only judge. Rules, steps and severities are those of `docs/item-rules.md`.

**Paths.** TOOL is the tool repository, three levels above this skill's directory. Run the tool as `uv run --project TOOL qb ...` from any directory. For a question file `DIR/NAME.json` the checker's files go to `DIR/checks/`: `NAME.lint.json`, `NAME.view.json`, `NAME.map.json`, `NAME.blind-checks.json` and `NAME.audit-checks.json`.

## Steps

1. **Lint.** `qb lint --json FILE > DIR/checks/NAME.lint.json`. Exit code 1 only means that some items break rules; go on.
2. **Blind view.** `qb blind FILE --out DIR/checks/NAME.view.json --map DIR/checks/NAME.map.json`. Never read the map, and never name it, the question file or the lint report to the step-A-and-B subagent: the view must be all it knows.
3. **Steps A and B.** Spawn one general-purpose subagent, with the model from the arguments when one is given, and this task: "Read TOOL/.claude/skills/quiz-check/checker.md, sections 'For both passes' and 'Steps A and B', then TOOL/docs/item-rules.md. Check the items of DIR/checks/NAME.view.json [only items n = first to last]. Open no other file. Write your result to DIR/checks/NAME.blind-checks.json and reply with one line: that path and the number of items checked." With more than 15 items, give each subagent a slice of at most 15 items and its own result file (`NAME.blind-checks.1.json`, `.2.json`...), running them in parallel.
4. **Attach steps A and B.** `qb attach-checks FILE RESULT --map DIR/checks/NAME.map.json` for each result file. When it prints problems, send them to the same subagent once and ask it to correct its file; if they remain, stop and report them.
5. **Step C.** Spawn new general-purpose subagents, never the ones from step 3, with the same model: "Read TOOL/.claude/skills/quiz-check/checker.md, sections 'For both passes' and 'Step C', then TOOL/docs/item-rules.md. Audit the items of FILE [only items n = first to last], using the lint report DIR/checks/NAME.lint.json. Write your result to DIR/checks/NAME.audit-checks.json and reply with one line: that path and the number of items audited." Slice as in step 3.
6. **Attach step C.** `qb attach-checks FILE RESULT` for each result file, with the same single correction round.
7. **Report** the lines `qb attach-checks` printed (failures by rule, verdicts and how many were made stricter than the checker's), the model used and where the files are. Don't paste item content into the conversation.

## Ground rules

- You orchestrate; you don't judge items and you don't edit the checker's results, apart from relaying `qb attach-checks` problems in steps 4 and 6.
- If the question file may be open in the editor, ask the user to close it before step 4: the editor's autosave would overwrite the checks.
- A checker of the same model family as the writer shares its blind spots. Prefer another model when one is available; calibration decides which.
