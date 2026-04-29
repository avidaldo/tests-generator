"""
State I/O - Save and load editor state as JSON.
"""

import json
from pathlib import Path
from dataclasses import asdict

from models.question import Question, Answer, QuestionStatus


def save_state(questions: list[Question], filepath: Path) -> None:
    """Save the current state to a JSON file."""
    data = {
        "version": "1.0",
        "questions": []
    }

    for q in questions:
        q_data = {
            "id": q.id,
            "name": q.name,
            "question_text": q.question_text,
            "general_feedback": q.general_feedback,
            "category_path": q.category_path,
            "status": q.status.value,
            "default_grade": q.default_grade,
            "penalty": q.penalty,
            "single": q.single,
            "shuffle_answers": q.shuffle_answers,
            "answer_numbering": q.answer_numbering,
            "correct_feedback": q.correct_feedback,
            "partially_correct_feedback": q.partially_correct_feedback,
            "incorrect_feedback": q.incorrect_feedback,
            "source_file": q.source_file,
            "source_ref": q.source_file,  # alias: concept-ID reference used by newer prompt versions
            "is_easy": q.is_easy,
            "answers": [
                {
                    "text": a.text,
                    "fraction": a.fraction,
                    "feedback": a.feedback,
                    "format": a.format,
                }
                for a in q.answers
            ]
        }
        data["questions"].append(q_data)

    filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_state(filepath: Path) -> list[Question]:
    """Load state from a JSON file."""
    data = json.loads(filepath.read_text(encoding="utf-8"))

    questions = []
    for q_data in data.get("questions", []):
        answers = [
            Answer(
                text=a["text"],
                fraction=a["fraction"],
                feedback=a.get("feedback", ""),
                format=a.get("format", "html"),
            )
            for a in q_data.get("answers", [])
        ]

        # Map status string to enum
        status_str = q_data.get("status", "pendiente")
        try:
            status = QuestionStatus(status_str)
        except ValueError:
            status = QuestionStatus.PENDIENTE

        question = Question(
            id=q_data["id"],
            name=q_data["name"],
            question_text=q_data["question_text"],
            general_feedback=q_data.get("general_feedback", ""),
            category_path=q_data.get("category_path", ""),
            answers=answers,
            status=status,
            default_grade=q_data.get("default_grade", "1.0000000"),
            penalty=q_data.get("penalty", "0.0000000"),  # adaptive-mode field; 0 for standard single-attempt exams
            single=q_data.get("single", "true"),
            shuffle_answers=q_data.get("shuffle_answers", "true"),
            answer_numbering=q_data.get("answer_numbering", "abc"),
            correct_feedback=q_data.get("correct_feedback", "<p>Correcto.</p>"),
            partially_correct_feedback=q_data.get("partially_correct_feedback", "<p>Parcialmente correcto.</p>"),
            incorrect_feedback=q_data.get("incorrect_feedback", "<p>Incorrecto.</p>"),
            source_file=q_data.get("source_ref", q_data.get("source_file", "")),  # prefer source_ref (concept IDs) over legacy source_file
            is_easy=bool(q_data.get("is_easy", False)),
        )
        questions.append(question)

    return questions
