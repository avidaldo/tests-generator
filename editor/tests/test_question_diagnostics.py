"""Unit tests for reviewed-question diagnostics."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


from models.question import Answer, Question  # noqa: E402
from models.question_diagnostics import analyze_question, extract_visible_text  # noqa: E402


class QuestionDiagnosticsTests(unittest.TestCase):

    def test_extract_visible_text_ignores_rich_text_wrapper(self) -> None:
        html_text = (
            '<!DOCTYPE HTML><html><head><style>p { color: red; }</style></head>'
            '<body><p>Alpha</p><p>Beta <b>Gamma</b></p></body></html>'
        )

        self.assertEqual(extract_visible_text(html_text), 'Alpha Beta Gamma')

    def test_flags_uniquely_long_correct_answer(self) -> None:
        question = _make_question([
            Answer('<p>Short distractor idea.</p>', '-50'),
            Answer('<p>Another short distractor idea.</p>', '-50'),
            Answer('<p>Third short distractor idea.</p>', '-50'),
            Answer(
                '<p>This correct option adds several more qualifying details so the rationale is much more elaborate than any distractor here.</p>',
                '100',
            ),
        ])

        diagnostics = analyze_question(question)

        self.assertTrue(diagnostics.has_warnings)
        self.assertIn('substantially longer', diagnostics.warnings[0])

    def test_does_not_flag_balanced_reviewed_four_answer_question(self) -> None:
        question = _make_question([
            Answer('<p>Describe a plausible but incomplete explanation of the model behavior.</p>', '-50'),
            Answer('<p>Describe a second plausible but incomplete explanation of the model behavior.</p>', '-50'),
            Answer('<p>Describe a third plausible but incomplete explanation of the model behavior.</p>', '-50'),
            Answer('<p>Describe the accurate explanation of the model behavior with similar detail.</p>', '100'),
        ])

        diagnostics = analyze_question(question)

        self.assertFalse(diagnostics.has_warnings)
        self.assertEqual(len(diagnostics.answer_metrics), 4)

    def test_flags_uniquely_short_correct_answer(self) -> None:
        question = _make_question([
            Answer('<p>A detailed distractor that sounds convincing because it includes extra procedural qualifiers and context.</p>', '-50'),
            Answer('<p>Another detailed distractor that sounds convincing because it includes extra procedural qualifiers and context.</p>', '-50'),
            Answer('<p>Third detailed distractor that sounds convincing because it includes extra procedural qualifiers and context.</p>', '-50'),
            Answer('<p>The key idea.</p>', '100'),
        ])

        diagnostics = analyze_question(question)

        self.assertTrue(diagnostics.has_warnings)
        self.assertIn('substantially shorter', diagnostics.warnings[0])

    def test_does_not_flag_char_only_gap_when_word_counts_are_close(self) -> None:
        question = _make_question([
            Answer('<p>Short distractor with broad but plausible reasoning for the observed failure case.</p>', '-50'),
            Answer('<p>Short distractor with concise but plausible reasoning for the observed failure case.</p>', '-50'),
            Answer('<p>Short distractor with compact but plausible reasoning for the observed failure case.</p>', '-50'),
            Answer('<p>Characteristically elongated terminology preserves a similar word count while adding technical specificity.</p>', '100'),
        ])

        diagnostics = analyze_question(question)

        self.assertFalse(diagnostics.has_warnings)


def _make_question(answers: list[Answer]) -> Question:
    return Question(
        id='TST_Q001',
        name='Q001: Test question',
        question_text='<p>Question stem</p>',
        general_feedback='<p>Feedback</p>',
        category_path='$course$/top/Test',
        answers=answers,
    )


if __name__ == '__main__':
    unittest.main()