"""
XML Writer for Moodle Quiz format.

Generates valid Moodle XML from Question/Answer dataclass instances.
"""

from collections.abc import Sequence

from models.question import Question, Category


def wrap_cdata(text: str) -> str:
    """Wrap text in CDATA. Always wraps since ET strips CDATA on parse."""
    if not text:
        return "<![CDATA[]]>"
    # Avoid double-wrapping
    if text.startswith("<![CDATA[") and text.endswith("]]>"):
        return text
    return f"<![CDATA[{text}]]>"


def generate_xml(questions: Sequence[Question], include_categories: bool = True) -> str:
    """
    Generate Moodle XML from questions.
    
    Groups questions by category and outputs category headers.
    
    Args:
        questions: Sequence of Question objects
        include_categories: Whether to include category definitions
        
    Returns:
        Valid Moodle XML string
    """
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    
    # Group questions by category
    questions_by_category: dict[str, list[Question]] = {}
    for q in questions:
        cat_path = q.category_path or "Uncategorized"
        if cat_path not in questions_by_category:
            questions_by_category[cat_path] = []
        questions_by_category[cat_path].append(q)
    
    # Output each category with its questions
    for cat_path in sorted(questions_by_category.keys()):
        cat_questions = questions_by_category[cat_path]
        
        if include_categories and cat_path != "Uncategorized":
            # Category header
            lines.extend([
                "<!-- category -->",
                '  <question type="category">',
                "    <category>",
                f"      <text>{cat_path}</text>",
                "    </category>",
                '    <info format="html">',
                "      <text></text>",
                "    </info>",
                "    <idnumber></idnumber>",
                "  </question>",
                "",
            ])
        
        # Questions in this category
        for i, q in enumerate(cat_questions, 1):
            lines.append(f"<!-- Q{i}: {q.name} -->")
            lines.extend([
                '  <question type="multichoice">',
                "    <name>",
                f"      <text>{q.name}</text>",
                "    </name>",
                '    <questiontext format="html">',
                f"      <text>{wrap_cdata(q.question_text)}</text>",
                "    </questiontext>",
                '    <generalfeedback format="html">',
                f"      <text>{wrap_cdata(q.general_feedback)}</text>",
                "    </generalfeedback>",
                f"    <defaultgrade>{q.default_grade}</defaultgrade>",
                f"    <penalty>{q.penalty}</penalty>",
                "    <hidden>0</hidden>",
                "    <idnumber></idnumber>",
                f"    <single>{q.single}</single>",
                f"    <shuffleanswers>{q.shuffle_answers}</shuffleanswers>",
                f"    <answernumbering>{q.answer_numbering}</answernumbering>",
                "    <showstandardinstruction>0</showstandardinstruction>",
                f'    <correctfeedback format="html"><text>{wrap_cdata(q.correct_feedback)}</text></correctfeedback>',
                f'    <partiallycorrectfeedback format="html"><text>{wrap_cdata(q.partially_correct_feedback)}</text></partiallycorrectfeedback>',
                f'    <incorrectfeedback format="html"><text>{wrap_cdata(q.incorrect_feedback)}</text></incorrectfeedback>',
                "    <shownumcorrect/>",
            ])
            
            # Answers
            for ans in q.answers:
                lines.extend([
                    f'    <answer fraction="{ans.fraction}" format="{ans.format}">',
                    f"      <text>{wrap_cdata(ans.text)}</text>",
                    f'      <feedback format="html"><text>{wrap_cdata(ans.feedback)}</text></feedback>',
                    "    </answer>",
                ])
            
            lines.extend(["  </question>", ""])
    
    lines.append("</quiz>")
    return "\n".join(lines)


def write_xml_file(questions: Sequence[Question], output_path: str) -> None:
    """
    Write questions to an XML file.
    
    Args:
        questions: Sequence of Question objects
        output_path: Path to write the XML file
    """
    xml_content = generate_xml(questions)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
