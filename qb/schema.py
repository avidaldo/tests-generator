"""Structure of question files: which kind a file is, schema validation, statuses and answer shape."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from functools import cache
from importlib import resources
import json
from pathlib import Path

from jsonschema import Draft202012Validator


REVIEW_SESSION = "review_session"
BATCH = "batch"

STATUSES = ("pending", "review", "ready")
_LEGACY_STATUSES = {"pendiente": "pending", "revisar": "review", "lista": "ready"}
# Fields that only the editor writes: a file carrying them is an old saved session, not a generated batch.
_EDITOR_ONLY_FIELDS = ("source_file", "correct_feedback", "partially_correct_feedback", "incorrect_feedback")

MOODLE_DEFAULTS = {
    "default_grade": "1.0000000",
    "penalty": "0.0000000",
    "single": "true",
    "shuffle_answers": "true",
    "answer_numbering": "abc",
    "correct_feedback": "<p>Correcto.</p>",
    "partially_correct_feedback": "<p>Parcialmente correcto.</p>",
    "incorrect_feedback": "<p>Incorrecto.</p>",
}

READY_DISTRACTORS = 3
BATCH_DISTRACTORS = {"1.0": 6, "2.0": 4}


def load_json(path: Path) -> dict:
    """Read a question file: a JSON object with a 'questions' array."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError(f"{path}: expected a JSON object with a 'questions' array.")
    return data


def artifact_kind(data: Mapping) -> str:
    """Tell a generated batch from a review session saved by the editor (current or legacy format)."""
    if data.get("artifact_type") == REVIEW_SESSION:
        return REVIEW_SESSION
    for question in data.get("questions", []):
        if isinstance(question, Mapping) and any(field in question for field in _EDITOR_ONLY_FIELDS):
            return REVIEW_SESSION
    return BATCH


def batch_schema_errors(data: object) -> list[str]:
    """Return one message per schema violation of a batch, each with the JSON path of the offending value."""
    errors = sorted(_batch_validator().iter_errors(data), key=lambda error: [str(part) for part in error.path])
    return [f"{json_path(error.path)}: {error.message}" for error in errors]


def normalize_status(value: object) -> str:
    """Map a status, including the legacy Spanish values, to pending, review or ready."""
    text = str(value or "pending")
    return _LEGACY_STATUSES.get(text, text)


def is_correct_fraction(fraction: object) -> bool:
    """A fraction of 100 or more marks the key; anything else is a distractor."""
    try:
        return float(str(fraction)) >= 100
    except ValueError:
        return False


def answer_shape_problems(
    fractions: Iterable[object],
    expected_distractors: int | None,
) -> list[tuple[str, int, int]]:
    """Return (problem, actual, expected) for a question without exactly one key or the expected distractors."""
    fraction_list = list(fractions)
    correct_count = sum(1 for fraction in fraction_list if is_correct_fraction(fraction))
    problems: list[tuple[str, int, int]] = []
    if correct_count != 1:
        problems.append(("correct_count", correct_count, 1))
    distractor_count = len(fraction_list) - correct_count
    if expected_distractors is not None and distractor_count != expected_distractors:
        problems.append(("distractor_count", distractor_count, expected_distractors))
    return problems


def expected_distractors(data: Mapping, question: Mapping) -> int | None:
    """Distractors a question should have: by batch version, or 3 for a ready question in a review session."""
    if artifact_kind(data) == BATCH:
        return BATCH_DISTRACTORS.get(str(data.get("version", "1.0")))
    return READY_DISTRACTORS if normalize_status(question.get("status")) == "ready" else None


def question_label(question: Mapping) -> str:
    """Short human label for messages: the id, or the name when there is no id."""
    return str(question.get("id") or question.get("name") or "?")


def answers_of(question: Mapping) -> Sequence[Mapping]:
    answers = question.get("answers", [])
    return [answer for answer in answers if isinstance(answer, Mapping)] if isinstance(answers, list) else []


@cache
def _batch_validator() -> Draft202012Validator:
    schema_text = resources.files("qb").joinpath("schemas/item-batch.schema.json").read_text(encoding="utf-8")
    return Draft202012Validator(json.loads(schema_text))


def json_path(path: Iterable[object]) -> str:
    """Render a jsonschema error path as $.questions[0].answers[1].fraction."""
    return "$" +"".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in path)
