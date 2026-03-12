"""
Moodle XML Quiz Editor

A Streamlit interface for reviewing and editing Moodle XML quiz files.
Supports marking questions as reviewed, deleting questions, and removing answer distractors.

Run with: streamlit run quiz_editor.py
"""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import streamlit as st

STATE_FILE_SUFFIX = ".review_state.txt"


@dataclass
class Answer:
    text: str
    fraction: str
    feedback: str
    format: str = "html"


@dataclass
class Question:
    name: str
    question_text: str
    general_feedback: str
    answers: list[Answer] = field(default_factory=list)
    default_grade: str = "1.0000000"
    penalty: str = "0.5000000"
    single: str = "true"
    shuffle_answers: str = "true"
    answer_numbering: str = "abc"
    correct_feedback: str = "<p>Correcto.</p>"
    partially_correct_feedback: str = "<p>Parcialmente correcto.</p>"
    incorrect_feedback: str = "<p>Incorrecto.</p>"
    reviewed: bool = False
    original_index: int = 0


@dataclass
class Category:
    path: str
    info: str = ""


def extract_cdata_content(text: str | None) -> str:
    if text is None:
        return ""
    return text


def clean_html_for_display(html: str) -> str:
    """Remove HTML tags for cleaner display preview."""
    clean = re.sub(r"<[^>]+>", "", html)
    clean = clean.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">")
    clean = clean.replace("&amp;", "&").replace("&quot;", '"')
    return clean.strip()


def parse_xml(xml_path: Path) -> tuple[Category | None, list[Question]]:
    """Parse Moodle XML file and return category and questions."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    category = None
    questions: list[Question] = []
    question_index = 0

    for q_elem in root.findall("question"):
        q_type = q_elem.get("type")

        if q_type == "category":
            cat_elem = q_elem.find("category/text")
            info_elem = q_elem.find("info/text")
            category = Category(
                path=cat_elem.text if cat_elem is not None and cat_elem.text else "",
                info=info_elem.text if info_elem is not None and info_elem.text else "",
            )

        elif q_type == "multichoice":
            name_elem = q_elem.find("name/text")
            qtext_elem = q_elem.find("questiontext/text")
            feedback_elem = q_elem.find("generalfeedback/text")

            answers: list[Answer] = []
            for ans_elem in q_elem.findall("answer"):
                ans_text_elem = ans_elem.find("text")
                ans_feedback_elem = ans_elem.find("feedback/text")
                answers.append(
                    Answer(
                        text=extract_cdata_content(ans_text_elem.text if ans_text_elem is not None else ""),
                        fraction=ans_elem.get("fraction", "0"),
                        feedback=extract_cdata_content(ans_feedback_elem.text if ans_feedback_elem is not None else ""),
                        format=ans_elem.get("format", "html"),
                    )
                )

            single_elem = q_elem.find("single")
            shuffle_elem = q_elem.find("shuffleanswers")
            numbering_elem = q_elem.find("answernumbering")
            grade_elem = q_elem.find("defaultgrade")
            penalty_elem = q_elem.find("penalty")
            correct_fb = q_elem.find("correctfeedback/text")
            partial_fb = q_elem.find("partiallycorrectfeedback/text")
            incorrect_fb = q_elem.find("incorrectfeedback/text")

            question = Question(
                name=name_elem.text if name_elem is not None and name_elem.text else f"Question {question_index + 1}",
                question_text=extract_cdata_content(qtext_elem.text if qtext_elem is not None else ""),
                general_feedback=extract_cdata_content(feedback_elem.text if feedback_elem is not None else ""),
                answers=answers,
                default_grade=grade_elem.text if grade_elem is not None and grade_elem.text else "1.0000000",
                penalty=penalty_elem.text if penalty_elem is not None and penalty_elem.text else "0.5000000",
                single=single_elem.text if single_elem is not None and single_elem.text else "true",
                shuffle_answers=shuffle_elem.text if shuffle_elem is not None and shuffle_elem.text else "true",
                answer_numbering=numbering_elem.text if numbering_elem is not None and numbering_elem.text else "abc",
                correct_feedback=correct_fb.text if correct_fb is not None and correct_fb.text else "<![CDATA[<p>Correcto.</p>]]>",
                partially_correct_feedback=partial_fb.text if partial_fb is not None and partial_fb.text else "<![CDATA[<p>Parcialmente correcto.</p>]]>",
                incorrect_feedback=incorrect_fb.text if incorrect_fb is not None and incorrect_fb.text else "<![CDATA[<p>Incorrecto.</p>]]>",
                original_index=question_index,
            )
            questions.append(question)
            question_index += 1

    return category, questions


def wrap_cdata(text: str) -> str:
    """Wrap text in CDATA. Always wraps since ET strips CDATA on parse."""
    if not text:
        return "<![CDATA[]]>"
    # ET strips CDATA markers when parsing, so we always need to re-add them
    # But avoid double-wrapping if text somehow still has markers
    if text.startswith("<![CDATA[") and text.endswith("]]>"):
        return text
    return f"<![CDATA[{text}]]>"


def generate_xml(category: Category | None, questions: list[Question]) -> str:
    """Generate Moodle XML from category and questions."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]

    if category:
        lines.extend([
            "<!-- category -->",
            '  <question type="category">',
            "    <category>",
            f"      <text>{category.path}</text>",
            "    </category>",
            '    <info format="html">',
            f"      <text>{category.info}</text>",
            "    </info>",
            "    <idnumber></idnumber>",
            "  </question>",
            "",
        ])

    for i, q in enumerate(questions, 1):
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


def load_review_state(xml_path: Path) -> set[str]:
    """Load reviewed question names from state file."""
    state_file = xml_path.with_suffix(xml_path.suffix + STATE_FILE_SUFFIX)
    if state_file.exists():
        return set(state_file.read_text().strip().split("\n")) - {""}
    return set()


def save_review_state(xml_path: Path, reviewed_names: set[str]) -> None:
    """Save reviewed question names to state file."""
    state_file = xml_path.with_suffix(xml_path.suffix + STATE_FILE_SUFFIX)
    state_file.write_text("\n".join(sorted(reviewed_names)))


def render_question_card(
    q: Question, idx: int, prefix: str, is_reviewed: bool
) -> tuple[bool, bool, list[int]]:
    """
    Render a question card and return actions taken.
    Returns: (toggle_review, delete_question, answers_to_delete)
    """
    toggle_review = False
    delete_question = False
    answers_to_delete: list[int] = []

    correct_count = sum(1 for a in q.answers if a.fraction == "100")
    wrong_count = len(q.answers) - correct_count

    with st.container(border=True):
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            status_icon = "✅" if is_reviewed else "⏳"
            st.markdown(f"**{status_icon} Q{q.original_index + 1}: {q.name}**")

        with col2:
            review_label = "Unreview" if is_reviewed else "Review ✓"
            if st.button(review_label, key=f"{prefix}_review_{idx}", use_container_width=True):
                toggle_review = True

        with col3:
            if st.button("🗑️ Delete", key=f"{prefix}_delete_{idx}", use_container_width=True, type="secondary"):
                delete_question = True

        if is_reviewed:
            with st.expander("Show details", expanded=False):
                st.markdown(q.question_text, unsafe_allow_html=True)
                st.caption(f"Answers: {correct_count} correct, {wrong_count} distractors")
        else:
            st.markdown(q.question_text, unsafe_allow_html=True)

            if q.general_feedback:
                with st.expander("📝 General Feedback"):
                    st.markdown(q.general_feedback, unsafe_allow_html=True)

            st.markdown("**Answers:**")
            for ans_idx, ans in enumerate(q.answers):
                is_correct = ans.fraction == "100"
                icon = "✅" if is_correct else "❌"

                ans_col1, ans_col2 = st.columns([10, 1])

                with ans_col1:
                    clean_text = clean_html_for_display(ans.text)[:200]
                    if is_correct:
                        st.success(f"{icon} {clean_text}")
                    else:
                        st.error(f"{icon} [{ans.fraction}%] {clean_text}")

                with ans_col2:
                    if not is_correct:
                        if st.button("🗑️", key=f"{prefix}_ans_{idx}_{ans_idx}", help="Delete this distractor"):
                            answers_to_delete.append(ans_idx)

    return toggle_review, delete_question, answers_to_delete


def main() -> None:
    st.set_page_config(page_title="Moodle Quiz Editor", page_icon="📝", layout="wide")

    st.title("📝 Moodle XML Quiz Editor")
    st.markdown("Review questions, delete distractors, and export clean XML files.")

    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.category = None
        st.session_state.xml_path = None
        st.session_state.reviewed_names = set()

    with st.sidebar:
        st.header("📂 Load XML File")

        xml_path_input = st.text_input(
            "XML File Path",
            value=str(Path(__file__).parent / "comprehensive_exam.xml"),
            help="Enter the full path to your Moodle XML file",
        )

        if st.button("Load File", type="primary", use_container_width=True):
            xml_path = Path(xml_path_input)
            if xml_path.exists() and xml_path.suffix == ".xml":
                category, questions = parse_xml(xml_path)
                reviewed_names = load_review_state(xml_path)

                for q in questions:
                    q.reviewed = q.name in reviewed_names

                st.session_state.questions = questions
                st.session_state.category = category
                st.session_state.xml_path = xml_path
                st.session_state.reviewed_names = reviewed_names
                st.success(f"Loaded {len(questions)} questions")
                st.rerun()
            else:
                st.error("File not found or not an XML file")

        st.divider()

        if st.session_state.questions:
            reviewed = [q for q in st.session_state.questions if q.reviewed]
            pending = [q for q in st.session_state.questions if not q.reviewed]

            st.metric("Total Questions", len(st.session_state.questions))
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Reviewed", len(reviewed))
            with col2:
                st.metric("⏳ Pending", len(pending))

            st.divider()

            if st.button("💾 Save XML", type="primary", use_container_width=True):
                xml_content = generate_xml(st.session_state.category, st.session_state.questions)
                st.session_state.xml_path.write_text(xml_content, encoding="utf-8")
                save_review_state(st.session_state.xml_path, st.session_state.reviewed_names)
                st.success("Saved!")

            st.download_button(
                "⬇️ Download XML",
                data=generate_xml(st.session_state.category, st.session_state.questions),
                file_name=st.session_state.xml_path.name if st.session_state.xml_path else "quiz.xml",
                mime="application/xml",
                use_container_width=True,
            )

            if st.button("🔄 Reload from Disk", use_container_width=True):
                if st.session_state.xml_path:
                    category, questions = parse_xml(st.session_state.xml_path)
                    reviewed_names = load_review_state(st.session_state.xml_path)
                    for q in questions:
                        q.reviewed = q.name in reviewed_names
                    st.session_state.questions = questions
                    st.session_state.category = category
                    st.session_state.reviewed_names = reviewed_names
                    st.rerun()

    if not st.session_state.questions:
        st.info("👈 Load an XML file from the sidebar to get started.")
        return

    reviewed_questions = [q for q in st.session_state.questions if q.reviewed]
    pending_questions = [q for q in st.session_state.questions if not q.reviewed]

    if reviewed_questions:
        st.header(f"✅ Reviewed Questions ({len(reviewed_questions)})")

        for idx, q in enumerate(reviewed_questions):
            toggle, delete, del_answers = render_question_card(q, idx, "reviewed", is_reviewed=True)

            if toggle:
                q.reviewed = False
                st.session_state.reviewed_names.discard(q.name)
                save_review_state(st.session_state.xml_path, st.session_state.reviewed_names)
                st.rerun()

            if delete:
                st.session_state.questions.remove(q)
                st.session_state.reviewed_names.discard(q.name)
                save_review_state(st.session_state.xml_path, st.session_state.reviewed_names)
                st.rerun()

            if del_answers:
                for ans_idx in sorted(del_answers, reverse=True):
                    q.answers.pop(ans_idx)
                st.rerun()

    st.header(f"⏳ Pending Questions ({len(pending_questions)})")

    if not pending_questions:
        st.success("🎉 All questions have been reviewed!")
    else:
        for idx, q in enumerate(pending_questions):
            toggle, delete, del_answers = render_question_card(q, idx, "pending", is_reviewed=False)

            if toggle:
                q.reviewed = True
                st.session_state.reviewed_names.add(q.name)
                save_review_state(st.session_state.xml_path, st.session_state.reviewed_names)
                st.rerun()

            if delete:
                st.session_state.questions.remove(q)
                st.rerun()

            if del_answers:
                for ans_idx in sorted(del_answers, reverse=True):
                    q.answers.pop(ans_idx)
                st.rerun()


if __name__ == "__main__":
    main()
