"""
XML Parser for Moodle Quiz format.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from models.question import Question, Answer, Category, QuestionStatus


def parse_xml_file(xml_path: Path) -> tuple[list[Category], list[Question]]:
    """Parse a Moodle XML file and return categories and questions."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    categories: list[Category] = []
    questions: list[Question] = []
    current_category_path = ""
    source_file = xml_path.name

    for q_elem in root.findall("question"):
        q_type = q_elem.get("type")

        if q_type == "category":
            cat_elem = q_elem.find("category/text")
            info_elem = q_elem.find("info/text")
            cat_path = cat_elem.text if cat_elem is not None and cat_elem.text else ""
            cat_info = info_elem.text if info_elem is not None and info_elem.text else ""
            current_category_path = cat_path
            categories.append(Category(path=cat_path, info=cat_info))

        elif q_type == "multichoice":
            name_elem = q_elem.find("name/text")
            qtext_elem = q_elem.find("questiontext/text")
            feedback_elem = q_elem.find("generalfeedback/text")
            question_name = name_elem.text if name_elem is not None and name_elem.text else "Untitled"

            answers: list[Answer] = []
            for ans_elem in q_elem.findall("answer"):
                ans_text_elem = ans_elem.find("text")
                ans_feedback_elem = ans_elem.find("feedback/text")
                answers.append(Answer(
                    text=ans_text_elem.text if ans_text_elem is not None and ans_text_elem.text else "",
                    fraction=ans_elem.get("fraction", "0"),
                    feedback=ans_feedback_elem.text if ans_feedback_elem is not None and ans_feedback_elem.text else "",
                    format=ans_elem.get("format", "html"),
                ))

            single_elem = q_elem.find("single")
            shuffle_elem = q_elem.find("shuffleanswers")
            numbering_elem = q_elem.find("answernumbering")
            grade_elem = q_elem.find("defaultgrade")
            penalty_elem = q_elem.find("penalty")

            question = Question(
                id=Question.generate_id(),
                name=question_name,
                question_text=qtext_elem.text if qtext_elem is not None and qtext_elem.text else "",
                general_feedback=feedback_elem.text if feedback_elem is not None and feedback_elem.text else "",
                category_path=current_category_path,
                answers=answers,
                status=QuestionStatus.PENDIENTE,
                default_grade=grade_elem.text if grade_elem is not None and grade_elem.text else "1.0000000",
                penalty=penalty_elem.text if penalty_elem is not None and penalty_elem.text else "0.0000000",
                single=single_elem.text if single_elem is not None and single_elem.text else "true",
                shuffle_answers=shuffle_elem.text if shuffle_elem is not None and shuffle_elem.text else "true",
                answer_numbering=numbering_elem.text if numbering_elem is not None and numbering_elem.text else "abc",
                source_file=source_file,
                origin_kind="xml_import",
                origin_path=str(xml_path),
                origin_question_id=f"{current_category_path}::{question_name}",
            )
            questions.append(question)

    return categories, questions


def parse_multiple_files(xml_paths: list[Path]) -> tuple[list[Category], list[Question]]:
    """Parse multiple XML files and merge results."""
    all_categories: list[Category] = []
    all_questions: list[Question] = []
    seen_category_paths: set[str] = set()

    for path in xml_paths:
        try:
            categories, questions = parse_xml_file(path)
            for cat in categories:
                if cat.path not in seen_category_paths:
                    all_categories.append(cat)
                    seen_category_paths.add(cat.path)
            all_questions.extend(questions)
        except Exception as e:
            print(f"Skipping {path.name}: {e}")
            continue

    return all_categories, all_questions
