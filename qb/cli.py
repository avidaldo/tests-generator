"""The `qb` command: check question files, run the checker's bookkeeping and export to Moodle XML."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
import json
import os
from pathlib import Path
import sys
import tempfile

from qb.calibration import calibration_report, unlabelled_copy
from qb.checks import BLIND_CHECKS, BLIND_MAP, attach_audit_checks, attach_blind_checks, blind_view
from qb.export import ExportError, moodle_xml, select_questions
from qb.lint import RULES, Finding, lint_document
from qb.schema import STATUSES, load_json, normalize_status


_STATUS_CHOICES = [*STATUSES, "pendiente", "revisar", "lista"]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line; returns the process exit code."""
    parser = argparse.ArgumentParser(prog="qb", description="Question-bank tools for the Moodle quiz pipeline.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    lint_parser = subcommands.add_parser(
        "lint",
        help="check batches or review sessions against the deterministic rules",
        description="Exit code 1 when any error-level rule is broken. Rules: "
        + "; ".join(f"{rule_id} ({severity})" for rule_id, (severity, _) in RULES.items()),
    )
    lint_parser.add_argument("files", nargs="+", type=Path, help="batch or review-session JSON files")
    lint_parser.add_argument(
        "--distractors",
        type=int,
        help="expected distractors per question (default: 6 in v1 batches, 4 in v2, 3 for ready questions)",
    )
    output_mode = lint_parser.add_mutually_exclusive_group()
    output_mode.add_argument("--json", action="store_true", help="print the findings as JSON")
    output_mode.add_argument("--summary", action="store_true", help="print only the questions affected per rule")

    export_parser = subcommands.add_parser(
        "export",
        help="write Moodle XML from a review session (by default only ready questions)",
    )
    export_parser.add_argument("input", type=Path, help="review-session or batch JSON file")
    export_parser.add_argument("output", type=Path, help="XML file, a directory, or '.' for a name from the input")
    status_selection = export_parser.add_mutually_exclusive_group()
    status_selection.add_argument("--status", nargs="+", choices=_STATUS_CHOICES, metavar="STATUS",
                                  help="statuses to export (default: ready)")
    status_selection.add_argument("--all-statuses", action="store_true", help="export every question")
    export_parser.add_argument("--easy-only", action="store_true", help="export only questions marked easy")
    export_parser.add_argument("--wrong-fraction", help="fraction for every distractor, e.g. -50 or -33.33333")
    export_parser.add_argument("-v", "--verbose", action="store_true", help="print a summary of the export")

    blind_parser = subcommands.add_parser(
        "blind",
        help="write the checker's key-less view of a question file (steps A and B) and the map that undoes it",
    )
    blind_parser.add_argument("input", type=Path, help="batch or review-session JSON file")
    blind_parser.add_argument("--out", type=Path, required=True, help="the key-less view, for the checker")
    blind_parser.add_argument("--map", type=Path, required=True, help="the letter map; keep it away from the checker")
    blind_parser.add_argument("--seed", type=int, default=1, help="shuffle seed (default 1); another seed reshuffles")

    attach_parser = subcommands.add_parser(
        "attach-checks",
        help="validate checker results and merge them into the question file, in place",
        description="Steps A and B (blind_checks) need the --map written by `qb blind`; step C (audit_checks) needs "
        "steps A and B attached first. Nothing is written when any result is invalid. Close the file in the editor "
        "first: its autosave would overwrite the checks.",
    )
    attach_parser.add_argument("input", type=Path, help="the batch or review session the blind view was made from")
    attach_parser.add_argument("results", type=Path, help="blind_checks or audit_checks JSON written by the checker")
    attach_parser.add_argument("--map", type=Path, help="the letter map from `qb blind` (steps A and B only)")

    calibrate_parser = subcommands.add_parser(
        "calibrate",
        help="measure the checker on items a teacher has judged (Lista = good, Revisar = flawed, rules in the notes)",
    )
    calibrate_steps = calibrate_parser.add_subparsers(dest="step", required=True)
    prepare_parser = calibrate_steps.add_parser("prepare", help="write the judged items without the judgement")
    prepare_parser.add_argument("labelled", type=Path, help="review session with the teacher's statuses and notes")
    prepare_parser.add_argument("--out", type=Path, required=True, help="the copy to run /quiz-check on")
    report_parser = calibrate_steps.add_parser("report", help="compare the checked copy with the teacher's labels")
    report_parser.add_argument("labelled", type=Path, help="review session with the teacher's statuses and notes")
    report_parser.add_argument("checked", type=Path, help="the copy from `calibrate prepare`, after /quiz-check")
    report_parser.add_argument("--catch", type=float, default=0.8, help="target share of flawed items flagged")
    report_parser.add_argument("--false-alarms", type=float, default=0.2, help="maximum share of good items flagged")
    report_parser.add_argument("--json", action="store_true", help="print the full report as JSON")

    args = parser.parse_args(argv)
    commands = {
        "lint": _lint, "export": _export, "blind": _blind, "attach-checks": _attach_checks, "calibrate": _calibrate
    }
    return commands[args.command](args)


def _lint(args: argparse.Namespace) -> int:
    reports: list[tuple[Path, int, list[Finding]]] = []
    for path in args.files:
        try:
            data = load_json(path)
        except (OSError, ValueError) as error:
            print(f"{path}: {error}", file=sys.stderr)
            return 2
        reports.append((path, len(data["questions"]), lint_document(data, args.distractors)))

    if args.json:
        payload = [
            {"path": str(path), "questions": question_count, "findings": [finding.to_dict() for finding in findings]}
            for path, question_count, findings in reports
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif args.summary:
        _print_summary(reports)
    else:
        for path, question_count, findings in reports:
            print(f"{path} ({question_count} questions)")
            for finding in findings:
                option = f"option {finding.answer_index + 1}" if finding.answer_index is not None else ""
                print(f"  {finding.severity:<7} {finding.rule:<16} {finding.question_id:<14} {option:<9} "
                      f"{finding.message}")
        _print_summary(reports)

    has_errors = any(finding.severity == "error" for _, _, findings in reports for finding in findings)
    return 1 if has_errors else 0


def _print_summary(reports: list[tuple[Path, int, list[Finding]]]) -> None:
    total_questions = sum(question_count for _, question_count, _ in reports)
    questions_per_rule: dict[str, set[tuple[str, str]]] = defaultdict(set)
    findings_per_rule: Counter[str] = Counter()
    for path, _, findings in reports:
        for finding in findings:
            questions_per_rule[finding.rule].add((str(path), finding.question_id))
            findings_per_rule[finding.rule] += 1
    print(f"\n{total_questions} questions in {len(reports)} file(s)")
    print(f"  {'rule':<16} {'severity':<8} {'questions':>10} {'findings':>9}")
    for rule_id, (severity, _) in RULES.items():
        if findings_per_rule[rule_id]:
            print(f"  {rule_id:<16} {severity:<8} {len(questions_per_rule[rule_id]):>10} "
                  f"{findings_per_rule[rule_id]:>9}")


def _export(args: argparse.Namespace) -> int:
    try:
        data = load_json(args.input)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    all_questions = [question for question in data["questions"] if isinstance(question, Mapping)]
    statuses = None if args.all_statuses else (args.status or ["ready"])
    questions = select_questions(all_questions, statuses, args.easy_only)
    if not questions:
        selection = "all statuses" if statuses is None else ", ".join(sorted({normalize_status(s) for s in statuses}))
        print(f"No questions with [{selection}]{' + easy' if args.easy_only else ''} in {args.input.name} "
              f"({len(all_questions)} questions in the file).", file=sys.stderr)
        return 1

    try:
        xml_text = moodle_xml(questions, wrong_fraction=args.wrong_fraction)
    except ExportError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    output_path = _resolve_output_path(args.output, args.input)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(xml_text, encoding="utf-8")

    if args.verbose:
        by_status = Counter(normalize_status(question.get("status")) for question in all_questions)
        print(f"Exported {len(questions)} of {len(all_questions)} questions to {output_path}")
        print("  in the file: " + ", ".join(f"{status}: {count}" for status, count in sorted(by_status.items())))
    return 0


def _resolve_output_path(output: Path, input_path: Path) -> Path:
    if output == Path(".") or output.is_dir():
        return (Path.cwd() if output == Path(".") else output) / f"{input_path.stem}.xml"
    return output


def _blind(args: argparse.Namespace) -> int:
    try:
        data = load_json(args.input)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if not_objects := [n for n, question in enumerate(data["questions"]) if not isinstance(question, Mapping)]:
        print(f"Error: questions {not_objects} of {args.input} are not JSON objects.", file=sys.stderr)
        return 1

    view, letter_map = blind_view(data["questions"], args.seed)
    _write_json(args.out, view)
    _write_json(args.map, letter_map)
    print(f"Key-less view of {len(view['items'])} questions: {args.out}")
    print(f"Letter map, to keep away from the checker: {args.map}")
    return 0


def _attach_checks(args: argparse.Namespace) -> int:
    try:
        data = load_json(args.input)
        results = json.loads(args.results.read_text(encoding="utf-8"))
        letter_map = json.loads(args.map.read_text(encoding="utf-8")) if args.map else None
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if isinstance(results, Mapping) and results.get("artifact_type") == BLIND_CHECKS:
        if not isinstance(letter_map, Mapping) or letter_map.get("artifact_type") != BLIND_MAP:
            print("Error: steps A and B need --map, the letter map written by `qb blind`.", file=sys.stderr)
            return 1
        problems = attach_blind_checks(data["questions"], results, letter_map)
    else:
        problems = attach_audit_checks(data["questions"], results)
    if problems:
        print(f"Nothing written to {args.input}:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    _write_json(args.input, data)
    checked = [question["checks"] for question in data["questions"] if isinstance(question.get("checks"), Mapping)]
    failed_rules = Counter(failure["rule"] for checks in checked for failure in checks.get("failed", []))
    print(f"{len(results['items'])} checker results merged into {args.input}")
    print("  failures by rule: " + (", ".join(f"{rule} {count}" for rule, count in failed_rules.most_common()) or "none"))
    verdicts = Counter(checks["verdict"] for checks in checked if "verdict" in checks)
    if verdicts:
        stricter = sum(
            1 for checks in checked if isinstance(checks.get("audit"), Mapping)
            and checks["audit"].get("verdict") != checks.get("verdict")
        )
        print("  verdicts: " + ", ".join(f"{verdict} {count}" for verdict, count in sorted(verdicts.items()))
              + f" ({stricter} made stricter than the checker's)")
    return 0


def _calibrate(args: argparse.Namespace) -> int:
    try:
        labelled = load_json(args.labelled)
        if args.step == "prepare":
            copy = unlabelled_copy(labelled)
            _write_json(args.out, copy)
            print(f"{len(copy['questions'])} judged items, without statuses or notes: {args.out}")
            return 0
        report = calibration_report(labelled, load_json(args.checked))
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    summary = report["summary"]
    print(f"{summary['items']} judged items, {summary['audited']} with a verdict")
    for label, target, comparison in (("flawed", args.catch, ">="), ("good", args.false_alarms, "<=")):
        group = summary[label]
        if not group["items"]:
            print(f"  {label} items: none audited")
            continue
        met = group["rate"] >= target if comparison == ">=" else group["rate"] <= target
        print(f"  {label} items flagged: {group['flagged']} of {group['items']} ({group['rate']:.0%}); "
              f"target {comparison} {target:.0%}: {'met' if met else 'NOT met'}")
    results = summary["expected_rules"]
    print(f"  rules the teacher named: {results.get('hit', 0)} found, {results.get('other rule', 0)} caught under "
          f"another rule, {results.get('elsewhere', 0)} found on another option, {results.get('missed', 0)} missed")
    for title, counts in (("missed", summary["missed_by_rule"]), ("false alarms", summary["false_alarms_by_rule"])):
        if counts:
            print(f"  {title}: " + ", ".join(f"{rule} {count}" for rule, count in Counter(counts).most_common()))
    key_found = summary["key_found"]
    print(f"  the blind solver chose the key in {key_found['found']} of {key_found['items']} items")
    if summary["unknown_rules_in_notes"]:
        print(f"  notes name unknown rules: {', '.join(summary['unknown_rules_in_notes'])}")
    print("\n  n  id            label   verdict  rules the teacher named")
    for row in report["items"]:
        expected = "; ".join(_describe_expectation(expectation) for expectation in row["expected"])
        alarms = ", ".join(sorted({alarm["rule"] for alarm in row["errors"]})) if row["label"] == "good" else ""
        print(f"  {row['n']:<2} {row['id']:<13} {row['label']:<7} {row['verdict'] or '-':<8} "
              f"{expected or ('false alarms: ' + alarms if alarms else '')}")
    return 0


def _describe_expectation(expectation: Mapping) -> str:
    """'DIS-TOPIC 6 other rule: DIS-ELEMENTS (A)': the rule, the option, the result and what found it."""
    option = f" {expectation['option']}" if expectation["option"] else ""
    found = f": {'/'.join(expectation['found_rules'])}" if expectation["result"] == "other rule" else ""
    steps = f" ({', '.join(expectation['steps'])})" if expectation["steps"] else ""
    return f"{expectation['rules']}{option} {expectation['result']}{found}{steps}"


def _write_json(path: Path, data: object) -> None:
    """Write through a temporary file in the same folder, so a failure never leaves half a file.

    Temporary files are created owner-only, so the final file takes the mode of the file it replaces, or the
    ordinary mode under the user's umask when it is new.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as handle:
        handle.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.chmod(handle.name, path.stat().st_mode if path.exists() else 0o666 & ~_umask())
    os.replace(handle.name, path)


def _umask() -> int:
    current = os.umask(0)
    os.umask(current)
    return current


if __name__ == "__main__":
    sys.exit(main())
