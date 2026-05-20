"""Unit tests for editor session replacement and dirty-state flow."""

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
from PyQt6.QtWidgets import QApplication, QMessageBox  # noqa: E402

from models.question import Answer, Question  # noqa: E402
from views.main_window import MainWindow  # noqa: E402


class MainWindowSessionFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        timer_patcher = patch.object(QTimer, 'singleShot', new=lambda *args, **kwargs: None)
        self.addCleanup(timer_patcher.stop)
        timer_patcher.start()

        self.window = MainWindow()
        self.addCleanup(self._dispose_window)

    def test_confirm_session_replacement_skips_prompt_for_clean_loaded_session(self) -> None:
        self.window._replace_loaded_session([_make_question()], Path('session.json'), 'Loaded clean')

        with patch.object(QMessageBox, 'question', side_effect=AssertionError('Prompt should not appear')):
            self.assertTrue(self.window._confirm_session_replacement('Title', 'Prompt'))

        self.assertFalse(self.window._session_dirty)
        self.assertFalse(self.window.isWindowModified())

    def test_confirm_session_replacement_prompts_for_dirty_session(self) -> None:
        self.window._replace_loaded_session([_make_question()], Path('session.json'), 'Loaded clean')
        self.window._mark_session_dirty()

        with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Discard) as question_mock:
            self.assertTrue(self.window._confirm_session_replacement('Title', 'Prompt'))

        question_mock.assert_called_once()
        self.assertTrue(self.window._session_dirty)
        self.assertTrue(self.window.isWindowModified())

    def test_replace_loaded_session_can_mark_restored_autosave_dirty(self) -> None:
        self.window._replace_loaded_session(
            [_make_question()],
            Path('session.json'),
            'Restored autosave',
            is_dirty=True,
        )

        self.assertTrue(self.window._session_dirty)
        self.assertTrue(self.window.isWindowModified())

    def _dispose_window(self) -> None:
        self.window.deleteLater()
        self._app.processEvents()


def _make_question() -> Question:
    return Question(
        id='TST_Q001',
        name='Q001: Test question',
        question_text='<p>Question stem</p>',
        general_feedback='<p>Feedback</p>',
        category_path='$course$/top/Test',
        answers=[
            Answer(text='<p>Correct answer</p>', fraction='100', feedback='<p>Correct.</p>'),
            Answer(text='<p>Distractor</p>', fraction='-50', feedback='<p>Wrong.</p>'),
        ],
    )


if __name__ == '__main__':
    unittest.main()