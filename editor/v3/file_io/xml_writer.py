"""
XML Writer for Moodle Quiz format.
"""

from collections.abc import Sequence
from models.question import Question


def wrap_cdata(text: str) -> str:
    if not text:
        return "<![CDATA[]]>"
    if text.startswith("<![CDATA[") and text.endswith("]]>"):
        return text
    return f"<![CDATA[{text}]]>"


def generate_xml(questions: Sequence[Question]) -> str:
    """Generate Moodle XML from questions, grouped by category."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    
    questions_by_category: dict[str, list[Question]] = {}
    for q in questions:
        cat_path = q.category_path or "Uncategorized"
        if cat_path not in questions_by_category:
            questions_by_category[cat_path] = []
        questions_by_category[cat_path].append(q)
    
    for cat_path in sorted(questions_by_category.keys()):
        cat_questions = questions_by_category[cat_path]
        
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
            lines.extend([
                '  <question type="multichoice">',
                f"    <name><text>{q.name}</text></name>",
                f'    <questiontext format="html"><text>{wrap_cdata(q.question_text)}</text></questiontext>',
                f'    <generalfeedback format="html"><text>{wrap_cdata(q.general_feedback)}</text></generalfeedback>',
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
            
            for ans in q.answers:
                lines.extend([
                    f'    <answer fraction="{ans.fraction}" format="{ans.format}">',
                    f"      <text>{wrap_cdata(ans.text)}</text>",
                    f'      <feedback format="html"><text>{wrap_cdata(ans.feedback)}</text></feedback>',
                    "    </answer>",
                ])
            
            lines.append("  </question>")
    
    lines.append("</quiz>")
    return "\n".join(lines)
