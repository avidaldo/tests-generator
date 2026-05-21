"""Regression tests for duplicate question ids in the detail panel."""

from __future__ import annotations

import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


from PyQt6.QtCore import QTimer  # noqa: E402
from PyQt6.QtGui import QUndoStack  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from models.question import Answer, Question  # noqa: E402
from models.quiz_model import QuizModel  # noqa: E402
from views.question_detail import QuestionDetailPanel  # noqa: E402


class QuestionDetailDuplicateIdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        timer_patcher = patch.object(QTimer, 'singleShot', new=lambda *args, **kwargs: None)
        self.addCleanup(timer_patcher.stop)
        timer_patcher.start()

        self.model = QuizModel()
        self.undo_stack = QUndoStack()
        self.panel = QuestionDetailPanel(self.model, self.undo_stack)
        self.addCleanup(self._dispose_panel)

    def test_delete_answer_targets_selected_question_even_with_duplicate_id(self) -> None:
        first_question = _make_question(
            question_id='DUP_Q001',
            name='Q001: First question',
            answer_count=2,
        )
        second_question = _make_question(
            question_id='DUP_Q001',
            name='Q002: Later question',
            answer_count=3,
        )
        self.model.add_questions([first_question, second_question])

        self.panel.set_question(second_question)
        self.panel._on_delete_answer(2)

        self.assertEqual(len(first_question.answers), 2)
        self.assertEqual(len(second_question.answers), 2)

    def test_toggle_easy_targets_selected_question_even_with_duplicate_id(self) -> None:
        first_question = _make_question(
            question_id='DUP_Q001',
            name='Q001: First question',
            answer_count=2,
        )
        second_question = _make_question(
            question_id='DUP_Q001',
            name='Q002: Later question',
            answer_count=3,
        )
        self.model.add_questions([first_question, second_question])

        self.panel.set_question(second_question)
        self.panel._toggle_easy()

        self.assertFalse(first_question.is_easy)
        self.assertTrue(second_question.is_easy)

    def _dispose_panel(self) -> None:
        self.panel.deleteLater()
        self._app.processEvents()


def _make_question(question_id: str, name: str, answer_count: int) -> Question:
    answers = [
        Answer(
            text=f'<p>Answer {index}</p>',
            fraction='100' if index == 0 else '-50',
            feedback=f'<p>Feedback {index}</p>',
        )
        for index in range(answer_count)
    ]
    return Question(
        id=question_id,
        name=name,
        question_text='<p>Question stem</p>',
        general_feedback='<p>General feedback</p>',
        category_path='$course$/top/Test',
        answers=answers,
    )


if __name__ == '__main__':
    unittest.main()