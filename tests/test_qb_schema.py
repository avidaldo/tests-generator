"""Tests for qb.schema: file kinds, batch schema, statuses and answer shape."""

from qb.schema import (
    BATCH,
    REVIEW_SESSION,
    answer_shape_problems,
    artifact_kind,
    batch_schema_errors,
    expected_distractors,
    normalize_status,
)


def _answer(fraction: str, text: str = "<p>Opción</p>") -> dict:
    return {"text": text, "fraction": fraction, "feedback": "<p>Explicación de la opción.</p>", "format": "html"}


def _v1_question() -> dict:
    return {
        "id": "NORM_Q001",
        "name": "Q001: Normalización",
        "question_text": "<p>Enunciado</p>",
        "general_feedback": "<p>Explicación</p>",
        "category_path": "$course$/top/Prueba",
        "status": "pendiente",
        "source_ref": "NORM-01",
        "answers": [_answer("100")] + [_answer("-50", f"<p>D{index}</p>") for index in range(6)],
    }


def test_a_v1_batch_matches_the_schema() -> None:
    assert batch_schema_errors({"version": "1.0", "questions": [_v1_question()]}) == []


def test_a_v2_batch_with_reasoning_fields_matches_the_schema() -> None:
    question = _v1_question() | {
        "target_id": "S06-T03",
        "qtype": "case",
        "tier": "core",
        "evidence": [{"locator": "saa/metrics.ipynb#Precision", "quote": "Precision is the share of..."}],
        "claim": "Precision measures how many predicted positives are correct.",
        "stem_premises": ["A spam filter flags 100 emails."],
    }
    question["answers"][1] |= {
        "misconception": {"belief": "Precision counts the positives found.", "origin": "inferred"},
        "why_wrong": "That is recall.",
    }

    assert batch_schema_errors({"version": "2.0", "questions": [question]}) == []


def test_schema_errors_name_the_offending_path() -> None:
    question = _v1_question() | {"surface": "SURF-01"}
    question["answers"][0]["fraction"] = "cien"

    errors = batch_schema_errors({"version": "1.0", "questions": [question]})

    assert any(error.startswith("$.questions[0]:") and "surface" in error for error in errors)
    assert any(error.startswith("$.questions[0].answers[0].fraction:") for error in errors)


def test_artifact_kind_tells_sessions_from_batches() -> None:
    assert artifact_kind({"version": "1.0", "questions": [_v1_question()]}) == BATCH
    assert artifact_kind({"artifact_type": "review_session", "questions": []}) == REVIEW_SESSION
    assert artifact_kind({"questions": [_v1_question() | {"correct_feedback": "<p>Bien</p>"}]}) == REVIEW_SESSION


def test_expected_distractors_depend_on_the_kind_and_status() -> None:
    session = {"artifact_type": "review_session", "questions": []}

    assert expected_distractors({"version": "1.0", "questions": []}, {}) == 6
    assert expected_distractors({"version": "2.0", "questions": []}, {}) == 4
    assert expected_distractors(session, {"status": "lista"}) == 3
    assert expected_distractors(session, {"status": "review"}) is None


def test_answer_shape_problems() -> None:
    assert answer_shape_problems(["100", "-50", "-50", "-50"], 3) == []
    assert answer_shape_problems(["100", "100", "-50"], 3) == [("correct_count", 2, 1), ("distractor_count", 1, 3)]
    assert answer_shape_problems(["-50", "-50"], None) == [("correct_count", 0, 1)]


def test_normalize_status_maps_legacy_values() -> None:
    assert [normalize_status(value) for value in ("pendiente", "revisar", "lista", "ready", None)] == [
        "pending", "review", "ready", "ready", "pending",
    ]
