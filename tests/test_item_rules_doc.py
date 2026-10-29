"""The rule page (docs/item-rules.md) and the code that tests the rules must name the same rules."""

import json
import re
from pathlib import Path

from qb.checks import CHECKER_WARNINGS
from qb.lint import RULES

RULE_PAGE = Path(__file__).resolve().parents[1] / "docs" / "item-rules.md"
CHECK_SCHEMA = Path(__file__).resolve().parents[1] / "qb" / "schemas" / "check-result.schema.json"
RULE_LINE = re.compile(r"^- \*\*(?P<id>[A-Z]+-[A-Z]+)\*\* · (?P<tests>[^·]+) · (?P<severity>error|warning) — ", re.M)


def _page_rules() -> dict[str, tuple[set[str], str]]:
    page_rules: dict[str, tuple[set[str], str]] = {}
    for match in RULE_LINE.finditer(RULE_PAGE.read_text(encoding="utf-8")):
        assert match["id"] not in page_rules, f"{match['id']} is defined twice"
        tests = {test.strip() for test in match["tests"].split("+")}
        page_rules[match["id"]] = (tests, match["severity"])
    return page_rules


def test_every_lint_rule_is_on_the_page_with_its_severity() -> None:
    page_rules = _page_rules()

    for rule_id, (severity, _) in RULES.items():
        assert rule_id in page_rules, f"{rule_id} is in qb/lint.py but not on the rule page"
        tests, page_severity = page_rules[rule_id]
        assert "lint" in tests, f"{rule_id} is not marked as tested by lint on the rule page"
        assert page_severity == severity, f"{rule_id}: {page_severity} on the page, {severity} in qb/lint.py"


def test_every_rule_the_page_says_lint_tests_exists_in_the_code() -> None:
    marked_lint = {rule_id for rule_id, (tests, _) in _page_rules().items() if "lint" in tests}

    assert marked_lint == set(RULES)


def test_every_rule_names_known_tests() -> None:
    for rule_id, (tests, _) in _page_rules().items():
        assert tests <= {"lint", "A", "B", "C"}, f"{rule_id}: unknown test in {tests}"


def test_the_checker_reports_the_rules_of_steps_a_and_c_and_derives_those_of_step_b() -> None:
    definitions = json.loads(CHECK_SCHEMA.read_text(encoding="utf-8"))["$defs"]
    page_rules = _page_rules()

    def tested_in(step: str) -> set[str]:
        return {rule_id for rule_id, (tests, _) in page_rules.items() if step in tests}

    assert set(definitions["a_rule"]["enum"]) == tested_in("A")
    assert set(definitions["c_rule"]["enum"]) == tested_in("C")
    assert tested_in("B") == {"KEY-UNIQUE", "DIS-FALSE"}


def test_the_checker_warnings_are_the_page_warnings() -> None:
    page_rules = _page_rules()
    checker_rules = {rule_id for rule_id, (tests, _) in page_rules.items() if tests & {"A", "B", "C"}}

    assert CHECKER_WARNINGS == {rule_id for rule_id in checker_rules if page_rules[rule_id][1] == "warning"}
