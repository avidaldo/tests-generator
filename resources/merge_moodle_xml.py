#!/usr/bin/env python3
"""
Merge Moodle quiz XML files recursively from a root directory into a single output file.

Preserves CDATA sections and original formatting by using string manipulation rather than
XML parsing. Categories are kept ordered based on their first appearance in source files.

Usage:
    merge_moodle_xml.py <root_path> <output_path> [--include-source-comments] [--verbose]

Examples:
    merge_moodle_xml.py ./questions merged.xml
    merge_moodle_xml.py /path/to/questions . --include-source-comments
    merge_moodle_xml.py ./questions ./output/all_questions.xml --verbose
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _extract_quiz_inner(xml_text: str, *, source: Path) -> str:
    """Extract the inner content of a <quiz> element, preserving exact formatting."""
    lower = xml_text.lower()

    quiz_open_index = lower.find("<quiz")
    if quiz_open_index == -1:
        raise ValueError(f"{source}: missing <quiz> root")

    quiz_open_end = lower.find(">", quiz_open_index)
    if quiz_open_end == -1:
        raise ValueError(f"{source}: malformed <quiz ...> opening tag")

    quiz_close_index = lower.rfind("</quiz>")
    if quiz_close_index == -1:
        raise ValueError(f"{source}: missing </quiz> closing tag")

    if quiz_close_index <= quiz_open_end:
        raise ValueError(f"{source}: malformed <quiz> section")

    inner = xml_text[quiz_open_end + 1:quiz_close_index]
    return inner.strip("\n")


def find_xml_files_recursive(root_path: Path) -> list[Path]:
    """Recursively find all *.xml files under root_path, sorted alphabetically by relative path."""
    if not root_path.exists():
        raise FileNotFoundError(f"Root path does not exist: {root_path}")

    if root_path.is_file():
        if root_path.suffix.lower() == ".xml":
            return [root_path]
        raise ValueError(f"Root path is a file but not XML: {root_path}")

    xml_files = sorted(root_path.rglob("*.xml"), key=lambda p: str(p.relative_to(root_path)))
    return xml_files


def merge_moodle_quiz_xml(inputs: list[Path], *, include_source_comments: bool, verbose: bool = False) -> str:
    """Merge multiple Moodle XML files into a single XML string."""
    merged_chunks: list[str] = []

    for path in inputs:
        try:
            xml_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            xml_text = path.read_text(encoding="latin-1")

        try:
            inner = _extract_quiz_inner(xml_text, source=path)
        except ValueError as e:
            if verbose:
                print(f"Skipping {path}: {e}", file=sys.stderr)
            continue

        if not inner.strip():
            if verbose:
                print(f"Skipping {path}: empty content", file=sys.stderr)
            continue

        if include_source_comments:
            safe_name = str(path)
            safe_name = safe_name.replace("--", "- -")
            merged_chunks.append(f"<!-- source: {safe_name} -->")

        merged_chunks.append(inner)

        if verbose:
            print(f"Merged: {path}")

    body = "\n\n".join(merged_chunks).strip("\n")
    if body:
        body = "\n" + body + "\n"

    return '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>' + body + "</quiz>\n"


def _resolve_output_path(output_arg: Path, root_path: Path) -> Path:
    """Resolve the output path, handling '.' as current directory with default filename."""
    if output_arg == Path("."):
        default_name = f"{root_path.name}_merged.xml"
        return Path.cwd() / default_name

    if output_arg.is_dir() or (not output_arg.suffix and not output_arg.exists()):
        output_arg.mkdir(parents=True, exist_ok=True)
        default_name = f"{root_path.name}_merged.xml"
        return output_arg / default_name

    return output_arg


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recursively merge Moodle quiz XML files from a root directory into a single file. "
            "Categories and questions are preserved in alphabetical order by source file path."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./questions merged.xml
      Merge all XML files under ./questions into merged.xml

  %(prog)s /path/to/questions .
      Merge all XML files into current directory with auto-generated name

  %(prog)s ./questions ./output/ --include-source-comments
      Merge into output directory, adding source file comments

  %(prog)s ./questions output.xml --verbose
      Merge with verbose output showing each file processed
""",
    )
    parser.add_argument(
        "root_path",
        type=Path,
        help="Root directory to search for XML files recursively (or a single XML file).",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Output path. Can be a file, directory, or '.' for current directory with auto-generated name.",
    )
    parser.add_argument(
        "--include-source-comments",
        action="store_true",
        help="Insert XML comments before each merged chunk identifying its source file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print each file as it's processed.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    root_path = args.root_path.resolve()

    xml_files = find_xml_files_recursive(root_path)

    if not xml_files:
        print(f"No XML files found under: {root_path}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Found {len(xml_files)} XML file(s) under {root_path}")

    output_path = _resolve_output_path(args.output, root_path)

    merged = merge_moodle_quiz_xml(xml_files, include_source_comments=args.include_source_comments, verbose=args.verbose)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(merged, encoding="utf-8")

    print(f"Merged {len(xml_files)} file(s) -> {output_path}")


if __name__ == "__main__":
    main()
