"""Tests for qb.calibration: labels from the editor's statuses and notes, and the report on synthetic items."""

import json

import pytest

from qb.calibration import ExpectedRule, calibration_report, expected_rules, unlabelled_copy


def _question(question_id: str, status: str, notes: str = "", stem: str = "¿Qué variable domina la distancia?") -> dict:
    return {
        "id": question_id,
        "name": f"{question_id}: nombre interno",
        "status": status,
        "review_notes": notes,
        "source_ref": "SAA2/batch-001.json#4",
        "generated_by_model": "some-model",
        "question_text": f"<p>{stem}</p>",
        "general_feedback": "<p>La de mayor rango.</p>",
        "answers": [
            {"text": "<p>Los ingresos, por su rango mayor.</p>", "fraction": "100",
             "feedback": "<p>Correcto. Su rango es miles de veces mayor.</p>", "correct_reviewed": True},
            {"text": "<p>La edad, por su escala más fina.</p>", "fraction": "-50",
             "feedback": "<p>Incorrecto. La finura de la escala no cuenta.</p>"},
            {"text": "<p>Ninguna, k-NN normaliza las distancias.</p>", "fraction": "-50",
             "feedback": "<p>Incorrecto. k-NN usa la distancia tal cual.</p>"},
            {"text": "<p>Ambas por igual, porque se compensan.</p>", "fraction": "-50",
             "feedback": "<p>Incorrecto. Nada las compensa sin escalar.</p>"},
        ],
    }


def _session(*questions: dict) -> dict:
    return {"artifact_type": "review_session", "version": "1.0", "questions": list(questions)}


def _checked(labelled: dict, results: list[tuple[str, list[dict]]]) -> dict:
    """The unlabelled copy with a verdict and failures attached to each item, as /quiz-check would leave them."""
    copy = unlabelled_copy(labelled)
    for item, (verdict, failed) in zip(copy["questions"], results):
        item["checks"] = {"blind": {"answer_index": 0}, "failed": failed, "verdict": verdict}
    return copy


def test_notes_name_rules_alternatives_and_editor_option_numbers() -> None:
    notes = "STEM-OPEN; DIS-TOPIC|DIS-ABSURD 3. Revisar también K-NN y TF-IDF."

    assert expected_rules(notes) == [
        ExpectedRule(frozenset({"STEM-OPEN"}), None),
        ExpectedRule(frozenset({"DIS-TOPIC", "DIS-ABSURD"}), 2),
    ]


def test_the_checker_sees_the_judged_items_without_the_judgement() -> None:
    labelled = _session(_question("A", "review", "DIS-TOPIC 2"), _question("B", "pending"), _question("C", "ready"))

    copy = unlabelled_copy(labelled)

    assert [item["id"] for item in copy["questions"]] == ["A", "C"]
    text = json.dumps(copy, ensure_ascii=False)
    for revealing in ("status", "review_notes", "DIS-TOPIC", "source_ref", "generated_by_model", "correct_reviewed",
                      "nombre interno"):
        assert revealing not in text


def test_hits_near_misses_and_false_alarms() -> None:
    labelled = _session(
        _question("FLAWED_1", "review", "DIS-TOPIC 2"),
        _question("FLAWED_2", "review", "DIS-ABSURD 3"),
        _question("GOOD_1", "ready"),
    )
    checked = _checked(labelled, [
        ("repair", [{"step": "A", "rule": "DIS-TOPIC", "answer_index": 1, "why": "otro tema"}]),
        ("repair", [{"step": "A", "rule": "DIS-ABSURD", "answer_index": 3, "why": "sin sentido"}]),
        ("repair", [{"step": "B", "rule": "DIS-FALSE", "answer_index": 2, "why": "defendible"}]),
    ])

    report = calibration_report(labelled, checked)

    summary = report["summary"]
    assert summary["flawed"] == {"items": 2, "flagged": 2, "rate": 1.0}
    assert summary["good"] == {"items": 1, "flagged": 1, "rate": 1.0}
    assert summary["expected_rules"] == {"hit": 1, "elsewhere": 1}
    assert summary["false_alarms_by_rule"] == {"DIS-FALSE": 1}
    assert summary["key_found"] == {"items": 3, "found": 3}


def test_the_right_option_failed_for_another_reason() -> None:
    labelled = _session(_question("FLAWED", "review", "DIS-TOPIC 2"))
    checked = _checked(labelled, [("repair", [{"step": "A", "rule": "DIS-ELEMENTS", "answer_index": 1, "why": "falta"}])])

    expectation = calibration_report(labelled, checked)["items"][0]["expected"][0]

    assert (expectation["result"], expectation["found_rules"]) == ("other rule", ["DIS-ELEMENTS"])


def test_rules_tested_by_lint_count_as_found() -> None:
    labelled = _session(_question("GRADED", "review", "STEM-GRADED", stem="¿Qué opción describe mejor el efecto?"))
    checked = _checked(labelled, [("repair", [])])

    expectation = calibration_report(labelled, checked)["items"][0]["expected"][0]

    assert (expectation["result"], expectation["steps"]) == ("hit", ["lint"])


def test_notes_with_a_misspelled_rule_are_reported() -> None:
    labelled = _session(_question("A", "review", "DIS-TOPC 2"))

    report = calibration_report(labelled, _checked(labelled, [("repair", [])]))

    assert report["summary"]["unknown_rules_in_notes"] == ["DIS-TOPC"]


def test_a_checked_file_from_other_items_is_refused() -> None:
    labelled = _session(_question("A", "review", "DIS-TOPIC 2"), _question("B", "ready"))
    other = _checked(_session(_question("B", "ready"), _question("A", "review")), [("accept", []), ("accept", [])])

    with pytest.raises(ValueError):
        calibration_report(labelled, other)
