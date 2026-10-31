"""Calibration of the checker on items a teacher has already judged.

The labelled file is a review session. Status "ready" (Lista) marks an item the teacher judged good and "review"
(Revisar) one judged flawed; the notes of a flawed item name the rules it breaks, with the option number the editor
shows: "STEM-OPEN; DIS-TOPIC 3". "DIS-TOPIC|DIS-ABSURD 3" accepts either rule. Items with any other status are left
out. unlabelled_copy() is what the checker gets; calibration_report() compares what it found with the teacher.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import re

from qb.checks import known_rules, rule_severity
from qb.lint import lint_question
from qb.schema import REVIEW_SESSION, answers_of, is_correct_fraction, normalize_status, question_label

GOOD = "good"
FLAWED = "flawed"
FLAGGED_VERDICTS = ("repair", "reject")
_LABELS = {"ready": GOOD, "review": FLAWED}
# What the checker may see: what students see plus the writer's reasoning. Status, notes, provenance and earlier
# checks would tell it the teacher's judgement.
_ITEM_FIELDS = ("id", "question_text", "general_feedback", "evidence", "claim", "stem_premises", "target_id", "qtype")
_ANSWER_FIELDS = ("text", "fraction", "feedback", "misconception", "why_right", "why_wrong")
_RULE_ID = r"(?:STEM|KEY|DIS|OPT|FB|LANG|GROUND|FMT)-[A-Z]+"
_EXPECTED = re.compile(rf"\b({_RULE_ID}(?:\|{_RULE_ID})*)(?:\s+(\d+))?")


@dataclass(frozen=True)
class ExpectedRule:
    """A rule the teacher says an item breaks: any of `rules`, at `answer_index` (None for the whole item)."""

    rules: frozenset[str]
    answer_index: int | None


def item_label(question: Mapping) -> str | None:
    """'good', 'flawed', or None for an item the teacher hasn't judged."""
    return _LABELS.get(normalize_status(question.get("status")))


def expected_rules(notes: str) -> list[ExpectedRule]:
    """The rules named in a flawed item's notes; option numbers count from 1, as the editor shows them."""
    return [
        ExpectedRule(frozenset(match[1].split("|")), int(match[2]) - 1 if match[2] else None)
        for match in _EXPECTED.finditer(notes or "")
    ]


def unlabelled_copy(labelled: Mapping) -> dict:
    """The judged items, in order, as the checker may see them: learner-facing text and reasoning, nothing else."""
    questions = []
    for question in labelled["questions"]:
        if item_label(question) is None:
            continue
        item = {field: question[field] for field in _ITEM_FIELDS if field in question}
        item["answers"] = [
            {field: answer[field] for field in _ANSWER_FIELDS if field in answer} for answer in answers_of(question)
        ]
        questions.append(item)
    return {"artifact_type": REVIEW_SESSION, "version": "1.0", "questions": questions}


def calibration_report(labelled: Mapping, checked: Mapping) -> dict:
    """Compare the checker's results on the unlabelled copy with the teacher's labels.

    Every rule the teacher named on a flawed item is a hit when the checker or lint reports one of its rules on
    the same option (or anywhere, for an item-level rule); every error-level failure on a good item is a false alarm.
    Raises ValueError when the checked file isn't the unlabelled copy of the labelled one.
    """
    judged = [question for question in labelled["questions"] if item_label(question)]
    checked_items = list(checked["questions"])
    if [question_label(question) for question in judged] != [question_label(item) for item in checked_items]:
        raise ValueError("the checked file doesn't hold the labelled items in the same order")

    rows = [_item_row(n, teacher, item) for n, (teacher, item) in enumerate(zip(judged, checked_items))]
    audited = [row for row in rows if row["verdict"] is not None]
    summary: dict = {"items": len(rows), "audited": len(audited)}
    for label in (FLAWED, GOOD):
        group = [row for row in audited if row["label"] == label]
        flagged = sum(1 for row in group if row["verdict"] in FLAGGED_VERDICTS)
        summary[label] = {"items": len(group), "flagged": flagged, "rate": flagged / len(group) if group else None}
    expectations = [expectation for row in audited for expectation in row["expected"]]
    summary["expected_rules"] = dict(Counter(expectation["result"] for expectation in expectations))
    summary["missed_by_rule"] = dict(Counter(
        expectation["rules"] for expectation in expectations if expectation["result"] == "missed"
    ))
    summary["false_alarms_by_rule"] = dict(Counter(
        alarm["rule"] for row in audited if row["label"] == GOOD for alarm in row["errors"]
    ))
    solved = [row["solved"] for row in audited if row["solved"] is not None]
    summary["key_found"] = {"items": len(solved), "found": sum(solved)}
    summary["unknown_rules_in_notes"] = sorted({rule for row in rows for rule in row["unknown_rules"]})
    return {"summary": summary, "items": rows}


def _item_row(n: int, teacher: Mapping, item: Mapping) -> dict:
    checks = item.get("checks") if isinstance(item.get("checks"), Mapping) else {}
    found = [
        {"step": failure["step"], "rule": failure["rule"], "answer_index": failure.get("answer_index")}
        for failure in checks.get("failed", [])
    ]
    found += [
        {"step": "lint", "rule": finding.rule, "answer_index": finding.answer_index}
        for finding in lint_question(item, None, with_reasoning=False)
    ]
    label = item_label(teacher)
    expected = expected_rules(str(teacher.get("review_notes") or "")) if label == FLAWED else []
    known = known_rules()
    blind = checks.get("blind") if isinstance(checks.get("blind"), Mapping) else None
    keys = {index for index, answer in enumerate(answers_of(item)) if is_correct_fraction(answer.get("fraction"))}
    return {
        "n": n,
        "id": question_label(item),
        "label": label,
        "verdict": checks.get("verdict"),
        "solved": None if blind is None else blind.get("answer_index") in keys,
        "expected": [_expectation_result(expectation, found) for expectation in expected],
        "errors": [failure for failure in found if rule_severity(failure["rule"]) == "error"],
        "unknown_rules": sorted(rule for expectation in expected for rule in expectation.rules - known),
    }


def _expectation_result(expectation: ExpectedRule, found: Sequence[Mapping]) -> dict:
    """hit: the rule on the option; other rule: the option failed an error-level rule but not this one; elsewhere:
    the rule on another option; missed: none of these."""
    matching = [failure for failure in found if failure["rule"] in expectation.rules]
    on_target = [
        failure for failure in matching
        if expectation.answer_index is None or failure["answer_index"] == expectation.answer_index
    ]
    other_rule = [
        failure for failure in found
        if expectation.answer_index is not None and failure["answer_index"] == expectation.answer_index
        and rule_severity(failure["rule"]) == "error"
    ]
    if on_target:
        result, evidence = "hit", on_target
    elif other_rule:
        result, evidence = "other rule", other_rule
    elif matching:
        result, evidence = "elsewhere", matching
    else:
        result, evidence = "missed", []
    return {
        "rules": "|".join(sorted(expectation.rules)),
        "option": None if expectation.answer_index is None else expectation.answer_index + 1,
        "result": result,
        "steps": sorted({failure["step"] for failure in evidence}),
        "found_rules": sorted({failure["rule"] for failure in evidence}),
    }
