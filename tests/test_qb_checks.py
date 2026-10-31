"""Tests for qb.checks: the checker's key-less view and the merge of its results, on synthetic items."""

import copy
import json
import os
from pathlib import Path
import re

from qb.checks import attach_audit_checks, attach_blind_checks, blind_view, check_result_errors
from qb.cli import main
from qb.html import sanitize

CHECKER_INSTRUCTIONS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "quiz-check" / "checker.md"


def _item(question_id: str = "T_Q001") -> dict:
    return {
        "id": question_id,
        "question_text": "<p>Un modelo k-NN usa la edad y los ingresos sin escalar. ¿Qué variable domina la distancia?</p>",
        "general_feedback": "<p>SECRET-GENERAL la variable de mayor rango domina.</p>",
        "claim": "SECRET-CLAIM",
        "answers": [
            {"text": "<p>Los ingresos, por su mayor rango.</p>", "fraction": "100",
             "feedback": "<p>SECRET-FEEDBACK-0</p>", "why_right": "SECRET-WHY-RIGHT"},
            {"text": "<p>La edad, por su escala más fina.</p>", "fraction": "-50", "feedback": "<p>SECRET-FEEDBACK-1</p>"},
            {"text": "<p>Ninguna, k-NN normaliza las distancias.</p>", "fraction": "-50",
             "feedback": "<p>SECRET-FEEDBACK-2</p>"},
            {"text": "<p>Ambas por igual, se compensan.</p>", "fraction": "-50", "feedback": "<p>SECRET-FEEDBACK-3</p>"},
        ],
    }


def _letter(letter_map: dict, n: int, answer_index: int) -> str:
    return next(letter for letter, index in letter_map["items"][str(n)]["letters"].items() if index == answer_index)


def _blind_results(letter_map: dict, *, answer: int = 0, eliminated: tuple[int, ...] = (),
                   defensible: tuple[int, ...] = ()) -> dict:
    return {
        "artifact_type": "blind_checks",
        "version": "1.0",
        "model": "test-model",
        "items": [{
            "n": 0,
            "id": "T_Q001",
            "form": {
                "eliminated": [{"option": _letter(letter_map, 0, index), "rule": "DIS-TOPIC", "why": "otro tema"}
                               for index in eliminated],
                "picked": None,
            },
            "solve": {
                "answer": _letter(letter_map, 0, answer),
                "confidence": "high",
                "why": "la distancia suma diferencias sin escalar",
                "defensible": [{"option": _letter(letter_map, 0, index), "why": "defendible"} for index in defensible],
            },
        }],
    }


def _audit_results(verdict: str = "accept", decisions: tuple[str, str, str] = ("keep", "keep", "keep")) -> dict:
    item = {
        "n": 0,
        "id": "T_Q001",
        "findings": [],
        "options": [{"answer_index": index, "decision": decision, "why": "nota"}
                    for index, decision in zip((1, 2, 3), decisions)],
        "verdict": verdict,
    }
    if verdict == "repair":
        item["repair"] = "reescribir la opción 2"
    return {"artifact_type": "audit_checks", "version": "1.0", "items": [item]}


def test_the_skeletons_in_the_checker_instructions_match_the_schema() -> None:
    skeletons = re.findall(r"```json\n(.*?)```", CHECKER_INSTRUCTIONS.read_text(encoding="utf-8"), re.S)

    assert [json.loads(skeleton)["artifact_type"] for skeleton in skeletons] == ["blind_checks", "audit_checks"]
    assert [check_result_errors(json.loads(skeleton)) for skeleton in skeletons] == [[], []]


def test_the_blind_view_shows_stem_and_options_and_nothing_that_reveals_the_key() -> None:
    view, _ = blind_view([_item()], seed=1)

    assert "SECRET" not in json.dumps(view)
    assert "fraction" not in json.dumps(view)
    assert sorted(view["items"][0]["options"].values()) == sorted(sanitize(a["text"]) for a in _item()["answers"])


def test_the_letter_map_undoes_the_shuffle_and_the_seed_fixes_it() -> None:
    questions = [_item(f"T_Q{number:03}") for number in range(10)]

    view, letter_map = blind_view(questions, seed=3)

    for item in view["items"]:
        for letter, index in letter_map["items"][str(item["n"])]["letters"].items():
            assert item["options"][letter] == sanitize(questions[item["n"]]["answers"][index]["text"])
    assert blind_view(questions, seed=3) == (view, letter_map)
    assert blind_view(questions, seed=4)[0] != view


def test_steps_a_and_b_become_failures_by_answer_index() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)

    problems = attach_blind_checks(questions, _blind_results(letter_map, answer=2, eliminated=(1,), defensible=(3,)),
                                   letter_map)

    assert problems == []
    failed = {(failure["step"], failure["rule"], failure["answer_index"]) for failure in questions[0]["checks"]["failed"]}
    assert failed == {("B", "KEY-UNIQUE", 2), ("B", "DIS-FALSE", 3), ("A", "DIS-TOPIC", 1)}
    assert questions[0]["checks"]["blind"]["model"] == "test-model"


def test_invalid_results_change_nothing() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)
    unknown_letter = _blind_results(letter_map)
    unknown_letter["items"][0]["solve"]["answer"] = "z"
    rule_not_tested_in_step_a = _blind_results(letter_map, eliminated=(1,))
    rule_not_tested_in_step_a["items"][0]["form"]["eliminated"][0]["rule"] = "STEM-GRADED"

    assert attach_blind_checks(questions, unknown_letter, letter_map) == ["item 0 (T_Q001): no option z in the blind view"]
    assert attach_blind_checks(questions, rule_not_tested_in_step_a, letter_map)
    assert questions == [_item()]


def test_step_c_needs_steps_a_and_b_first() -> None:
    questions = [_item()]

    assert attach_audit_checks(questions, _audit_results()) == [
        "item 0 (T_Q001): no step A and B results; attach them first"
    ]


def test_a_clean_item_is_accepted() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)
    attach_blind_checks(questions, _blind_results(letter_map), letter_map)

    assert attach_audit_checks(questions, _audit_results()) == []
    assert questions[0]["checks"]["verdict"] == "accept"
    assert questions[0]["checks"]["conflicts"] == []


def test_an_accepted_item_that_keeps_a_failed_distractor_is_made_stricter() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)
    attach_blind_checks(questions, _blind_results(letter_map, eliminated=(1,)), letter_map)

    attach_audit_checks(questions, _audit_results("accept", ("keep", "keep", "keep")))

    assert questions[0]["checks"]["verdict"] == "repair"
    assert questions[0]["checks"]["conflicts"] == ["option 2 is marked keep but breaks DIS-TOPIC"]


def test_a_missed_key_and_too_few_distractors_block_acceptance() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)
    attach_blind_checks(questions, _blind_results(letter_map, answer=2), letter_map)

    attach_audit_checks(questions, _audit_results("accept", ("keep", "keep", "drop")))

    assert questions[0]["checks"]["conflicts"] == [
        "the blind solver didn't choose the key (KEY-UNIQUE)",
        "2 distractors kept, 3 needed",
    ]
    assert questions[0]["checks"]["verdict"] == "repair"


def test_new_blind_results_void_an_earlier_audit() -> None:
    questions = [_item()]
    _, letter_map = blind_view(questions, seed=1)
    attach_blind_checks(questions, _blind_results(letter_map), letter_map)
    attach_audit_checks(questions, _audit_results())

    attach_blind_checks(questions, _blind_results(letter_map, defensible=(1,)), letter_map)

    assert {"audit", "verdict", "conflicts"}.isdisjoint(questions[0]["checks"])


def test_the_command_line_round_trip_and_a_failed_attach_leaves_the_file_alone(tmp_path: Path) -> None:
    batch_path, view_path, map_path = tmp_path / "batch.json", tmp_path / "view.json", tmp_path / "map.json"
    batch_path.write_text(json.dumps({"version": "1.0", "questions": [_item()]}), encoding="utf-8")
    assert main(["blind", str(batch_path), "--out", str(view_path), "--map", str(map_path)]) == 0
    letter_map = json.loads(map_path.read_text(encoding="utf-8"))
    results_path = tmp_path / "blind-checks.json"
    results_path.write_text(json.dumps(_blind_results(letter_map, defensible=(1,))), encoding="utf-8")

    assert main(["attach-checks", str(batch_path), str(results_path)]) == 1
    before = batch_path.read_bytes()
    broken = copy.deepcopy(_blind_results(letter_map))
    broken["items"][0]["id"] = "OTHER"
    (tmp_path / "broken.json").write_text(json.dumps(broken), encoding="utf-8")
    assert main(["attach-checks", str(batch_path), str(tmp_path / "broken.json"), "--map", str(map_path)]) == 1
    assert batch_path.read_bytes() == before

    assert main(["attach-checks", str(batch_path), str(results_path), "--map", str(map_path)]) == 0
    checks = json.loads(batch_path.read_text(encoding="utf-8"))["questions"][0]["checks"]
    assert [failure["rule"] for failure in checks["failed"]] == ["DIS-FALSE"]


def test_the_summary_counts_only_verdicts_the_code_changed(tmp_path: Path, capsys) -> None:
    batch_path, view_path, map_path = tmp_path / "batch.json", tmp_path / "view.json", tmp_path / "map.json"
    batch_path.write_text(json.dumps({"version": "1.0", "questions": [_item("T_Q001"), _item("T_Q002")]}),
                          encoding="utf-8")
    main(["blind", str(batch_path), "--out", str(view_path), "--map", str(map_path)])
    letter_map = json.loads(map_path.read_text(encoding="utf-8"))
    blind = _blind_results(letter_map, defensible=(1,))
    blind["items"].append({**copy.deepcopy(_blind_results(letter_map)["items"][0]), "n": 1, "id": "T_Q002"})
    blind["items"][1]["solve"]["answer"] = _letter(letter_map, 1, 0)
    # The second item has a conflict too, but its step C already says repair: nothing for the code to change.
    blind["items"][1]["solve"]["defensible"] = [{"option": _letter(letter_map, 1, 1), "why": "defendible"}]
    (tmp_path / "blind.json").write_text(json.dumps(blind), encoding="utf-8")
    main(["attach-checks", str(batch_path), str(tmp_path / "blind.json"), "--map", str(map_path)])
    audit = _audit_results("accept")
    audit["items"].append({**copy.deepcopy(audit["items"][0]), "n": 1, "id": "T_Q002", "verdict": "repair",
                           "repair": "acortar la clave"})
    (tmp_path / "audit.json").write_text(json.dumps(audit), encoding="utf-8")
    capsys.readouterr()

    assert main(["attach-checks", str(batch_path), str(tmp_path / "audit.json")]) == 0

    assert "verdicts: repair 2 (1 made stricter than the checker's)" in capsys.readouterr().out


def test_rewriting_a_file_keeps_its_permissions(tmp_path: Path) -> None:
    batch_path = tmp_path / "batch.json"
    batch_path.write_text(json.dumps({"version": "1.0", "questions": [_item()]}), encoding="utf-8")
    batch_path.chmod(0o640)
    main(["blind", str(batch_path), "--out", str(tmp_path / "view.json"), "--map", str(tmp_path / "map.json")])
    letter_map = json.loads((tmp_path / "map.json").read_text(encoding="utf-8"))
    (tmp_path / "blind.json").write_text(json.dumps(_blind_results(letter_map)), encoding="utf-8")

    assert main(["attach-checks", str(batch_path), str(tmp_path / "blind.json"), "--map", str(tmp_path / "map.json")]) == 0

    assert batch_path.stat().st_mode & 0o777 == 0o640
    umask = os.umask(0)
    os.umask(umask)
    assert (tmp_path / "view.json").stat().st_mode & 0o777 == 0o666 & ~umask
