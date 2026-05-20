"""Unit tests for editor JSON artifact loading."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


from file_io.state_io import load_review_session, load_stage3_batch  # noqa: E402
from models.review_session import REVIEW_SESSION_ARTIFACT_TYPE  # noqa: E402


class StateIoArtifactTests(unittest.TestCase):

    def test_load_stage3_batch_accepts_raw_stage3_json(self) -> None:
        stage3_path = self._write_json({
            "version": "1.0",
            "questions": [self._make_question_data()],
        }, "batch-001.json")

        questions = load_stage3_batch(stage3_path)

        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].origin_path, str(stage3_path))

    def test_load_review_session_rejects_raw_stage3_json(self) -> None:
        stage3_path = self._write_json({
            "version": "1.0",
            "questions": [self._make_question_data()],
        }, "batch-001.json")

        with self.assertRaisesRegex(ValueError, "Stage 3 batch JSON"):
            load_review_session(stage3_path)

    def test_load_stage3_batch_rejects_saved_review_session(self) -> None:
        review_session_path = self._write_json({
            "artifact_type": REVIEW_SESSION_ARTIFACT_TYPE,
            "version": "1.0",
            "imported_sources": [],
            "questions": [self._make_question_data()],
        }, "session.json")

        with self.assertRaisesRegex(ValueError, "saved review session JSON"):
            load_stage3_batch(review_session_path)

    def test_load_review_session_accepts_legacy_editor_state(self) -> None:
        legacy_state_path = self._write_json({
            "questions": [
                self._make_question_data(
                    source_file="legacy-export.xml",
                    correct_feedback="<p>Correcto.</p>",
                    partially_correct_feedback="<p>Parcialmente correcto.</p>",
                    incorrect_feedback="<p>Incorrecto.</p>",
                )
            ],
        }, "legacy-session.json")

        review_session = load_review_session(legacy_state_path)

        self.assertEqual(len(review_session.questions), 1)
        self.assertEqual(review_session.questions[0].origin_kind, "legacy_state")

    def _write_json(self, payload: dict, filename: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        file_path = Path(temp_dir.name) / filename
        file_path.write_text(json.dumps(payload), encoding="utf-8")
        return file_path

    def _make_question_data(self, **overrides: str) -> dict:
        question_data = {
            "id": "TST_Q001",
            "name": "Q001: Test question",
            "question_text": "<p>Question stem</p>",
            "general_feedback": "<p>Feedback</p>",
            "category_path": "$course$/top/Test",
            "status": "pendiente",
            "answers": [
                {
                    "text": "<p>Correct answer</p>",
                    "fraction": "100",
                    "feedback": "<p>Correct.</p>",
                    "format": "html",
                },
                {
                    "text": "<p>Distractor</p>",
                    "fraction": "-50",
                    "feedback": "<p>Wrong.</p>",
                    "format": "html",
                },
            ],
        }
        question_data.update(overrides)
        return question_data


if __name__ == '__main__':
    unittest.main()