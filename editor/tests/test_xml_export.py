"""Regression tests for the editor's Moodle XML export, which delegates to qb.export."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ElementTree


EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


from file_io.xml_parser import parse_xml_file  # noqa: E402
from file_io.xml_writer import generate_xml  # noqa: E402
from models.question import Answer, Question, QuestionStatus  # noqa: E402
from qb.export import ExportError  # noqa: E402

SAMPLE_WITH_CATEGORIES = EDITOR_DIR.parent / "samples" / "with_categories.xml"


class XmlExportTests(unittest.TestCase):

    def test_reexported_sample_with_an_ampersand_category_is_well_formed(self) -> None:
        _, questions = parse_xml_file(SAMPLE_WITH_CATEGORIES)

        root = ElementTree.fromstring(generate_xml(questions))

        categories = [element.findtext("category/text") for element in root if element.get("type") == "category"]
        self.assertIn("$course$/top/CSPy/Examen CSPy/Módulos & Paquetes", categories)
        self.assertEqual(sum(1 for element in root if element.get("type") == "multichoice"), len(questions))

    def test_a_ready_question_with_seven_options_is_not_exported(self) -> None:
        answers = [Answer("<p>Clave</p>", "100", "<p>Correcto.</p>")]
        answers += [Answer(f"<p>D{index}</p>", "-50", "<p>Incorrecto.</p>") for index in range(6)]
        question = Question("Q1", "Q1", "<p>Enunciado</p>", "", "$course$/top/X", answers, QuestionStatus.READY)

        with self.assertRaises(ExportError):
            generate_xml([question])


if __name__ == '__main__':
    unittest.main()
