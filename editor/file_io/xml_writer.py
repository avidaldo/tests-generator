"""Moodle XML export for the editor; the writer itself is qb.export, shared with `qb export`."""

from collections.abc import Sequence

from file_io.state_io import _serialize_question
from models.question import Question
from qb.export import moodle_xml


def generate_xml(questions: Sequence[Question]) -> str:
    """Return Moodle XML for the questions; raises qb.export.ExportError for a question with the wrong shape."""
    return moodle_xml([_serialize_question(question) for question in questions])
