"""Non-blocking diagnostics shown while reviewing; the analysis itself lives in qb.length."""

from __future__ import annotations

from models.question import Question
from qb.html import visible_text as extract_visible_text
from qb.length import LengthAnalysis as QuestionDiagnostics, analyze_answer_lengths

__all__ = ["QuestionDiagnostics", "analyze_question", "extract_visible_text"]


def analyze_question(question: Question) -> QuestionDiagnostics:
    """Compute the answer-length diagnostics of one question."""
    return analyze_answer_lengths([(answer.text, answer.is_correct) for answer in question.answers])
