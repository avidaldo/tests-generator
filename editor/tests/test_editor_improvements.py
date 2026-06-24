"""Unit tests for the new editor improvements: correct-reviewed checkboxes, purging, formatting validation, and demotion."""

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

from PyQt6.QtCore import QTimer, QModelIndex
from PyQt6.QtGui import QUndoStack
from PyQt6.QtWidgets import QApplication

from models.question import Answer, Question, QuestionStatus
from models.quiz_model import QuizModel
from models.undo_commands import PurgeAnswersCommand
from file_io.state_io import _serialize_question, _deserialize_question
from views.question_detail import QuestionDetailPanel
from views.main_window import MainWindow


class EditorImprovementsTests(unittest.TestCase):
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

    def _dispose_panel(self) -> None:
        self.panel.deleteLater()
        self._app.processEvents()

    def test_answer_correct_reviewed_serialization_deserialization(self) -> None:
        # 1. Verify correct_reviewed property of Answer models.
        # Test default value
        ans1 = Answer(text="Ans 1", fraction="-33.33333")
        self.assertFalse(ans1.correct_reviewed)

        # Test setting true
        ans2 = Answer(text="Ans 2", fraction="-33.33333", correct_reviewed=True)
        self.assertTrue(ans2.correct_reviewed)

        # Create a mock Question with these answers
        q = Question(
            id="TST_Q001",
            name="Test",
            question_text="Stem",
            general_feedback="Feedback",
            category_path="Cat",
            answers=[ans1, ans2],
        )

        # Serialize
        serialized = _serialize_question(q)
        ans_data = serialized["answers"]
        self.assertEqual(len(ans_data), 2)
        self.assertFalse(ans_data[0]["correct_reviewed"])
        self.assertTrue(ans_data[1]["correct_reviewed"])

        # Deserialize
        deserialized = _deserialize_question(serialized, Path("dummy.json"))
        self.assertEqual(len(deserialized.answers), 2)
        self.assertFalse(deserialized.answers[0].correct_reviewed)
        self.assertTrue(deserialized.answers[1].correct_reviewed)

    def test_purge_answers_command(self) -> None:
        # 2. Undo/redo behavior of PurgeAnswersCommand.
        ans_correct = Answer(text="Correct", fraction="100")
        ans_reviewed = Answer(text="Reviewed", fraction="-50", correct_reviewed=True)
        ans_not_reviewed = Answer(text="Not Reviewed", fraction="-50", correct_reviewed=False)

        q = Question(
            id="TST_Q001",
            name="Test",
            question_text="Stem",
            general_feedback="",
            category_path="Cat",
            answers=[ans_correct, ans_reviewed, ans_not_reviewed],
        )
        self.model.add_questions([q])

        cmd = PurgeAnswersCommand(self.model, q)
        
        # Redo (Purge)
        cmd.redo()
        self.assertEqual(len(q.answers), 2)
        self.assertIn(ans_correct, q.answers)
        self.assertIn(ans_reviewed, q.answers)
        self.assertNotIn(ans_not_reviewed, q.answers)

        # Undo
        cmd.undo()
        self.assertEqual(len(q.answers), 3)
        self.assertIn(ans_not_reviewed, q.answers)

        # Redo again
        cmd.redo()
        self.assertEqual(len(q.answers), 2)
        self.assertNotIn(ans_not_reviewed, q.answers)

    def test_validate_format_logic(self) -> None:
        # 3. Question format validation helper.
        # Exactly 1 correct + 3 wrong -> valid (empty list of errors)
        q_valid = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat",
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        errors = self.panel._validate_format(q_valid)
        self.assertEqual(len(errors), 0)

        # 0 correct -> invalid
        q_no_correct = Question(
            id="Q2", name="Q2", question_text="Stem", general_feedback="", category_path="Cat",
            answers=[
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        errors = self.panel._validate_format(q_no_correct)
        self.assertTrue(any("correcta" in e for e in errors))

        # 2 correct -> invalid
        q_two_correct = Question(
            id="Q3", name="Q3", question_text="Stem", general_feedback="", category_path="Cat",
            answers=[
                Answer(text="C1", fraction="100"),
                Answer(text="C2", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        errors = self.panel._validate_format(q_two_correct)
        self.assertTrue(any("correcta" in e for e in errors))

        # 1 correct + 2 wrong -> invalid
        q_two_wrong = Question(
            id="Q4", name="Q4", question_text="Stem", general_feedback="", category_path="Cat",
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
            ]
        )
        errors = self.panel._validate_format(q_two_wrong)
        self.assertTrue(any("distractores" in e for e in errors))

    def test_automatic_demotion_on_delete_answer(self) -> None:
        # 4. Deletion/purge demotion macro.
        q = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat",
            status=QuestionStatus.READY,
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        self.model.add_questions([q])
        self.panel.set_question(q)

        # Delete one wrong answer.
        # This reduces distractors to 2, which makes the format invalid.
        # It should demote status to PENDIENTE automatically.
        self.panel._on_delete_answer(3)

        self.assertEqual(len(q.answers), 3)
        self.assertEqual(q.status, QuestionStatus.PENDING)

        # Verify undo restores both the deleted answer and the LISTA status.
        self.undo_stack.undo()
        self.assertEqual(len(q.answers), 4)
        self.assertEqual(q.status, QuestionStatus.READY)

    def test_set_status_lista_validation_fails(self) -> None:
        # Setting status to READY on an invalid question should show a transient inline
        # hint (not a blocking dialog) and remain at the previous status.
        q = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat",
            status=QuestionStatus.PENDING,
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
            ]
        )
        self.model.add_questions([q])
        self.panel.set_question(q)

        self.panel._set_status(QuestionStatus.READY)

        # The inline hint is populated and not explicitly hidden (parent isn't shown
        # in headless tests, so isVisible() would be False; isHidden() is the right check).
        self.assertFalse(self.panel._format_hint_label.isHidden())
        self.assertIn("LISTA", self.panel._format_hint_label.text())
        self.assertEqual(q.status, QuestionStatus.PENDING)

    def test_auto_navigation_on_status_lista(self) -> None:
        # Create a MainWindow instance
        window = MainWindow()
        self.addCleanup(self._dispose_window, window)

        # Create three questions
        q1 = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat",
            status=QuestionStatus.PENDING,
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        q2 = Question(
            id="Q2", name="Q2", question_text="Stem", general_feedback="", category_path="Cat",
            status=QuestionStatus.PENDING,
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        q3 = Question(
            id="Q3", name="Q3", question_text="Stem", general_feedback="", category_path="Cat",
            status=QuestionStatus.PENDING,
            answers=[
                Answer(text="Correct", fraction="100"),
                Answer(text="W1", fraction="-33.33333"),
                Answer(text="W2", fraction="-33.33333"),
                Answer(text="W3", fraction="-33.33333"),
            ]
        )
        
        # Clear model and add our questions
        window._model.clear()
        window._model.add_questions([q1, q2, q3])
        window._refresh_category_tree()

        # Set filter to PENDIENTE so that changing q1 to LISTA will filter it out
        window._set_status_filter(QuestionStatus.PENDING)

        # Select Q1 in the list view
        idx1 = window._proxy_model.index(0, 0)
        window._question_list.setCurrentIndex(idx1)
        self.assertEqual(window._detail_panel._current_question, q1)

        # We want QTimer.singleShot to execute its callback immediately during this status change
        def immediate_single_shot(ms, callback):
            callback()

        with patch.object(QTimer, 'singleShot', side_effect=immediate_single_shot):
            # Mark Q1 as LISTA
            window._detail_panel._set_status(QuestionStatus.READY)

        # Q1 should now be LISTA and filtered out, and the selected question in details panel should be Q2!
        self.assertEqual(q1.status, QuestionStatus.READY)
        self.assertEqual(window._detail_panel._current_question, q2)

    def test_question_review_notes_persistence(self) -> None:
        q = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat",
            review_notes="needs clarification"
        )
        self.model.add_questions([q])
        
        serialized = _serialize_question(q)
        self.assertEqual(serialized["review_notes"], "needs clarification")
        
        deserialized = _deserialize_question(serialized, Path("dummy.json"))
        self.assertEqual(deserialized.review_notes, "needs clarification")

    def test_session_notes_persistence(self) -> None:
        from file_io.state_io import save_state, load_review_session
        import tempfile
        
        q = Question(
            id="Q1", name="Q1", question_text="Stem", general_feedback="", category_path="Cat"
        )
        questions = [q]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "session.json"
            save_state(questions, filepath, notes="some general session notes")
            
            session = load_review_session(filepath)
            self.assertEqual(session.notes, "some general session notes")
            self.assertEqual(len(session.questions), 1)

    def test_mainwindow_session_notes(self) -> None:
        window = MainWindow()
        self.addCleanup(self._dispose_window, window)
        
        self.assertEqual(window._session_notes, "")
        
        window._session_notes = "Important session issues"
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_session_notes.json"
            window._save_review_session_to_path(filepath)
            
            window._session_notes = "other"
            window._replace_loaded_session([], None, "Cleared")
            self.assertEqual(window._session_notes, "")
            
            from file_io.state_io import load_review_session
            session = load_review_session(filepath)
            window._replace_loaded_session(session.questions, filepath, "Loaded", notes=session.notes)
            self.assertEqual(window._session_notes, "Important session issues")

    def test_source_ref_editing_undo_redo_and_refresh(self) -> None:
        q = Question(
            id="Q_SRC", name="Q_SRC", question_text="Stem", general_feedback="", category_path="Cat",
            source_ref="OLD-REF", origin_kind="stage3_batch"
        )
        self.model.add_questions([q])
        self.panel.set_question(q)

        # Assert initially populated
        self.assertEqual(self.panel._source_ref_edit.text(), "OLD-REF")
        self.assertEqual(self.panel._source_label.text(), "📄 Stage 3 | OLD-REF")

        # Edit the source_ref field
        self.panel._source_ref_edit.setText("  NEW-REF  ")
        self.panel._on_source_ref_changed()

        # Assert question is updated
        self.assertEqual(q.source_ref, "NEW-REF")
        self.assertEqual(self.panel._source_label.text(), "📄 Stage 3 | NEW-REF")

        # Undo modification
        self.undo_stack.undo()
        self.assertEqual(q.source_ref, "OLD-REF")
        self.assertEqual(self.panel._source_ref_edit.text(), "OLD-REF")
        self.assertEqual(self.panel._source_label.text(), "📄 Stage 3 | OLD-REF")

        # Redo modification
        self.undo_stack.redo()
        self.assertEqual(q.source_ref, "NEW-REF")
        self.assertEqual(self.panel._source_ref_edit.text(), "NEW-REF")
        self.assertEqual(self.panel._source_label.text(), "📄 Stage 3 | NEW-REF")

    def _dispose_window(self, window: MainWindow) -> None:
        window.deleteLater()
        self._app.processEvents()


if __name__ == '__main__':
    unittest.main()
