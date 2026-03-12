"""
QuizStore: Centralized state management with undo/redo support.

Uses the Command pattern to track all mutations, enabling full undo/redo functionality.
"""

from dataclasses import dataclass, field
from typing import Callable
from collections.abc import Sequence
import json
from pathlib import Path
import copy

from models.question import Question, Answer, QuestionStatus, Category


# --- Command Pattern for Undo/Redo ---

@dataclass
class Command:
    """Base class for undoable commands."""
    description: str
    
    def execute(self, store: "QuizStore") -> None:
        """Execute the command."""
        raise NotImplementedError
    
    def undo(self, store: "QuizStore") -> None:
        """Undo the command."""
        raise NotImplementedError


@dataclass
class DeleteQuestionCommand(Command):
    """Command to delete a question."""
    question_id: str
    _deleted_question: Question | None = field(default=None, repr=False)
    _deleted_index: int = -1
    
    def execute(self, store: "QuizStore") -> None:
        for i, q in enumerate(store._questions):
            if q.id == self.question_id:
                self._deleted_question = q
                self._deleted_index = i
                store._questions.pop(i)
                return
    
    def undo(self, store: "QuizStore") -> None:
        if self._deleted_question is not None:
            store._questions.insert(self._deleted_index, self._deleted_question)


@dataclass  
class UpdateQuestionCommand(Command):
    """Command to update question fields."""
    question_id: str
    field_name: str
    new_value: str | QuestionStatus
    _old_value: str | QuestionStatus | None = field(default=None, repr=False)
    
    def execute(self, store: "QuizStore") -> None:
        for q in store._questions:
            if q.id == self.question_id:
                self._old_value = getattr(q, self.field_name)
                setattr(q, self.field_name, self.new_value)
                return
    
    def undo(self, store: "QuizStore") -> None:
        for q in store._questions:
            if q.id == self.question_id:
                setattr(q, self.field_name, self._old_value)
                return


@dataclass
class DeleteAnswerCommand(Command):
    """Command to delete an answer from a question."""
    question_id: str
    answer_index: int
    _deleted_answer: Answer | None = field(default=None, repr=False)
    
    def execute(self, store: "QuizStore") -> None:
        for q in store._questions:
            if q.id == self.question_id:
                if 0 <= self.answer_index < len(q.answers):
                    self._deleted_answer = q.answers.pop(self.answer_index)
                return
    
    def undo(self, store: "QuizStore") -> None:
        if self._deleted_answer is not None:
            for q in store._questions:
                if q.id == self.question_id:
                    q.answers.insert(self.answer_index, self._deleted_answer)
                    return


@dataclass
class ToggleStatusCommand(Command):
    """Command to toggle question status between Lista and Revisar."""
    question_id: str
    _old_status: QuestionStatus | None = field(default=None, repr=False)
    
    def execute(self, store: "QuizStore") -> None:
        for q in store._questions:
            if q.id == self.question_id:
                self._old_status = q.status
                q.status = (QuestionStatus.LISTA 
                           if q.status == QuestionStatus.REVISAR 
                           else QuestionStatus.REVISAR)
                return
    
    def undo(self, store: "QuizStore") -> None:
        if self._old_status is not None:
            for q in store._questions:
                if q.id == self.question_id:
                    q.status = self._old_status
                    return


# --- Main Store ---

class QuizStore:
    """
    Centralized state management for quiz questions.
    
    Supports:
    - Multi-file import with source tracking
    - Undo/redo via command pattern
    - Category-based filtering
    - JSON persistence
    """
    
    MAX_UNDO_HISTORY = 100
    
    def __init__(self) -> None:
        self._questions: list[Question] = []
        self._categories: dict[str, Category] = {}  # path -> Category
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []
        self._listeners: list[Callable[[], None]] = []
        self._dirty: bool = False
    
    # --- Properties ---
    
    @property
    def questions(self) -> Sequence[Question]:
        """Read-only access to questions."""
        return self._questions
    
    @property
    def categories(self) -> list[str]:
        """Get sorted list of unique category paths."""
        return sorted(set(q.category_path for q in self._questions))
    
    @property
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0
    
    @property
    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0
    
    @property
    def is_dirty(self) -> bool:
        """Check if there are unsaved changes."""
        return self._dirty
    
    # --- Question Access ---
    
    def get_question(self, question_id: str) -> Question | None:
        """Get a question by ID."""
        for q in self._questions:
            if q.id == question_id:
                return q
        return None
    
    def get_questions_by_category(self, category_path: str) -> list[Question]:
        """Get all questions in a category."""
        return [q for q in self._questions if q.category_path == category_path]
    
    def get_questions_by_status(self, status: QuestionStatus) -> list[Question]:
        """Get all questions with a specific status."""
        return [q for q in self._questions if q.status == status]
    
    def get_filtered_questions(
        self, 
        category_path: str | None = None,
        status: QuestionStatus | None = None
    ) -> list[Question]:
        """Get questions filtered by category and/or status."""
        result = list(self._questions)
        if category_path is not None:
            result = [q for q in result if q.category_path == category_path]
        if status is not None:
            result = [q for q in result if q.status == status]
        return result
    
    # --- Mutations (via Commands) ---
    
    def _execute(self, command: Command) -> None:
        """Execute a command and add to undo stack."""
        command.execute(self)
        self._undo_stack.append(command)
        self._redo_stack.clear()  # Clear redo on new action
        
        # Limit undo history
        if len(self._undo_stack) > self.MAX_UNDO_HISTORY:
            self._undo_stack.pop(0)
        
        self._dirty = True
        self._notify_listeners()
    
    def delete_question(self, question_id: str) -> None:
        """Delete a question (undoable)."""
        cmd = DeleteQuestionCommand(
            description=f"Delete question",
            question_id=question_id
        )
        self._execute(cmd)
    
    def update_question(self, question_id: str, field_name: str, new_value: str) -> None:
        """Update a question field (undoable)."""
        cmd = UpdateQuestionCommand(
            description=f"Update {field_name}",
            question_id=question_id,
            field_name=field_name,
            new_value=new_value
        )
        self._execute(cmd)
    
    def delete_answer(self, question_id: str, answer_index: int) -> None:
        """Delete an answer from a question (undoable)."""
        cmd = DeleteAnswerCommand(
            description="Delete answer",
            question_id=question_id,
            answer_index=answer_index
        )
        self._execute(cmd)
    
    def toggle_status(self, question_id: str) -> None:
        """Toggle question status between Lista and Revisar (undoable)."""
        cmd = ToggleStatusCommand(
            description="Toggle status",
            question_id=question_id
        )
        self._execute(cmd)
    
    # --- Undo/Redo ---
    
    def undo(self) -> str | None:
        """Undo the last command. Returns command description or None."""
        if not self._undo_stack:
            return None
        
        cmd = self._undo_stack.pop()
        cmd.undo(self)
        self._redo_stack.append(cmd)
        self._dirty = True
        self._notify_listeners()
        return cmd.description
    
    def redo(self) -> str | None:
        """Redo the last undone command. Returns command description or None."""
        if not self._redo_stack:
            return None
        
        cmd = self._redo_stack.pop()
        cmd.execute(self)
        self._undo_stack.append(cmd)
        self._dirty = True
        self._notify_listeners()
        return cmd.description
    
    # --- Bulk Operations (not undoable) ---
    
    def add_questions(self, questions: list[Question]) -> None:
        """Add questions from import (not undoable - use for initial load)."""
        self._questions.extend(questions)
        self._notify_listeners()
    
    def clear(self) -> None:
        """Clear all questions (not undoable)."""
        self._questions.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._dirty = False
        self._notify_listeners()
    
    # --- Listeners ---
    
    def add_listener(self, callback: Callable[[], None]) -> None:
        """Add a listener that gets called on state changes."""
        self._listeners.append(callback)
    
    def _notify_listeners(self) -> None:
        """Notify all listeners of state change."""
        for listener in self._listeners:
            listener()
    
    # --- Persistence ---
    
    def to_dict(self) -> dict:
        """Serialize store to dictionary for JSON persistence."""
        return {
            "questions": [
                {
                    "id": q.id,
                    "name": q.name,
                    "question_text": q.question_text,
                    "general_feedback": q.general_feedback,
                    "category_path": q.category_path,
                    "status": q.status.value,
                    "default_grade": q.default_grade,
                    "penalty": q.penalty,
                    "single": q.single,
                    "shuffle_answers": q.shuffle_answers,
                    "answer_numbering": q.answer_numbering,
                    "correct_feedback": q.correct_feedback,
                    "partially_correct_feedback": q.partially_correct_feedback,
                    "incorrect_feedback": q.incorrect_feedback,
                    "source_file": q.source_file,
                    "answers": [
                        {
                            "text": a.text,
                            "fraction": a.fraction,
                            "feedback": a.feedback,
                            "format": a.format,
                        }
                        for a in q.answers
                    ],
                }
                for q in self._questions
            ]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuizStore":
        """Deserialize store from dictionary."""
        store = cls()
        for q_data in data.get("questions", []):
            answers = [
                Answer(
                    text=a["text"],
                    fraction=a["fraction"],
                    feedback=a.get("feedback", ""),
                    format=a.get("format", "html"),
                )
                for a in q_data.get("answers", [])
            ]
            question = Question(
                id=q_data["id"],
                name=q_data["name"],
                question_text=q_data["question_text"],
                general_feedback=q_data.get("general_feedback", ""),
                category_path=q_data.get("category_path", ""),
                status=QuestionStatus(q_data.get("status", "revisar")),
                default_grade=q_data.get("default_grade", "1.0000000"),
                penalty=q_data.get("penalty", "0.5000000"),
                single=q_data.get("single", "true"),
                shuffle_answers=q_data.get("shuffle_answers", "true"),
                answer_numbering=q_data.get("answer_numbering", "abc"),
                correct_feedback=q_data.get("correct_feedback", "<p>Correcto.</p>"),
                partially_correct_feedback=q_data.get("partially_correct_feedback", "<p>Parcialmente correcto.</p>"),
                incorrect_feedback=q_data.get("incorrect_feedback", "<p>Incorrecto.</p>"),
                source_file=q_data.get("source_file", ""),
                answers=answers,
            )
            store._questions.append(question)
        return store
    
    def save_to_file(self, path: Path) -> None:
        """Save state to JSON file."""
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        self._dirty = False
    
    @classmethod
    def load_from_file(cls, path: Path) -> "QuizStore":
        """Load state from JSON file."""
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data)
