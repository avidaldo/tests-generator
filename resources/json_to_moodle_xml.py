#!/usr/bin/env python3
"""
Convert a quiz editor JSON state file to Moodle XML.

Reads the JSON format produced by the quiz editor (editor/v3/file_io/state_io.py)
and outputs Moodle-compatible multichoice XML. By default only exports questions
with status "lista" (approved by the human reviewer), which is the intended
pipeline step after human review in the editor.

Usage:
    json_to_moodle_xml.py <input.json> <output.xml>
    json_to_moodle_xml.py <input.json> <output.xml> --status lista revisar
    json_to_moodle_xml.py <input.json> <output.xml> --all-statuses
    json_to_moodle_xml.py <input.json> . --verbose

Examples:
    # Export only approved questions (default)
    json_to_moodle_xml.py session.json exam.xml

    # Export approved + under-review questions
    json_to_moodle_xml.py session.json exam.xml --status lista revisar

    # Export everything regardless of review status
    json_to_moodle_xml.py session.json exam.xml --all-statuses

    # Auto-name output in current directory, with verbose logging
    json_to_moodle_xml.py session.json . --verbose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


_VALID_STATUSES = {"pendiente", "revisar", "lista"}
_DEFAULT_STATUSES = {"lista"}


def _wrap_cdata(text: str) -> str:
    if not text:
        return "<![CDATA[]]>"
    if text.startswith("<![CDATA[") and text.endswith("]]>"):
        return text
    return f"<![CDATA[{text}]]>"


def _generate_xml(questions: list[dict]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]

    # Group by category, preserving insertion order
    questions_by_category: dict[str, list[dict]] = {}
    for q in questions:
        cat = q.get("category_path") or "Uncategorized"
        if cat not in questions_by_category:
            questions_by_category[cat] = []
        questions_by_category[cat].append(q)

    for cat_path, cat_questions in questions_by_category.items():
        if cat_path != "Uncategorized":
            lines.extend([
                '  <question type="category">',
                "    <category>",
                f"      <text>{cat_path}</text>",
                "    </category>",
                '    <info format="html"><text></text></info>',
                "    <idnumber></idnumber>",
                "  </question>",
            ])

        for q in cat_questions:
            name = q.get("name", "")
            question_text = q.get("question_text", "")
            general_feedback = q.get("general_feedback", "")
            default_grade = q.get("default_grade", "1.0000000")
            penalty = q.get("penalty", "0.0000000")
            single = q.get("single", "true")
            shuffle_answers = q.get("shuffle_answers", "true")
            answer_numbering = q.get("answer_numbering", "abc")
            correct_feedback = q.get("correct_feedback", "<p>Correcto.</p>")
            partially_correct_feedback = q.get("partially_correct_feedback", "<p>Parcialmente correcto.</p>")
            incorrect_feedback = q.get("incorrect_feedback", "<p>Incorrecto.</p>")

            lines.extend([
                '  <question type="multichoice">',
                f"    <name><text>{name}</text></name>",
                f'    <questiontext format="html"><text>{_wrap_cdata(question_text)}</text></questiontext>',
                f'    <generalfeedback format="html"><text>{_wrap_cdata(general_feedback)}</text></generalfeedback>',
                f"    <defaultgrade>{default_grade}</defaultgrade>",
                f"    <penalty>{penalty}</penalty>",
                "    <hidden>0</hidden>",
                "    <idnumber></idnumber>",
                f"    <single>{single}</single>",
                f"    <shuffleanswers>{shuffle_answers}</shuffleanswers>",
                f"    <answernumbering>{answer_numbering}</answernumbering>",
                "    <showstandardinstruction>0</showstandardinstruction>",
                f'    <correctfeedback format="html"><text>{_wrap_cdata(correct_feedback)}</text></correctfeedback>',
                f'    <partiallycorrectfeedback format="html">'
                f'<text>{_wrap_cdata(partially_correct_feedback)}</text></partiallycorrectfeedback>',
                f'    <incorrectfeedback format="html"><text>{_wrap_cdata(incorrect_feedback)}</text></incorrectfeedback>',
                "    <shownumcorrect/>",
            ])

            for ans in q.get("answers", []):
                fraction = ans.get("fraction", "-50")
                fmt = ans.get("format", "html")
                text = ans.get("text", "")
                feedback = ans.get("feedback", "")
                lines.extend([
                    f'    <answer fraction="{fraction}" format="{fmt}">',
                    f"      <text>{_wrap_cdata(text)}</text>",
                    f'      <feedback format="html"><text>{_wrap_cdata(feedback)}</text></feedback>',
                    "    </answer>",
                ])

            lines.append("  </question>")

    lines.append("</quiz>")
    return "\n".join(lines)


def _resolve_output_path(output_arg: Path, input_path: Path) -> Path:
    """Resolve output path; '.' generates a name from the input filename."""
    if output_arg == Path("."):
        return Path.cwd() / (input_path.stem + ".xml")
    if output_arg.is_dir():
        return output_arg / (input_path.stem + ".xml")
    return output_arg


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a quiz editor JSON state file to Moodle XML. "
            "By default exports only questions with status 'lista' (human-approved)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Status values:
  pendiente  Not yet reviewed (default for newly generated questions)
  revisar    Flagged for revision
  lista      Approved — ready for students

By default only 'lista' questions are exported. Use --all-statuses to override.
""",
    )
    parser.add_argument("input", type=Path, help="Input JSON state file.")
    parser.add_argument(
        "output",
        type=Path,
        help="Output XML file, directory, or '.' for auto-named file in current directory.",
    )
    status_group = parser.add_mutually_exclusive_group()
    status_group.add_argument(
        "--status",
        nargs="+",
        choices=sorted(_VALID_STATUSES),
        default=None,
        metavar="STATUS",
        help="Export questions with these statuses (space-separated). Default: lista",
    )
    status_group.add_argument(
        "--all-statuses",
        action="store_true",
        help="Export all questions regardless of status.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Print export summary.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    all_questions = data.get("questions", [])

    if args.all_statuses:
        selected_statuses = _VALID_STATUSES
    elif args.status:
        selected_statuses = set(args.status)
    else:
        selected_statuses = _DEFAULT_STATUSES

    questions = [q for q in all_questions if q.get("status", "pendiente") in selected_statuses]

    if not questions:
        status_label = ", ".join(sorted(selected_statuses))
        print(
            f"No questions with status [{status_label}] found in {input_path.name}. "
            f"Total questions in file: {len(all_questions)}.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = _resolve_output_path(args.output, input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    xml_content = _generate_xml(questions)
    output_path.write_text(xml_content, encoding="utf-8")

    if args.verbose:
        by_status: dict[str, int] = {}
        for q in all_questions:
            s = q.get("status", "pendiente")
            by_status[s] = by_status.get(s, 0) + 1

        status_summary = ", ".join(f"{s}: {n}" for s, n in sorted(by_status.items()))
        print(f"Input : {input_path.name} ({len(all_questions)} total — {status_summary})")
        print(f"Filter: {', '.join(sorted(selected_statuses))}")
        print(f"Output: {output_path} ({len(questions)} questions)")
    else:
        print(f"Exported {len(questions)} question(s) → {output_path}")


if __name__ == "__main__":
    main()
