"""Deterministic checks of question batches and review sessions. Every finding names the rule it breaks.

These are the checks a pattern can decide; flaws that need understanding (a distractor that contradicts the stem,
a stem that leaks its answer, an ambiguous key) are left to the checker. Patterns match visible text in lower
case without accents, so "¿Por qué" and "¿Por que" are the same.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import asdict, dataclass
import re
import unicodedata

from qb.html import markup_problems, visible_text
from qb.length import analyze_answer_lengths
from qb.schema import (
    BATCH,
    answer_shape_problems,
    answers_of,
    artifact_kind,
    batch_schema_errors,
    expected_distractors,
    is_correct_fraction,
    question_label,
)


RULES: dict[str, tuple[str, str]] = {
    "FMT-SCHEMA": ("error", "The batch doesn't match the item schema."),
    "FMT-ANSWERS": ("error", "Not exactly one key, or not the expected number of distractors."),
    "FMT-EMPTY": ("error", "Empty stem, option or option feedback."),
    "FMT-DUPLICATE": ("error", "Two options with the same visible text."),
    "FMT-HTML": ("error", "A Qt document, an inline style or a tag outside the whitelist in learner-facing text."),
    "STEM-GRADED": (
        "error",
        "Graded framing in the question (¿qué describe mejor...?, ¿la más precisa?) or a presupposed comparison "
        "(¿por qué X es mejor que Y?).",
    ),
    "STEM-DIRECT": ("warning", "A 'which statement is correct' stem that can't be answered before reading the options."),
    "OPT-PORQUE": ("error", "An option to a '¿Por qué...?' stem that doesn't start with 'Porque'."),
    "LANG-SELF": ("error", "Learner-facing text that refers to the course material."),
    "LANG-TRUST": ("error", "'Confiar en que' framing."),
    "DIS-LOADED": ("warning", "A loaded adjective that marks a distractor as wrong (enorme, confuso, absurdo...)."),
    "DIS-ABSOLUTE": ("warning", "Absolutes (siempre, solo, nunca...) in most distractors but not in the key."),
    "KEY-LENGTH": ("warning", "The key is uniquely the longest or shortest option by a clear margin."),
    "FB-HEDGE": ("warning", "Distractor feedback that hedges about correctness (casi correcta, no es la mejor...)."),
    "FB-THIN": ("warning", "Option feedback too short to explain the option."),
    "GROUND-EVIDENCE": ("error", "An item without evidence: a locator and a quote from the material."),
    "GROUND-REASONING": (
        "error", "Missing claim, a key without why_right, or a distractor without misconception or why_wrong."
    ),
    "STEM-CLAIM": ("error", "The stem states the claim the item tests."),
}

# Graded framing is searched only inside the question clause (from '¿' to '?'): comparisons that describe the
# scenario ("un árbol ajusta mejor train que...") are legitimate. Plural "mejores" is descriptive, so it is ignored.
_QUESTION_CLAUSE = re.compile(r"¿[^?]*\?")
_GRADED = [
    re.compile(r"\bmejor\b"),
    re.compile(
        r"\bmas (adecuad|apropiad|precis|correct|acertad|exact|complet|razonabl|convenient|recomendabl|indicad"
        r"|idone|solid|convincent|important|relevant|eficient|probabl|fiabl)\w*"
    ),
    re.compile(r"\bmas (util|utiles|eficaz|eficaces)\b"),
    re.compile(r"\bpreferibles?\b"),
    re.compile(r"\bmayor (precision|exactitud|claridad|rigor|acierto)\b"),
    re.compile(
        r"\b(la|el|las|los) principal(es)? (razon|ventaja|motivo|causa|diferencia|objetivo|problema|riesgo|limitacion"
        r"|beneficio|funcion|proposito)"
    ),
    re.compile(r"\b(best|better|most appropriate|most accurate|most suitable|most correct|closest|least wrong)\b"),
]
# "Which statement is correct" stems can't be answered before reading the options (the cover-the-options test).
_INDIRECT = [
    re.compile(r"^¿(que|cual|cuales) (afirmacion|afirmaciones|opcion|opciones|enunciado|descripcion|explicacion"
               r"|combinacion)\b"),
    re.compile(r"\b(describe|describen|explica|explican|resume|define|refleja|evalua) correctamente\b"),
]
_MATERIAL = [
    re.compile(
        r"\bsegun (el|la|los|las) (material|materiales|notas|apuntes|cuaderno|notebook|temario|curso"
        r"|documentacion del curso)\b"
    ),
    re.compile(r"\b(el|del|al) material(es)?\b"),
    re.compile(r"\b(los apuntes|las notas del curso)\b"),
    re.compile(
        r"\b(visto|vista|vistos|vistas|explicado|explicada|explicados|explicadas|estudiado|estudiada|vimos)"
        r" en (clase|el curso|el material|los apuntes)\b"
    ),
    re.compile(r"\baccording to the (material|notes|notebook|course|slides)\b"),
    re.compile(r"\b(in|from) the (course )?(material|notes|slides)\b"),
]
_TRUST = [re.compile(r"\bconfi(ar|ando|amos|a|an) en que\b"), re.compile(r"\by confiar\b")]
_LOADED = [
    re.compile(
        r"\b(enormes?|confus[oa]s?|caotic[oa]s?|absurd[oa]s?|ridicul[oa]s?|magic[oa]s?|milagros[oa]s?"
        r"|disparatad[oa]s?)\b"
    )
]
_ABSOLUTE = [
    re.compile(
        r"\b(siempre|nunca|jamas|solo|unicamente|exclusivamente|automaticamente|garantiza|garantizan|garantizar"
        r"|completamente|totalmente|imposible|ningun|ninguna|todos los|todas las|cualquier|necesariamente)\b"
    )
]
# Hedges about correctness only: bare "casi" or "en parte" are ordinary Spanish ("casi todos", "en parte del proceso").
_HEDGES = [
    re.compile(
        r"\b(casi (correct|ciert|verdader|valid)\w*|(parcialmente|en parte) (correct|ciert|verdader|valid)\w*"
        r"|no del todo|no es (la|el) (mejor|mas)\b|menos (precis|complet|adecuad|apropiad|correct)\w*"
        r"|not the best|(partially|almost) (correct|true|right))"
    )
]
_FEEDBACK_VERDICT = re.compile(r"^(in)?correct[oa]?\s*[.:,!]?\s*")
_WORD = re.compile(r"\w+")
_THIN_FEEDBACK_WORDS = 5
_REASONING_FIELDS = ("evidence", "claim", "target_id", "stem_premises")


@dataclass(frozen=True)
class Finding:
    """One broken rule in one question; answer_index points at the option when the rule is about one."""

    rule: str
    severity: str
    question_id: str
    message: str
    answer_index: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def lint_document(data: Mapping, distractors: int | None = None) -> list[Finding]:
    """Check every question of a batch or review session; distractors overrides the expected count."""
    findings: list[Finding] = []
    kind = artifact_kind(data)
    if kind == BATCH:
        findings.extend(Finding("FMT-SCHEMA", "error", "", message) for message in batch_schema_errors(data))
    is_v2_batch = kind == BATCH and str(data.get("version")) == "2.0"
    for question in data.get("questions", []):
        if not isinstance(question, Mapping):
            continue
        expected = distractors if distractors is not None else expected_distractors(data, question)
        with_reasoning = is_v2_batch or any(field in question for field in _REASONING_FIELDS)
        findings.extend(lint_question(question, expected, with_reasoning=with_reasoning))
    return findings


def lint_question(question: Mapping, expected_distractors: int | None, *, with_reasoning: bool) -> list[Finding]:
    """Check one question. with_reasoning adds the rules of the v2 reasoning fields."""
    question_id = question_label(question)
    findings: list[Finding] = []

    def add(rule: str, message: str, answer_index: int | None = None) -> None:
        findings.append(Finding(rule, RULES[rule][0], question_id, message, answer_index))

    answers = answers_of(question)
    keys = [index for index, answer in enumerate(answers) if is_correct_fraction(answer.get("fraction"))]
    distractor_indexes = [index for index in range(len(answers)) if index not in keys]
    option_texts = [plain_text(str(answer.get("text") or "")) for answer in answers]
    stem = plain_text(str(question.get("question_text") or ""))

    for problem, actual, expected in answer_shape_problems(
        [answer.get("fraction") for answer in answers], expected_distractors
    ):
        add("FMT-ANSWERS", f"{problem} is {actual}, expected {expected}")

    if not stem:
        add("FMT-EMPTY", "empty stem")
    for index, answer in enumerate(answers):
        if not option_texts[index]:
            add("FMT-EMPTY", "empty option", index)
        if not plain_text(str(answer.get("feedback") or "")):
            add("FMT-EMPTY", "empty option feedback", index)

    first_index_of_text: dict[str, int] = {}
    for index, text in enumerate(option_texts):
        if text and text in first_index_of_text:
            add("FMT-DUPLICATE", f"same text as option {first_index_of_text[text] + 1}", index)
        first_index_of_text.setdefault(text, index)

    for field_name, index, html_text in _learner_fields(question):
        problems = markup_problems(html_text)
        if problems:
            add("FMT-HTML", f"{field_name}: {', '.join(problems)}", index)
        text = plain_text(html_text)
        if match := _first_match(_MATERIAL, text):
            add("LANG-SELF", f"{field_name} refers to the material: '{match}'", index)
        if match := _first_match(_TRUST, text):
            add("LANG-TRUST", f"{field_name}: '{match}'", index)

    clauses = _QUESTION_CLAUSE.findall(stem) or [stem]
    for clause in clauses:
        if _first_match(_GRADED, clause):
            kind = "presupposed comparison" if clause.startswith("¿por que") else "graded wording"
            add("STEM-GRADED", f"{kind}: '{clause[:90]}'")
            break
    for clause in clauses:
        if _first_match(_INDIRECT, clause):
            add("STEM-DIRECT", f"answerable only through the options: '{clause[:90]}'")
            break

    if "¿por que" in stem or stem.startswith("por que"):
        for index, text in enumerate(option_texts):
            if text and not text.lstrip(" ¿¡\"'«“-–—•").startswith("porque"):
                add("OPT-PORQUE", "option to a '¿Por qué...?' stem doesn't start with 'Porque'", index)

    for index in distractor_indexes:
        if match := _first_match(_LOADED, option_texts[index]):
            add("DIS-LOADED", f"loaded adjective '{match}'", index)

    distractors_with_absolutes = [index for index in distractor_indexes if _first_match(_ABSOLUTE, option_texts[index])]
    key_has_absolutes = any(_first_match(_ABSOLUTE, option_texts[index]) for index in keys)
    if (
        distractor_indexes
        and not key_has_absolutes
        and len(distractors_with_absolutes) * 2 >= len(distractor_indexes)
    ):
        add(
            "DIS-ABSOLUTE",
            f"{len(distractors_with_absolutes)} of {len(distractor_indexes)} distractors use absolutes; the key doesn't",
        )

    length_analysis = analyze_answer_lengths(
        [(str(answer.get("text") or ""), index in keys) for index, answer in enumerate(answers)]
    )
    for warning in length_analysis.warnings:
        add("KEY-LENGTH", warning)

    for index, answer in enumerate(answers):
        feedback = plain_text(str(answer.get("feedback") or ""))
        if not feedback:
            continue
        if index in distractor_indexes and (match := _first_match(_HEDGES, feedback)):
            add("FB-HEDGE", f"hedging feedback: '{match}'", index)
        if len(_WORD.findall(_FEEDBACK_VERDICT.sub("", feedback))) < _THIN_FEEDBACK_WORDS:
            add("FB-THIN", "feedback doesn't explain the option", index)

    if with_reasoning:
        _check_reasoning_fields(question, answers, keys, stem, add)
    return findings


def plain_text(html_text: str) -> str:
    """Visible text in lower case without accents: the form every pattern here matches."""
    decomposed = unicodedata.normalize("NFKD", visible_text(html_text).lower())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def _check_reasoning_fields(
    question: Mapping,
    answers: list[Mapping],
    keys: list[int],
    stem: str,
    add: Callable[..., None],
) -> None:
    evidence = question.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(item, Mapping) and item.get("locator") and item.get("quote") for item in evidence
    ):
        add("GROUND-EVIDENCE", "no evidence with a locator and a quote")

    claim = plain_text(str(question.get("claim") or ""))
    if not claim:
        add("GROUND-REASONING", "no claim")
    for index, answer in enumerate(answers):
        if index in keys:
            if not str(answer.get("why_right") or "").strip():
                add("GROUND-REASONING", "key without why_right", index)
            continue
        misconception = answer.get("misconception")
        if not isinstance(misconception, Mapping) or not misconception.get("belief"):
            add("GROUND-REASONING", "distractor without misconception", index)
        if not str(answer.get("why_wrong") or "").strip():
            add("GROUND-REASONING", "distractor without why_wrong", index)

    premises = [plain_text(str(premise)) for premise in question.get("stem_premises") or []]
    if claim and (claim in stem or claim in premises):
        add("STEM-CLAIM", "the stem states the claim it tests")


def _learner_fields(question: Mapping) -> Iterator[tuple[str, int | None, str]]:
    yield "stem", None, str(question.get("question_text") or "")
    yield "general feedback", None, str(question.get("general_feedback") or "")
    for index, answer in enumerate(answers_of(question)):
        yield "option", index, str(answer.get("text") or "")
        yield "option feedback", index, str(answer.get("feedback") or "")


def _first_match(patterns: list[re.Pattern[str]], text: str) -> str | None:
    for pattern in patterns:
        if match := pattern.search(text):
            return match.group(0)
    return None
