"""Tests for qb.export and `qb export`: well-formed XML, categories, shape checks, fractions, HTML cleaning."""

import json
from pathlib import Path
import xml.etree.ElementTree as ElementTree

import pytest

from qb.cli import main
from qb.export import ExportError, moodle_xml, select_questions


def _question(name: str, category: str = "$course$/top/Prueba", status: str = "ready", **fields) -> dict:
    question = {
        "id": name,
        "name": name,
        "question_text": "<p>Enunciado</p>",
        "general_feedback": "<p>Explicación</p>",
        "category_path": category,
        "status": status,
        "answers": [
            {"text": "<p>Clave</p>", "fraction": "100", "feedback": "<p>Correcto, porque...</p>"},
            {"text": "<p>D1</p>", "fraction": "-50", "feedback": "<p>Incorrecto, porque...</p>"},
            {"text": "<p>D2</p>", "fraction": "-50", "feedback": "<p>Incorrecto, porque...</p>"},
            {"text": "<p>D3</p>", "fraction": "-50", "feedback": "<p>Incorrecto, porque...</p>"},
        ],
    }
    return question | fields


def test_names_and_categories_are_escaped() -> None:
    root = ElementTree.fromstring(moodle_xml([_question("Módulos & Paquetes", category="$course$/top/A & B")]))

    assert root.find("question[@type='category']/category/text").text == "$course$/top/A & B"
    assert root.find("question[@type='multichoice']/name/text").text == "Módulos & Paquetes"


def test_cdata_survives_a_closing_sequence_in_unsanitized_text() -> None:
    code = "<p><code>a[b[0]]>1</code></p>"  # a raw '>' after ']]' would end a naive CDATA section
    root = ElementTree.fromstring(moodle_xml([_question("Q", question_text=code)], sanitize_html=False))

    assert root.find("question[@type='multichoice']/questiontext/text").text == code


def test_sanitized_text_escapes_the_closing_sequence() -> None:
    root = ElementTree.fromstring(moodle_xml([_question("Q", question_text="<p><code>a[b[0]]>1</code></p>")]))

    assert root.find("question[@type='multichoice']/questiontext/text").text == "<p><code>a[b[0]]&gt;1</code></p>"


def test_uncategorized_questions_come_before_any_category() -> None:
    questions = [_question("Q1", category="$course$/top/A"), _question("Q2", category="")]

    root = ElementTree.fromstring(moodle_xml(questions))

    assert [element.get("type") for element in root] == ["multichoice", "category", "multichoice"]
    assert root[0].find("name/text").text == "Q2"


def test_a_ready_question_needs_one_key_and_three_distractors() -> None:
    seven_options = _question("Q")
    seven_options["answers"] += [dict(seven_options["answers"][1]) for _ in range(3)]

    with pytest.raises(ExportError, match="distractor_count is 6, expected 3"):
        moodle_xml([seven_options])
    moodle_xml([seven_options | {"status": "pending"}])  # a draft may have any number of distractors


def test_wrong_fraction_replaces_only_distractor_fractions() -> None:
    root = ElementTree.fromstring(moodle_xml([_question("Q")], wrong_fraction="-33.33333"))

    assert [answer.get("fraction") for answer in root.iter("answer")] == ["100", "-33.33333", "-33.33333", "-33.33333"]


def test_qt_documents_are_cleaned_before_export() -> None:
    qt_stem = (
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN"><html><head><meta name="qrichtext" content="1" />'
        '<style type="text/css">p { white-space: pre-wrap; }</style></head><body style=" font-size:16pt;">'
        '<p style=" margin-top:0px;">¿Qué devuelve <span style=" font-family:\'monospace\';">len(x)</span>?</p>'
        "</body></html>"
    )

    xml_text = moodle_xml([_question("Q", question_text=qt_stem)])

    assert "qrichtext" not in xml_text and "style=" not in xml_text
    assert "<p>¿Qué devuelve <code>len(x)</code>?</p>" in xml_text


def test_select_questions_by_status_and_easy_flag() -> None:
    questions = [_question("A", status="lista", is_easy=True), _question("B", status="ready"), _question("C", "", "review")]

    assert [q["name"] for q in select_questions(questions, ["ready"])] == ["A", "B"]
    assert [q["name"] for q in select_questions(questions, ["ready"], easy_only=True)] == ["A"]
    assert len(select_questions(questions)) == 3


def test_cli_export_writes_only_ready_questions(tmp_path: Path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({"questions": [_question("A"), _question("B", status="review")]}), encoding="utf-8")

    assert main(["export", str(session), str(tmp_path)]) == 0
    root = ElementTree.parse(tmp_path / "session.xml").getroot()
    assert [name.text for name in root.iter("text") if name.text in {"A", "B"}] == ["A"]


def test_cli_export_fails_when_nothing_matches(tmp_path: Path) -> None:
    session = tmp_path / "session.json"
    session.write_text(json.dumps({"questions": [_question("A", status="pending")]}), encoding="utf-8")

    assert main(["export", str(session), str(tmp_path / "out.xml")]) == 1
    assert not (tmp_path / "out.xml").exists()
