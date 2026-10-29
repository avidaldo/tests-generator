"""Moodle XML export: the only writer, used by `qb export` and by the editor."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from xml.sax.saxutils import escape

from qb.html import sanitize
from qb.schema import (
    MOODLE_DEFAULTS,
    READY_DISTRACTORS,
    answer_shape_problems,
    answers_of,
    is_correct_fraction,
    normalize_status,
    question_label,
)


class ExportError(ValueError):
    """Raised when questions can't be exported as they are."""


def cdata(text: str) -> str:
    """Wrap text in a CDATA section, splitting any ']]>' inside so it can't end the section early."""
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def select_questions(
    questions: Iterable[Mapping],
    statuses: Iterable[str] | None = None,
    easy_only: bool = False,
) -> list[Mapping]:
    """Keep the questions with one of the statuses (all when None) and, with easy_only, those marked easy."""
    wanted = None if statuses is None else {normalize_status(status) for status in statuses}
    selected = [
        question for question in questions
        if wanted is None or normalize_status(question.get("status")) in wanted
    ]
    if easy_only:
        selected = [question for question in selected if question.get("is_easy") is True]
    return selected


def moodle_xml(
    questions: Sequence[Mapping],
    *,
    wrong_fraction: str | None = None,
    sanitize_html: bool = True,
) -> str:
    """Return Moodle XML for the questions.

    Questions are grouped by category in order of first appearance. Questions without a category come first,
    before any category element, so Moodle puts them in the category chosen in its import form instead of the
    category of the question before them. A ready question needs 1 key and 3 distractors; any other question,
    exactly 1 key. wrong_fraction, when given, replaces the fraction of every distractor.
    Raises ExportError listing every question that breaks those rules.
    """
    problems = [
        f"{question_label(question)}: {problem} is {actual}, expected {expected}"
        for question in questions
        for problem, actual, expected in answer_shape_problems(
            [answer.get("fraction") for answer in answers_of(question)],
            READY_DISTRACTORS if normalize_status(question.get("status")) == "ready" else None,
        )
    ]
    if problems:
        raise ExportError("Cannot export these questions:\n" + "\n".join(problems))

    clean: Callable[[str], str] = sanitize if sanitize_html else str
    questions_by_category: dict[str, list[Mapping]] = {}
    for question in questions:
        questions_by_category.setdefault(str(question.get("category_path") or ""), []).append(question)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    for category_path, category_questions in sorted(questions_by_category.items(), key=lambda item: item[0] != ""):
        if category_path:
            lines.extend([
                '  <question type="category">',
                "    <category>",
                f"      <text>{escape(category_path)}</text>",
                "    </category>",
                '    <info format="html"><text></text></info>',
                "    <idnumber></idnumber>",
                "  </question>",
            ])
        for question in category_questions:
            lines.extend(_question_lines(question, clean, wrong_fraction))
    lines.append("</quiz>")
    return "\n".join(lines) + "\n"


def _question_lines(question: Mapping, clean: Callable[[str], str], wrong_fraction: str | None) -> list[str]:
    def html_field(key: str) -> str:
        return cdata(clean(str(question.get(key, MOODLE_DEFAULTS.get(key, "")) or "")))

    lines = [
        '  <question type="multichoice">',
        f"    <name><text>{escape(str(question.get('name') or question_label(question)))}</text></name>",
        f'    <questiontext format="html"><text>{html_field("question_text")}</text></questiontext>',
        f'    <generalfeedback format="html"><text>{html_field("general_feedback")}</text></generalfeedback>',
        f"    <defaultgrade>{_setting(question, 'default_grade')}</defaultgrade>",
        f"    <penalty>{_setting(question, 'penalty')}</penalty>",
        "    <hidden>0</hidden>",
        "    <idnumber></idnumber>",
        f"    <single>{_setting(question, 'single')}</single>",
        f"    <shuffleanswers>{_setting(question, 'shuffle_answers')}</shuffleanswers>",
        f"    <answernumbering>{_setting(question, 'answer_numbering')}</answernumbering>",
        "    <showstandardinstruction>0</showstandardinstruction>",
        f'    <correctfeedback format="html"><text>{html_field("correct_feedback")}</text></correctfeedback>',
        '    <partiallycorrectfeedback format="html">'
        f'<text>{html_field("partially_correct_feedback")}</text></partiallycorrectfeedback>',
        f'    <incorrectfeedback format="html"><text>{html_field("incorrect_feedback")}</text></incorrectfeedback>',
        "    <shownumcorrect/>",
    ]
    for answer in answers_of(question):
        fraction = str(answer.get("fraction"))
        if wrong_fraction is not None and not is_correct_fraction(fraction):
            fraction = wrong_fraction
        lines.extend([
            f'    <answer fraction="{escape(fraction, {chr(34): "&quot;"})}" format="html">',
            f"      <text>{cdata(clean(str(answer.get('text') or '')))}</text>",
            f'      <feedback format="html"><text>{cdata(clean(str(answer.get("feedback") or "")))}</text></feedback>',
            "    </answer>",
        ])
    lines.append("  </question>")
    return lines


def _setting(question: Mapping, key: str) -> str:
    value = question.get(key, MOODLE_DEFAULTS[key])
    if isinstance(value, bool):
        value = "true" if value else "false"
    return escape(str(value))
