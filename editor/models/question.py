"""
Moodle Quiz Editor v3 - Data Models

Dataclasses for Question, Answer, and Category.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import uuid


class QuestionStatus(Enum):
    """Question review status."""
    PENDIENTE = "pendiente"  # Newly imported, not yet seen
    REVISAR = "revisar"       # Seen but needs further review
    LISTA = "lista"           # Approved and ready for exam


@dataclass
class Answer:
    """Represents an answer option in a multichoice question."""
    text: str
    fraction: str  # "100" for correct, negative for incorrect
    feedback: str = ""
    format: str = "html"

    @property
    def is_correct(self) -> bool:
        try:
            return float(self.fraction) >= 100
        except ValueError:
            return False


@dataclass
class Question:
    """Represents a Moodle multichoice question."""
    id: str
    name: str
    question_text: str
    general_feedback: str
    category_path: str
    answers: list[Answer] = field(default_factory=list)
    status: QuestionStatus = QuestionStatus.PENDIENTE

    # Moodle-specific fields
    default_grade: str = "1.0000000"
    penalty: str = "0.0000000"
    single: str = "true"
    shuffle_answers: str = "true"
    answer_numbering: str = "abc"
    correct_feedback: str = "<p>Correcto.</p>"
    partially_correct_feedback: str = "<p>Parcialmente correcto.</p>"
    incorrect_feedback: str = "<p>Incorrecto.</p>"
    source_file: str = ""
    source_ref: str = ""
    origin_kind: str = ""
    origin_path: str = ""
    origin_question_id: str = ""
    generated_by_model: str = ""
    is_easy: bool = False

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())[:8]

    @property
    def category_name(self) -> str:
        parts = self.category_path.split("/")
        return parts[-1] if parts else "Sin categoría"

    @property
    def correct_count(self) -> int:
        return sum(1 for a in self.answers if a.is_correct)

    @property
    def wrong_count(self) -> int:
        return len(self.answers) - self.correct_count

    @property
    def source_label(self) -> str:
        if self.origin_path:
            return Path(self.origin_path).name
        if self.source_file:
            return self.source_file
        return self.source_ref

    @property
    def import_key(self) -> tuple[str, str]:
        if self.origin_path and self.origin_question_id:
            return (self.origin_path, self.origin_question_id)
        if self.origin_path:
            return (self.origin_path, self.id)
        return ("", self.name)


@dataclass
class Category:
    """Represents a Moodle category."""
    path: str
    info: str = ""

    @property
    def name(self) -> str:
        parts = self.path.split("/")
        return parts[-1] if parts else ""
