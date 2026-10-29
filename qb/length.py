"""Answer-length analysis: is the key the option that stands out by length?

A key that is uniquely the longest (or shortest) option by a clear margin lets students guess without knowing
the topic. "Clear margin" means 1.35 times the median distractor and at least 4 words more; for options under
6 words, at least 24 characters more.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import re
from statistics import median

from qb.html import visible_text


_WORD_PATTERN = re.compile(r"\w+", re.UNICODE)

_LONG_RATIO_THRESHOLD = 1.35
_SHORT_RATIO_THRESHOLD = 1 / _LONG_RATIO_THRESHOLD
_MIN_WORD_DELTA = 4
_MIN_CHAR_DELTA = 24
_SHORT_TEXT_WORD_FALLBACK_LIMIT = 6


@dataclass(frozen=True)
class AnswerLengthMetrics:
    """Visible-text metrics for one answer option."""

    index: int
    is_correct: bool
    visible_text: str
    word_count: int
    char_count: int


@dataclass(frozen=True)
class LengthAnalysis:
    """Length warnings for one question, with the numbers behind them."""

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


def analyze_answer_lengths(answers: Sequence[tuple[str, bool]]) -> LengthAnalysis:
    """Analyze (html_text, is_correct) answer pairs. Questions without exactly one key get no warning."""
    answer_metrics = tuple(_build_answer_metrics(answers))
    correct_metrics = [metrics for metrics in answer_metrics if metrics.is_correct]
    distractor_metrics = [metrics for metrics in answer_metrics if not metrics.is_correct]

    if len(correct_metrics) != 1 or not distractor_metrics:
        return LengthAnalysis(
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
    if is_unique_longest(correct_answer, answer_metrics, "word_count") and _is_meaningfully_longer(
        correct_answer.word_count,
        distractor_median_word_count,
        correct_answer.char_count,
        distractor_median_char_count,
    ):
        warnings.append(
            "Correct answer is substantially longer than distractors "
            f"({correct_answer.word_count} words vs median {distractor_median_word_count:.1f})."
        )
    elif is_unique_shortest(correct_answer, answer_metrics) and _is_meaningfully_shorter(
        correct_answer.word_count,
        distractor_median_word_count,
        correct_answer.char_count,
        distractor_median_char_count,
    ):
        warnings.append(
            "Correct answer is substantially shorter than distractors "
            f"({correct_answer.word_count} words vs median {distractor_median_word_count:.1f})."
        )

    return LengthAnalysis(
        warnings=tuple(warnings),
        answer_metrics=answer_metrics,
        correct_answer_index=correct_answer.index,
        correct_word_count=correct_answer.word_count,
        distractor_median_word_count=distractor_median_word_count,
        correct_char_count=correct_answer.char_count,
        distractor_median_char_count=distractor_median_char_count,
    )


def is_unique_longest(
    correct_answer: AnswerLengthMetrics,
    answer_metrics: Sequence[AnswerLengthMetrics],
    unit: str = "word_count",
) -> bool:
    """Tell whether the key is longer than every other option, in words or in characters (unit="char_count")."""
    longest = max(getattr(metrics, unit) for metrics in answer_metrics)
    return (
        getattr(correct_answer, unit) == longest
        and sum(getattr(metrics, unit) == longest for metrics in answer_metrics) == 1
    )


def is_unique_shortest(correct_answer: AnswerLengthMetrics, answer_metrics: Sequence[AnswerLengthMetrics]) -> bool:
    """Tell whether the key has fewer words than every other option."""
    shortest_word_count = min(metrics.word_count for metrics in answer_metrics)
    return (
        correct_answer.word_count == shortest_word_count
        and sum(metrics.word_count == shortest_word_count for metrics in answer_metrics) == 1
    )


def _build_answer_metrics(answers: Sequence[tuple[str, bool]]) -> list[AnswerLengthMetrics]:
    metrics: list[AnswerLengthMetrics] = []
    for index, (html_text, is_correct) in enumerate(answers):
        text = visible_text(html_text)
        metrics.append(
            AnswerLengthMetrics(
                index=index,
                is_correct=is_correct,
                visible_text=text,
                word_count=len(_WORD_PATTERN.findall(text)),
                char_count=len(text),
            )
        )
    return metrics


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
