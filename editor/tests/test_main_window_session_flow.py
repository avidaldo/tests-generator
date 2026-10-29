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


import tempfile  # noqa: E402

from PyQt6.QtCore import QSettings, QTimer  # noqa: E402
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox  # noqa: E402

from file_io.state_io import load_review_session, save_state  # noqa: E402
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

        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self.window = MainWindow(autosave_file=Path(self._temp_dir.name) / "autosave.json")
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

    def test_autosave_writes_through_to_session_file_and_clears_dirty(self) -> None:
        import json
        import tempfile

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        session_path = Path(temp_dir.name) / "session.json"

        self.window._replace_loaded_session([_make_question()], session_path, 'Loaded')
        self.window._mark_session_dirty()
        self.assertTrue(self.window._session_dirty)

        self.window._do_autosave()

        self.assertTrue(session_path.exists())
        data = json.loads(session_path.read_text())
        self.assertEqual(len(data["questions"]), 1)
        self.assertFalse(self.window._session_dirty)

    def test_recent_sessions_mru_dedups_and_orders_most_recent_first(self) -> None:
        import tempfile
        from PyQt6.QtCore import QSettings

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        # Isolate QSettings to a temp ini file so the test does not touch real settings.
        self.window._settings = QSettings(str(Path(temp_dir.name) / "s.ini"), QSettings.Format.IniFormat)

        a = Path(temp_dir.name) / "a.json"
        b = Path(temp_dir.name) / "b.json"
        self.window._add_recent_session(a)
        self.window._add_recent_session(b)
        self.window._add_recent_session(a)  # re-adding moves it to the front

        self.assertEqual(self.window._recent_sessions(), [str(a), str(b)])

    def test_replace_loaded_session_can_mark_restored_autosave_dirty(self) -> None:
        self.window._replace_loaded_session(
            [_make_question()],
            Path('session.json'),
            'Restored autosave',
            is_dirty=True,
        )

        self.assertTrue(self.window._session_dirty)
        self.assertTrue(self.window.isWindowModified())

    def test_restored_autosave_is_not_attached_to_the_last_saved_session(self) -> None:
        temp_path = Path(self._temp_dir.name)
        saved_session = temp_path / "saved.json"
        save_state([_make_question('SAVED_Q001')], saved_session)
        save_state([_make_question('UNSAVED_Q001')], self.window._autosave_file)
        os.utime(saved_session, (1, 1))  # the backup must be the newest file to be offered
        self.window._settings = QSettings(str(temp_path / "s.ini"), QSettings.Format.IniFormat)
        self.window._settings.setValue("last_state_file", str(saved_session))

        with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Yes):
            self.window._auto_load_last_state()
        self.window._do_autosave()  # what the debounce timer does after the next edit

        self.assertIsNone(self.window._current_state_file)
        self.assertTrue(self.window._session_dirty)
        saved_ids = [question.id for question in load_review_session(saved_session).questions]
        self.assertEqual(saved_ids, ['SAVED_Q001'])

    def test_loading_a_session_does_not_schedule_a_rewrite_of_its_file(self) -> None:
        session_path = Path(self._temp_dir.name) / "session.json"
        save_state([_make_question()], session_path)

        self.window._replace_loaded_session(load_review_session(session_path).questions, session_path, 'Loaded')

        self.assertFalse(self.window._autosave_timer.isActive())

    def test_unsaved_session_autosaves_to_the_injected_backup_path(self) -> None:
        self.window._replace_loaded_session([_make_question()], None, 'Imported', is_dirty=True)

        self.window._do_autosave()

        self.assertTrue(self.window._autosave_file.exists())
        self.assertEqual(self.window._autosave_file.parent, Path(self._temp_dir.name))

    def test_xml_import_names_unreadable_files_and_keeps_the_readable_ones(self) -> None:
        readable_xml = Path(self._temp_dir.name) / "readable.xml"
        broken_xml = Path(self._temp_dir.name) / "broken.xml"
        readable_xml.write_text(_ONE_QUESTION_XML.replace("{cdata_open}", "<![CDATA["), encoding="utf-8")
        broken_xml.write_text(_ONE_QUESTION_XML.replace("{cdata_open}", "<![CDATA>"), encoding="utf-8")
        chosen_files = ([str(readable_xml), str(broken_xml)], "XML Files (*.xml)")

        with patch.object(QFileDialog, 'getOpenFileNames', return_value=chosen_files), \
                patch.object(QMessageBox, 'warning') as warning_mock:
            self.window._import_legacy_xml_files()

        self.assertEqual([question.name for question in self.window._model.questions], ['Q1'])
        warning_mock.assert_called_once()
        self.assertIn("broken.xml: not well-formed", warning_mock.call_args.args[2])

    def _dispose_window(self) -> None:
        self.window.deleteLater()
        self._app.processEvents()


def _make_question(question_id: str = 'TST_Q001') -> Question:
    return Question(
        id=question_id,
        name='Q001: Test question',
        question_text='<p>Question stem</p>',
        general_feedback='<p>Feedback</p>',
        category_path='$course$/top/Test',
        answers=[
            Answer(text='<p>Correct answer</p>', fraction='100', feedback='<p>Correct.</p>'),
            Answer(text='<p>Distractor</p>', fraction='-50', feedback='<p>Wrong.</p>'),
        ],
    )


_ONE_QUESTION_XML = """<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <question type="multichoice">
    <name><text>Q1</text></name>
    <questiontext format="html"><text>{cdata_open}<p>Stem</p>]]></text></questiontext>
    <answer fraction="100" format="html"><text>Key</text><feedback><text>Correct.</text></feedback></answer>
    <answer fraction="-50" format="html"><text>Distractor</text><feedback><text>Wrong.</text></feedback></answer>
  </question>
</quiz>
"""


if __name__ == '__main__':
    unittest.main()