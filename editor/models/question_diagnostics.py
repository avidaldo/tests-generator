"""Derived diagnostics for reviewed questions."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import re
from statistics import median

from models.question import Question


_WORD_PATTERN = re.compile(r"\w+", re.UNICODE)
_WHITESPACE_PATTERN = re.compile(r"\s+")
_BLOCK_TAGS = {
    "br",
    "div",
    "li",
    "p",
    "tr",
    "td",
    "th",
    "hr",
    "section",
    "article",
}
_IGNORED_TAGS = {"head", "script", "style", "title"}

_LONG_RATIO_THRESHOLD = 1.35
_SHORT_RATIO_THRESHOLD = 1 / _LONG_RATIO_THRESHOLD
_MIN_WORD_DELTA = 4
_MIN_CHAR_DELTA = 24
_SHORT_TEXT_WORD_FALLBACK_LIMIT = 6


class _VisibleTextExtractor(HTMLParser):
    """Extract visible text while ignoring rich-text boilerplate."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        lowered_tag = tag.lower()
        if lowered_tag in _IGNORED_TAGS:
            self._ignored_depth += 1
            return
        if lowered_tag in _BLOCK_TAGS:
            self._chunks.append(" ")

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        lowered_tag = tag.lower()
        if lowered_tag in _IGNORED_TAGS and self._ignored_depth > 0:
            self._ignored_depth -= 1
            return
        if lowered_tag in _BLOCK_TAGS:
            self._chunks.append(" ")

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._ignored_depth == 0 and data:
            self._chunks.append(data)

    def get_text(self) -> str:
        return "".join(self._chunks)


@dataclass(frozen=True)
class AnswerLengthMetrics:
    """Visible-text metrics for one answer option."""

    index: int
    is_correct: bool
    visible_text: str
    word_count: int
    char_count: int


@dataclass(frozen=True)
class QuestionDiagnostics:
    """Derived warning surface for one question."""

    warnings: tuple[str, ...]
    answer_metrics: tuple[AnswerLengthMetrics, ...]
    correct_answer_index: int | None
    correct_word_count: int
    distractor_median_word_count: float
    correct_char_count: int
    distractor_median_char_count: float

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)


def extract_visible_text(html_text: str) -> str:
    """Return normalized visible text from a rich-text HTML string."""
    if not html_text:
        return ""

    extractor = _VisibleTextExtractor()
    extractor.feed(html_text)
    extractor.close()
    return _WHITESPACE_PATTERN.sub(" ", extractor.get_text()).strip()


def analyze_question(question: Question) -> QuestionDiagnostics:
    """Compute non-blocking diagnostics for a reviewed question."""
    answer_metrics = tuple(_build_answer_metrics(question))
    correct_metrics = [metrics for metrics in answer_metrics if metrics.is_correct]
    distractor_metrics = [metrics for metrics in answer_metrics if not metrics.is_correct]

    if len(correct_metrics) != 1 or not distractor_metrics:
        return QuestionDiagnostics(
            warnings=(),
            answer_metrics=answer_metrics,
            correct_answer_index=correct_metrics[0].index if len(correct_metrics) == 1 else None,
            correct_word_count=correct_metrics[0].word_count if len(correct_metrics) == 1 else 0,
            distractor_median_word_count=0,
            correct_char_count=correct_metrics[0].char_count if len(correct_metrics) == 1 else 0,
            distractor_median_char_count=0,
        )

    correct_answer = correct_metrics[0]
    distractor_median_word_count = float(median(metrics.word_count for metrics in distractor_metrics))
    distractor_median_char_count = float(median(metrics.char_count for metrics in distractor_metrics))

    warnings: list[str] = []
    if _is_unique_longest(correct_answer, answer_metrics) and _is_meaningfully_longer(
        correct_answer.word_count,
        distractor_median_word_count,
        correct_answer.char_count,
        distractor_median_char_count,
    ):
        warnings.append(
            "Correct answer is substantially longer than distractors "
            f"({correct_answer.word_count} words vs median {distractor_median_word_count:.1f})."
        )
    elif _is_unique_shortest(correct_answer, answer_metrics) and _is_meaningfully_shorter(
        correct_answer.word_count,
        distractor_median_word_count,
        correct_answer.char_count,
        distractor_median_char_count,
    ):
        warnings.append(
            "Correct answer is substantially shorter than distractors "
            f"({correct_answer.word_count} words vs median {distractor_median_word_count:.1f})."
        )

    return QuestionDiagnostics(
        warnings=tuple(warnings),
        answer_metrics=answer_metrics,
        correct_answer_index=correct_answer.index,
        correct_word_count=correct_answer.word_count,
        distractor_median_word_count=distractor_median_word_count,
        correct_char_count=correct_answer.char_count,
        distractor_median_char_count=distractor_median_char_count,
    )


def _build_answer_metrics(question: Question) -> list[AnswerLengthMetrics]:
    metrics: list[AnswerLengthMetrics] = []
    for index, answer in enumerate(question.answers):
        visible_text = extract_visible_text(answer.text)
        metrics.append(
            AnswerLengthMetrics(
                index=index,
                is_correct=answer.is_correct,
                visible_text=visible_text,
                word_count=len(_WORD_PATTERN.findall(visible_text)),
                char_count=len(visible_text),
            )
        )
    return metrics


def _is_unique_longest(correct_answer: AnswerLengthMetrics, answer_metrics: tuple[AnswerLengthMetrics, ...]) -> bool:
    longest_word_count = max(metrics.word_count for metrics in answer_metrics)
    return (
        correct_answer.word_count == longest_word_count
        and sum(metrics.word_count == longest_word_count for metrics in answer_metrics) == 1
    )


def _is_unique_shortest(correct_answer: AnswerLengthMetrics, answer_metrics: tuple[AnswerLengthMetrics, ...]) -> bool:
    shortest_word_count = min(metrics.word_count for metrics in answer_metrics)
    return (
        correct_answer.word_count == shortest_word_count
        and sum(metrics.word_count == shortest_word_count for metrics in answer_metrics) == 1
    )


def _is_meaningfully_longer(
    correct_word_count: int,
    distractor_median_word_count: float,
    correct_char_count: int,
    distractor_median_char_count: float,
) -> bool:
    if _exceeds_ratio_and_delta(
        correct_word_count,
        distractor_median_word_count,
        _LONG_RATIO_THRESHOLD,
        _MIN_WORD_DELTA,
    ):
        return True
    if max(correct_word_count, distractor_median_word_count) >= _SHORT_TEXT_WORD_FALLBACK_LIMIT:
        return False
    return _exceeds_ratio_and_delta(
        correct_char_count,
        distractor_median_char_count,
        _LONG_RATIO_THRESHOLD,
        _MIN_CHAR_DELTA,
    )


def _is_meaningfully_shorter(
    correct_word_count: int,
    distractor_median_word_count: float,
    correct_char_count: int,
    distractor_median_char_count: float,
) -> bool:
    if _falls_below_ratio_and_delta(
        correct_word_count,
        distractor_median_word_count,
        _SHORT_RATIO_THRESHOLD,
        _MIN_WORD_DELTA,
    ):
        return True
    if max(correct_word_count, distractor_median_word_count) >= _SHORT_TEXT_WORD_FALLBACK_LIMIT:
        return False
    return _falls_below_ratio_and_delta(
        correct_char_count,
        distractor_median_char_count,
        _SHORT_RATIO_THRESHOLD,
        _MIN_CHAR_DELTA,
    )


def _exceeds_ratio_and_delta(value: int, reference: float, ratio_threshold: float, minimum_delta: int) -> bool:
    if reference <= 0 or value <= reference:
        return False
    return value / reference >= ratio_threshold and value - reference >= minimum_delta


def _falls_below_ratio_and_delta(value: int, reference: float, ratio_threshold: float, minimum_delta: int) -> bool:
    if value <= 0 or reference <= 0 or value >= reference:
        return False
    return value / reference <= ratio_threshold and reference - value >= minimum_delta