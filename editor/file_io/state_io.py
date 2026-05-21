"""Save and load Stage 4 review-session JSON."""

import json
from pathlib import Path

from models.question import Question, Answer, QuestionStatus
from models.review_session import (
    REVIEW_SESSION_ARTIFACT_TYPE,
    REVIEW_SESSION_VERSION,
    ImportedSource,
    ReviewSession,
)


STAGE3_BATCH_ARTIFACT_KIND = "stage3_batch"
LEGACY_STATE_ARTIFACT_KIND = "legacy_state"


def _serialize_question(question: Question) -> dict:
    return {
        "id": question.id,
        "name": question.name,
        "question_text": question.question_text,
        "general_feedback": question.general_feedback,
        "category_path": question.category_path,
        "status": question.status.value,
        "default_grade": question.default_grade,
        "penalty": question.penalty,
        "single": question.single,
        "shuffle_answers": question.shuffle_answers,
        "answer_numbering": question.answer_numbering,
        "correct_feedback": question.correct_feedback,
        "partially_correct_feedback": question.partially_correct_feedback,
        "incorrect_feedback": question.incorrect_feedback,
        "source_file": question.source_file,
        "source_ref": question.source_ref,
        "origin_kind": question.origin_kind,
        "origin_path": question.origin_path,
        "origin_question_id": question.origin_question_id,
        "generated_by_model": question.generated_by_model,
        "is_easy": question.is_easy,
        "review_notes": question.review_notes,
        "answers": [
            {
                "text": answer.text,
                "fraction": answer.fraction,
                "feedback": answer.feedback,
                "format": answer.format,
                "correct_reviewed": getattr(answer, "correct_reviewed", False),
            }
            for answer in question.answers
        ],
    }


def _serialize_imported_source(imported_source: ImportedSource) -> dict:
    return {
        "origin_kind": imported_source.origin_kind,
        "origin_path": imported_source.origin_path,
        "label": imported_source.label,
    }


def _read_json_payload(filepath: Path) -> dict:
    data = json.loads(filepath.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Expected a top-level JSON object.")
    questions = data.get("questions")
    if not isinstance(questions, list):
        raise ValueError("Expected a top-level 'questions' array.")
    return data


def _looks_like_legacy_state(data: dict) -> bool:
    for question_data in data.get("questions", []):
        if not isinstance(question_data, dict):
            continue
        if question_data.get("origin_kind") == LEGACY_STATE_ARTIFACT_KIND:
            return True
        if any(
            field in question_data
            for field in (
                "source_file",
                "correct_feedback",
                "partially_correct_feedback",
                "incorrect_feedback",
            )
        ):
            return True
    return False


def _detect_json_artifact_kind(data: dict) -> str:
    artifact_type = data.get("artifact_type", "")
    if artifact_type:
        if artifact_type == REVIEW_SESSION_ARTIFACT_TYPE:
            return REVIEW_SESSION_ARTIFACT_TYPE
        raise ValueError(f"Unsupported artifact_type: {artifact_type}")
    if _looks_like_legacy_state(data):
        return LEGACY_STATE_ARTIFACT_KIND
    return STAGE3_BATCH_ARTIFACT_KIND


def _infer_origin_kind(question_data: dict, filepath: Path) -> str:
    if question_data.get("origin_kind"):
        return question_data["origin_kind"]
    if "source_file" in question_data or "correct_feedback" in question_data:
        return LEGACY_STATE_ARTIFACT_KIND
    return STAGE3_BATCH_ARTIFACT_KIND


def _deserialize_question(question_data: dict, filepath: Path) -> Question:
    answers = [
        Answer(
            text=answer["text"],
            fraction=answer["fraction"],
            feedback=answer.get("feedback", ""),
            format=answer.get("format", "html"),
            correct_reviewed=answer.get("correct_reviewed", False),
        )
        for answer in question_data.get("answers", [])
    ]

    status_str = question_data.get("status", "pendiente")
    try:
        status = QuestionStatus(status_str)
    except ValueError:
        status = QuestionStatus.PENDIENTE

    origin_kind = _infer_origin_kind(question_data, filepath)
    origin_path = question_data.get("origin_path", "")
    if not origin_path and origin_kind == "stage3_batch":
        origin_path = str(filepath)

    source_ref = question_data.get("source_ref", "")
    source_file = question_data.get("source_file", "")
    if not source_file and origin_path:
        source_file = Path(origin_path).name

    return Question(
        id=question_data["id"],
        name=question_data["name"],
        question_text=question_data["question_text"],
        general_feedback=question_data.get("general_feedback", ""),
        category_path=question_data.get("category_path", ""),
        answers=answers,
        status=status,
        default_grade=question_data.get("default_grade", "1.0000000"),
        penalty=question_data.get("penalty", "0.0000000"),
        single=question_data.get("single", "true"),
        shuffle_answers=question_data.get("shuffle_answers", "true"),
        answer_numbering=question_data.get("answer_numbering", "abc"),
        correct_feedback=question_data.get("correct_feedback", "<p>Correcto.</p>"),
        partially_correct_feedback=question_data.get("partially_correct_feedback", "<p>Parcialmente correcto.</p>"),
        incorrect_feedback=question_data.get("incorrect_feedback", "<p>Incorrecto.</p>"),
        source_file=source_file,
        source_ref=source_ref,
        origin_kind=origin_kind,
        origin_path=origin_path,
        origin_question_id=question_data.get("origin_question_id", question_data.get("id", "")),
        generated_by_model=question_data.get("generated_by_model", ""),
        is_easy=bool(question_data.get("is_easy", False)),
        review_notes=question_data.get("review_notes", ""),
    )


def _deserialize_review_session(data: dict, filepath: Path) -> ReviewSession:
    questions = [_deserialize_question(question_data, filepath) for question_data in data.get("questions", [])]

    imported_sources = [
        ImportedSource(
            origin_kind=imported_source.get("origin_kind", ""),
            origin_path=imported_source.get("origin_path", ""),
            label=imported_source.get("label", ""),
        )
        for imported_source in data.get("imported_sources", [])
    ]

    review_session = ReviewSession(
        questions=questions,
        imported_sources=imported_sources,
        notes=data.get("notes", ""),
        artifact_type=data.get("artifact_type", REVIEW_SESSION_ARTIFACT_TYPE),
        version=data.get("version", REVIEW_SESSION_VERSION),
    )
    if review_session.imported_sources:
        return review_session
    return ReviewSession.from_questions(review_session.questions, notes=review_session.notes)


def save_review_session(review_session: ReviewSession, filepath: Path) -> None:
    """Save a Stage 4 review session to a JSON file."""
    data = {
        "artifact_type": REVIEW_SESSION_ARTIFACT_TYPE,
        "version": review_session.version,
        "notes": review_session.notes,
        "imported_sources": [
            _serialize_imported_source(imported_source)
            for imported_source in review_session.imported_sources
        ],
        "questions": [_serialize_question(question) for question in review_session.questions],
    }
    filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_review_session(filepath: Path) -> ReviewSession:
    """Load a saved Stage 4 review session or backward-compatible legacy editor state."""
    data = _read_json_payload(filepath)
    artifact_kind = _detect_json_artifact_kind(data)
    if artifact_kind == STAGE3_BATCH_ARTIFACT_KIND:
        raise ValueError(
            "Expected a saved review session JSON, but received a Stage 3 batch JSON. "
            "Use the Stage 3 add actions instead."
        )
    return _deserialize_review_session(data, filepath)


def load_stage3_batch(filepath: Path) -> list[Question]:
    """Load a Stage 3 batch JSON file for import into the current review session."""
    data = _read_json_payload(filepath)
    artifact_kind = _detect_json_artifact_kind(data)
    if artifact_kind != STAGE3_BATCH_ARTIFACT_KIND:
        if artifact_kind in {REVIEW_SESSION_ARTIFACT_TYPE, LEGACY_STATE_ARTIFACT_KIND}:
            raise ValueError(
                "Expected a Stage 3 batch JSON, but received a saved review session JSON. "
                "Use 'Abrir sesión de revisión...' instead."
            )
        raise ValueError(f"Unsupported JSON artifact kind: {artifact_kind}")
    return _deserialize_review_session(data, filepath).questions


def save_state(questions: list[Question], filepath: Path, notes: str = "") -> None:
    """Save the current state to a JSON file."""
    session = ReviewSession.from_questions(questions)
    session.notes = notes
    save_review_session(session, filepath)


def load_state(filepath: Path) -> list[Question]:
    """Load state from a JSON file."""
    return load_review_session(filepath).questions
