"""The checker's side of the pipeline: key-less views for steps A and B, and the merge of steps A, B and C into a batch.

The checker is a model, so this module keeps it honest. It validates what the checker wrote, turns the letters of the
shuffled view back into answer indices, derives the failures that follow from steps A and B, and makes a verdict
stricter when it contradicts them. Rule IDs and steps are those of docs/item-rules.md.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, MutableMapping, Sequence
from functools import cache
from importlib import resources
import json
import random
import string

from jsonschema import Draft202012Validator

from qb.html import sanitize
from qb.lint import RULES
from qb.schema import READY_DISTRACTORS, answers_of, is_correct_fraction, json_path, question_label

BLIND_VIEW = "blind_view"
BLIND_MAP = "blind_map"
BLIND_CHECKS = "blind_checks"
AUDIT_CHECKS = "audit_checks"
FORMAT_VERSION = "1.0"

# Rules the checker reports that are warnings on the rule page; every other checker rule is an error.
CHECKER_WARNINGS = frozenset(
    {"KEY-LENGTH", "DIS-LOADED", "DIS-ABSOLUTE", "OPT-PAIR", "FB-HEDGE", "FB-GENERAL", "LANG-CLEAR", "LANG-GLOSSARY"}
)


def blind_view(questions: Sequence[Mapping], seed: int) -> tuple[dict, dict]:
    """Return the key-less view of the questions for steps A and B, and the letter map that undoes its shuffle.

    The view holds what a student sees (the stem and the shuffled options) plus any evidence quotes; no fractions,
    feedback, order or reasoning from which the key could be read. Items are numbered by position (n) because a
    review session may repeat ids. The same seed gives the same shuffle.
    """
    items: list[dict] = []
    letter_maps: dict[str, dict] = {}
    for n, question in enumerate(questions):
        answers = answers_of(question)
        if len(answers) > len(string.ascii_lowercase):
            raise ValueError(f"{question_label(question)}: {len(answers)} options, more than there are letters")
        order = list(range(len(answers)))
        random.Random(f"{seed}:{n}:{question_label(question)}").shuffle(order)
        letters = string.ascii_lowercase[: len(order)]
        item: dict = {
            "n": n,
            "id": question_label(question),
            "stem": sanitize(str(question.get("question_text") or "")),
            "options": {letter: sanitize(str(answers[index].get("text") or "")) for letter, index in zip(letters, order)},
        }
        evidence = [entry for entry in question.get("evidence") or [] if isinstance(entry, Mapping)]
        if evidence:
            item["evidence"] = [{"locator": entry.get("locator"), "quote": entry.get("quote")} for entry in evidence]
        items.append(item)
        letter_maps[str(n)] = {"id": item["id"], "letters": dict(zip(letters, order))}
    view = {"artifact_type": BLIND_VIEW, "version": FORMAT_VERSION, "items": items}
    letter_map = {"artifact_type": BLIND_MAP, "version": FORMAT_VERSION, "seed": seed, "items": letter_maps}
    return view, letter_map


def check_result_errors(data: object) -> list[str]:
    """Return one message per schema violation of a checker result, each with its JSON path; empty when valid."""
    kind = data.get("artifact_type") if isinstance(data, Mapping) else None
    if kind not in (BLIND_CHECKS, AUDIT_CHECKS):
        return [f"$.artifact_type: expected '{BLIND_CHECKS}' or '{AUDIT_CHECKS}', got {kind!r}"]
    errors = sorted(_result_validator(kind).iter_errors(data), key=lambda error: [str(part) for part in error.path])
    return [f"{json_path(error.path)}: {error.message}" for error in errors]


def attach_blind_checks(questions: Sequence[MutableMapping], results: Mapping, letter_map: Mapping) -> list[str]:
    """Store steps A and B in each checked question's checks.blind, with letters turned back into answer indices.

    New A and B results void an earlier step C, so its audit and verdict are removed. Returns the problems found
    (an item missing from the view, an id that changed since `qb blind`, a letter the item doesn't have); nothing is
    stored when there are any. Items the results don't mention are left as they were.
    """
    problems = check_result_errors(results)
    if problems or results["artifact_type"] != BLIND_CHECKS:
        return problems or [f"expected '{BLIND_CHECKS}', got '{results['artifact_type']}'"]

    updates: list[tuple[MutableMapping, dict]] = []
    for item in results["items"]:
        label = f"item {item['n']} ({item['id']})"
        mapped = letter_map.get("items", {}).get(str(item["n"]))
        problem = _item_problem(questions, item, label) or (
            f"{label}: not in the blind view" if mapped is None or mapped.get("id") != item["id"] else None
        )
        if problem:
            problems.append(problem)
            continue
        letters: dict[str, int] = mapped["letters"]
        used = [cue["option"] for cue in item["form"]["eliminated"]]
        used += [item["form"]["picked"]["option"]] if item["form"]["picked"] else []
        used += [item["solve"]["answer"]] if item["solve"]["answer"] else []
        used += [note["option"] for note in item["solve"]["defensible"]]
        if unknown := sorted(set(used) - set(letters)):
            problems.append(f"{label}: no option {', '.join(unknown)} in the blind view")
            continue
        updates.append((questions[item["n"]], _blind_record(item, letters, results.get("model"))))

    problems += _duplicate_items(results["items"])
    if problems:
        return problems
    for question, blind in updates:
        checks = _checks_of(question)
        for stale in ("audit", "verdict", "conflicts"):
            checks.pop(stale, None)
        checks["blind"] = blind
        checks["failed"] = _blind_failures(question, blind)
    return []


def attach_audit_checks(questions: Sequence[MutableMapping], results: Mapping) -> list[str]:
    """Store step C in each checked question's checks.audit and settle the item's verdict in checks.verdict.

    The verdict is step C's, made stricter when it contradicts the record: an item is not accepted while the blind
    solver missed the key, while it keeps a distractor that failed an error-level rule in step A or B, with fewer than
    three distractors kept, or with error-level findings of its own. Each contradiction goes to checks.conflicts.
    Returns the problems found; nothing is stored when there are any.
    """
    problems = check_result_errors(results)
    if problems or results["artifact_type"] != AUDIT_CHECKS:
        return problems or [f"expected '{AUDIT_CHECKS}', got '{results['artifact_type']}'"]

    updates: list[tuple[MutableMapping, dict]] = []
    for item in results["items"]:
        label = f"item {item['n']} ({item['id']})"
        if problem := _item_problem(questions, item, label):
            problems.append(problem)
            continue
        question = questions[item["n"]]
        blind = _checks_of(question).get("blind")
        if not isinstance(blind, Mapping):
            problems.append(f"{label}: no step A and B results; attach them first")
            continue
        answer_count = len(answers_of(question))
        distractors = set(range(answer_count)) - _key_indexes(question)
        if out_of_range := sorted(
            finding["answer_index"] for finding in item["findings"]
            if finding["answer_index"] is not None and finding["answer_index"] >= answer_count
        ):
            problems.append(f"{label}: findings point at options {out_of_range}, the item has {answer_count}")
            continue
        decided = [decision["answer_index"] for decision in item["options"]]
        if sorted(decided) != sorted(distractors):
            problems.append(f"{label}: decisions for options {sorted(decided)}, expected one per distractor "
                            f"{sorted(distractors)}")
            continue
        updates.append((question, item))

    problems += _duplicate_items(results["items"])
    if problems:
        return problems
    for question, item in updates:
        checks = _checks_of(question)
        audit = {key: item[key] for key in ("findings", "options", "verdict", "repair") if key in item}
        if results.get("model"):
            audit["model"] = results["model"]
        failed = _blind_failures(question, checks["blind"])
        failed += [{"step": "C", **finding} for finding in item["findings"]]
        conflicts = _verdict_conflicts(question, failed, item)
        checks["audit"] = audit
        checks["failed"] = failed
        checks["conflicts"] = conflicts
        checks["verdict"] = "reject" if item["verdict"] == "reject" else (
            "repair" if item["verdict"] == "repair" or conflicts else "accept"
        )
    return []


def rule_severity(rule: str) -> str:
    """Severity of a rule on the rule page: lint rules carry their own, checker rules are errors unless listed."""
    if rule in RULES:
        return RULES[rule][0]
    return "warning" if rule in CHECKER_WARNINGS else "error"


def _blind_record(item: Mapping, letters: Mapping[str, int], model: str | None) -> dict:
    picked = item["form"]["picked"]
    solve = item["solve"]
    record = {
        "eliminated": [
            {"answer_index": letters[cue["option"]], "rule": cue["rule"], "why": cue["why"]}
            for cue in item["form"]["eliminated"]
        ],
        "picked": None if picked is None else {
            "answer_index": letters[picked["option"]], "rule": picked["rule"], "why": picked["why"]
        },
        "answer_index": None if solve["answer"] is None else letters[solve["answer"]],
        "confidence": solve["confidence"],
        "why": solve["why"],
        "defensible": [{"answer_index": letters[note["option"]], "why": note["why"]} for note in solve["defensible"]],
    }
    if model:
        record["model"] = model
    return record


def _blind_failures(question: Mapping, blind: Mapping) -> list[dict]:
    """The failures steps A and B imply: a missed key, defensible distractors, options told apart by their wording."""
    keys = _key_indexes(question)
    failures: list[dict] = []
    if blind["answer_index"] not in keys:
        failures.append({"step": "B", "rule": "KEY-UNIQUE", "answer_index": blind["answer_index"], "why": blind["why"]})
    failures += [
        {"step": "B", "rule": "DIS-FALSE", **note} for note in blind["defensible"] if note["answer_index"] not in keys
    ]
    failures += [{"step": "A", **cue} for cue in blind["eliminated"]]
    picked = blind["picked"]
    if picked is not None and picked["answer_index"] in keys:
        failures.append({"step": "A", **picked})
    return failures


def _verdict_conflicts(question: Mapping, failed: Sequence[Mapping], audit_item: Mapping) -> list[str]:
    if audit_item["verdict"] == "reject":
        return []
    keys = _key_indexes(question)
    errors = [failure for failure in failed if rule_severity(failure["rule"]) == "error"]
    conflicts: list[str] = []
    if any(failure["rule"] == "KEY-UNIQUE" for failure in errors):
        conflicts.append("the blind solver didn't choose the key (KEY-UNIQUE)")
    for failure in errors:
        if failure["step"] == "A" and failure["answer_index"] in keys:
            conflicts.append(f"the key can be told apart by its wording ({failure['rule']})")
    # A missed key is a fault of the item, already reported above, not of the distractor the solver chose.
    option_errors = [failure for failure in errors if failure["rule"] != "KEY-UNIQUE"]
    decisions = {decision["answer_index"]: decision["decision"] for decision in audit_item["options"]}
    for index, decision in sorted(decisions.items()):
        broken = sorted({failure["rule"] for failure in option_errors if failure["answer_index"] == index})
        if decision != "drop" and broken:
            conflicts.append(f"option {index + 1} is marked {decision} but breaks {', '.join(broken)}")
    kept = sum(1 for decision in decisions.values() if decision == "keep")
    if kept < READY_DISTRACTORS:
        conflicts.append(f"{kept} distractors kept, {READY_DISTRACTORS} needed")
    if sum(1 for decision in decisions.values() if decision == "spare") > 1:
        conflicts.append("more than one spare distractor")
    if audit_item["verdict"] == "accept":
        own_errors = sorted({f["rule"] for f in audit_item["findings"] if rule_severity(f["rule"]) == "error"})
        if own_errors:
            conflicts.append(f"accepted with error-level findings: {', '.join(own_errors)}")
    return conflicts


def _item_problem(questions: Sequence[Mapping], item: Mapping, label: str) -> str | None:
    if item["n"] >= len(questions):
        return f"{label}: the file has {len(questions)} questions"
    if question_label(questions[item["n"]]) != item["id"]:
        return f"{label}: the question at that position is {question_label(questions[item['n']])}"
    return None


def _duplicate_items(items: Sequence[Mapping]) -> list[str]:
    counts = Counter(item["n"] for item in items)
    return [f"item {n} appears more than once" for n, count in sorted(counts.items()) if count > 1]


def _key_indexes(question: Mapping) -> set[int]:
    return {index for index, answer in enumerate(answers_of(question)) if is_correct_fraction(answer.get("fraction"))}


def _checks_of(question: MutableMapping) -> dict:
    if not isinstance(question.get("checks"), dict):
        question["checks"] = {}
    return question["checks"]


@cache
def _result_validator(kind: str) -> Draft202012Validator:
    schema_text = resources.files("qb").joinpath("schemas/check-result.schema.json").read_text(encoding="utf-8")
    schema = json.loads(schema_text)
    return Draft202012Validator({"$defs": schema["$defs"], "$ref": f"#/$defs/{kind}"})
