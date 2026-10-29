"""Tests for qb.lint. Each flaw is shown on a variant of one clean, synthetic item."""

import copy

from qb.lint import lint_document, lint_question


def _clean_question() -> dict:
    return {
        "id": "T_Q001",
        "name": "Q001: Escalado y distancias",
        "question_text": (
            "<p>Un modelo k-NN usa dos variables: la edad (de 18 a 90 años) y los ingresos anuales "
            "(de 10 000 a 200 000 euros). ¿Qué ocurre con las distancias si no se escalan las variables?</p>"
        ),
        "general_feedback": (
            "<p>La distancia euclídea suma diferencias al cuadrado, así que la variable con mayor rango "
            "domina el resultado.</p>"
        ),
        "answers": [
            {
                "text": "<p>Los ingresos dominan la distancia, porque su rango es miles de veces mayor que el de la edad.</p>",
                "fraction": "100",
                "feedback": "<p>Correcto. Una diferencia de ingresos de miles de euros pesa mucho más que una de pocos años.</p>",
            },
            {
                "text": "<p>La edad domina la distancia, porque su escala en años es más fina que la de los ingresos.</p>",
                "fraction": "-50",
                "feedback": "<p>Incorrecto. La finura de la escala no importa; importa el tamaño de las diferencias.</p>",
            },
            {
                "text": "<p>Las dos variables pesan lo mismo, porque k-NN normaliza las distancias al calcularlas.</p>",
                "fraction": "-50",
                "feedback": "<p>Incorrecto. k-NN usa la distancia tal como la recibe; escalar es un paso previo.</p>",
            },
            {
                "text": "<p>Las variables se compensan, porque la distancia euclídea divide cada diferencia entre su unidad.</p>",
                "fraction": "-50",
                "feedback": "<p>Incorrecto. La distancia euclídea no conoce las unidades: suma las diferencias tal cual.</p>",
            },
        ],
    }


def _rules(question: dict, distractors: int = 3, with_reasoning: bool = False) -> list[str]:
    return [finding.rule for finding in lint_question(question, distractors, with_reasoning=with_reasoning)]


def test_a_clean_question_has_no_findings() -> None:
    assert lint_question(_clean_question(), 3, with_reasoning=False) == []


def test_graded_framing_in_the_stem() -> None:
    question = _clean_question()
    question["question_text"] = "<p>¿Qué opción describe mejor el efecto de no escalar las variables en k-NN?</p>"

    findings = lint_question(question, 3, with_reasoning=False)

    assert [finding.message for finding in findings if finding.rule == "STEM-GRADED"] == [
        "graded wording: '¿que opcion describe mejor el efecto de no escalar las variables en k-nn?'"
    ]


def test_a_presupposed_comparison_in_a_por_que_stem() -> None:
    question = _clean_question()
    question["question_text"] = "<p>¿Por qué k-NN es más adecuado que un árbol de decisión para estos datos?</p>"

    messages = [finding.message for finding in lint_question(question, 3, with_reasoning=False)]

    assert any(message.startswith("presupposed comparison") for message in messages)


def test_comparisons_in_the_scenario_are_not_graded_framing() -> None:
    question = _clean_question()
    question["question_text"] = (
        "<p>Un árbol ajusta mejor el conjunto de entrenamiento que una regresión lineal, pero obtiene mejores "
        "resultados en train que en test. ¿Qué indica esa diferencia?</p>"
    )

    assert "STEM-GRADED" not in _rules(question)


def test_options_to_a_por_que_stem_must_start_with_porque() -> None:
    question = _clean_question()
    question["question_text"] = "<p>¿Por qué conviene escalar las variables antes de usar k-NN?</p>"
    for answer in question["answers"][:3]:
        answer["text"] = "<p>Porque " + answer["text"][3:].lower()

    findings = [finding for finding in lint_question(question, 3, with_reasoning=False) if finding.rule == "OPT-PORQUE"]

    assert [finding.answer_index for finding in findings] == [3]


def test_references_to_the_material() -> None:
    question = _clean_question()
    question["general_feedback"] = "<p>Esa es la distinción central del material.</p>"

    assert "LANG-SELF" in _rules(question)


def test_trust_framing() -> None:
    question = _clean_question()
    question["answers"][2]["text"] = "<p>Escalar no hace falta: basta con entrenar y confiar en que el modelo compense.</p>"

    assert "LANG-TRUST" in _rules(question)


def test_loaded_adjectives_in_distractors() -> None:
    question = _clean_question()
    question["answers"][1]["text"] = "<p>La edad crea un error enorme, porque los años se cuentan de uno en uno.</p>"

    assert "DIS-LOADED" in _rules(question)


def test_absolutes_only_in_distractors() -> None:
    question = _clean_question()
    question["answers"][1]["text"] = "<p>La edad siempre domina la distancia, porque se mide en años enteros.</p>"
    question["answers"][2]["text"] = "<p>Las dos variables pesan lo mismo, porque k-NN solo usa el orden de los valores.</p>"

    assert "DIS-ABSOLUTE" in _rules(question)


def test_a_key_that_stands_out_by_length() -> None:
    question = _clean_question()
    question["answers"][0]["text"] = (
        "<p>Los ingresos dominan la distancia, porque su rango es miles de veces mayor que el de la edad, de modo "
        "que cualquier diferencia de ingresos, por pequeña que sea, pesa más que la mayor diferencia posible de edad.</p>"
    )

    assert "KEY-LENGTH" in _rules(question)


def test_hedging_and_thin_feedback() -> None:
    question = _clean_question()
    question["answers"][1]["feedback"] = "<p>Incorrecto. Es casi correcta, aunque no del todo.</p>"
    question["answers"][2]["feedback"] = "<p>Incorrecto.</p>"

    findings = lint_question(question, 3, with_reasoning=False)

    assert {(finding.rule, finding.answer_index) for finding in findings} >= {("FB-HEDGE", 1), ("FB-THIN", 2)}


def test_duplicate_and_empty_options() -> None:
    question = _clean_question()
    question["answers"][3]["text"] = question["answers"][2]["text"]
    question["answers"][1]["feedback"] = ""

    rules = _rules(question)

    assert "FMT-DUPLICATE" in rules and "FMT-EMPTY" in rules


def test_qt_markup_in_learner_facing_text() -> None:
    question = _clean_question()
    question["question_text"] = '<html><body style="font-size:16pt"><p>¿Qué ocurre?</p></body></html>'

    assert "FMT-HTML" in _rules(question)


def test_a_v1_batch_expects_six_distractors_and_a_valid_schema() -> None:
    question = _clean_question() | {"surface": "SURF-01"}

    findings = lint_document({"version": "1.0", "questions": [question]})

    assert {finding.rule for finding in findings} == {"FMT-SCHEMA", "FMT-ANSWERS"}
    assert any(finding.message == "distractor_count is 3, expected 6" for finding in findings)


def test_a_review_session_checks_three_distractors_only_on_ready_questions() -> None:
    ready = _clean_question() | {"status": "ready"}
    pending_with_extra_option = copy.deepcopy(ready) | {"id": "T_Q002", "status": "pending"}
    pending_with_extra_option["answers"].append(dict(pending_with_extra_option["answers"][1], text="<p>Otra</p>"))
    session = {"artifact_type": "review_session", "questions": [ready, pending_with_extra_option]}

    assert [finding.rule for finding in lint_document(session)] == []


def test_reasoning_fields_are_required_in_v2_items() -> None:
    question = _clean_question() | {"claim": "Sin escalar, la variable de mayor rango domina la distancia."}

    findings = lint_question(question, 3, with_reasoning=True)

    assert {finding.rule for finding in findings} == {"GROUND-EVIDENCE", "GROUND-REASONING"}


def test_a_stem_that_states_its_claim() -> None:
    question = _clean_question() | {
        "claim": "La variable de mayor rango domina la distancia",
        "evidence": [{"locator": "knn.ipynb#Scaling", "quote": "The feature with the larger range dominates."}],
    }
    question["question_text"] = "<p>Si no se escala, la variable de mayor rango domina la distancia. ¿Qué hacer?</p>"
    question["answers"][0]["why_right"] = "Escalar iguala los rangos."
    for answer in question["answers"][1:]:
        answer["misconception"] = {"belief": "Una creencia.", "origin": "inferred"}
        answer["why_wrong"] = "Una refutación."

    assert _rules(question, with_reasoning=True) == ["STEM-CLAIM"]
