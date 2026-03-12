"""
Data models for Moodle Quiz Editor.

Defines Question, Answer, Category dataclasses that represent Moodle XML quiz structure.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal
import uuid


class QuestionStatus(Enum):
    """Question review status."""
    LISTA = "lista"
    REVISAR = "revisar"


@dataclass
class Answer:
    """Represents an answer option in a multichoice question."""
    text: str
    fraction: str  # "100" for correct, negative for incorrect
    feedback: str = ""
    format: str = "html"
    
    @property
    def is_correct(self) -> bool:
        """Check if this is a correct answer (fraction >= 100)."""
        try:
            return float(self.fraction) >= 100
        except ValueError:
            return False


@dataclass
class Question:
    """Represents a Moodle multichoice question."""
    id: str  # Unique ID for tracking (UUID)
    name: str
    question_text: str
    general_feedback: str
    category_path: str  # e.g., "$course$/top/CSPy/Examen CSPy/Git"
    answers: list[Answer] = field(default_factory=list)
    status: QuestionStatus = QuestionStatus.REVISAR
    
    # Moodle-specific fields with sensible defaults
    default_grade: str = "1.0000000"
    penalty: str = "0.5000000"
    single: str = "true"
    shuffle_answers: str = "true"
    answer_numbering: str = "abc"
    correct_feedback: str = "<p>Correcto.</p>"
    partially_correct_feedback: str = "<p>Parcialmente correcto.</p>"
    incorrect_feedback: str = "<p>Incorrecto.</p>"
    
    # Source tracking for multi-file import
    source_file: str = ""
    
    @staticmethod
    def generate_id() -> str:
        """Generate a unique question ID."""
        return str(uuid.uuid4())[:8]
    
    @property
    def category_name(self) -> str:
        """Get the leaf category name (last segment of path)."""
        parts = self.category_path.split("/")
        return parts[-1] if parts else "Sin categoría"
    
    @property
    def correct_count(self) -> int:
        """Count correct answers."""
        return sum(1 for a in self.answers if a.is_correct)
    
    @property
    def wrong_count(self) -> int:
        """Count wrong answers."""
        return len(self.answers) - self.correct_count


@dataclass
class Category:
    """Represents a Moodle category (question grouping)."""
    path: str  # Full path like "$course$/top/CSPy/Examen CSPy/Git"
    info: str = ""
    
    @property
    def name(self) -> str:
        """Get the leaf category name."""
        parts = self.path.split("/")
        return parts[-1] if parts else ""
    
    @property 
    def depth(self) -> int:
        """Get the nesting depth of this category."""
        return self.path.count("/")
