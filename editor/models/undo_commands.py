"""
Undo Commands for Quiz Editor.

QUndoCommand subclasses for undoable operations.
"""

from PyQt6.QtGui import QUndoCommand

from models.question import Question, Answer, QuestionStatus
from models.quiz_model import QuizModel


class DeleteQuestionCommand(QUndoCommand):
    """Command to delete a question."""
    
    def __init__(self, model: QuizModel, index: int, parent=None):
        super().__init__(parent)
        self._model = model
        self._index = index
        self._question: Question | None = None
        self.setText("Eliminar pregunta")
    
    def redo(self) -> None:
        self._question = self._model.remove_question(self._index)
    
    def undo(self) -> None:
        if self._question:
            self._model.insert_question(self._index, self._question)


class ToggleStatusCommand(QUndoCommand):
    """Command to toggle question status."""
    
    def __init__(self, model: QuizModel, question_id: str, parent=None):
        super().__init__(parent)
        self._model = model
        self._question_id = question_id
        self.setText("Cambiar estado")
    
    def _toggle(self) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question:
            question.status = (
                QuestionStatus.LISTA 
                if question.status == QuestionStatus.REVISAR 
                else QuestionStatus.REVISAR
            )
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)
    
    def redo(self) -> None:
        self._toggle()
    
    def undo(self) -> None:
        self._toggle()


class SetStatusCommand(QUndoCommand):
    """Command to set question status to a specific value."""
    
    def __init__(self, model: QuizModel, question_id: str, new_status: QuestionStatus, parent=None):
        super().__init__(parent)
        self._model = model
        self._question_id = question_id
        self._new_status = new_status
        self._old_status: QuestionStatus | None = None
        self.setText(f"Estado → {new_status.value}")
    
    def redo(self) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question:
            self._old_status = question.status
            question.status = self._new_status
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)
    
    def undo(self) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question and self._old_status is not None:
            question.status = self._old_status
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)


class EditQuestionFieldCommand(QUndoCommand):
    """Command to edit a question field."""
    
    def __init__(self, model: QuizModel, question_id: str, 
                 field_name: str, old_value: str, new_value: str, parent=None):
        super().__init__(parent)
        self._model = model
        self._question_id = question_id
        self._field_name = field_name
        self._old_value = old_value
        self._new_value = new_value
        self.setText(f"Editar {field_name}")
    
    def redo(self) -> None:
        self._set_value(self._new_value)
    
    def undo(self) -> None:
        self._set_value(self._old_value)
    
    def _set_value(self, value: str) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question:
            setattr(question, self._field_name, value)
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)


class DeleteAnswerCommand(QUndoCommand):
    """Command to delete an answer from a question."""
    
    def __init__(self, model: QuizModel, question_id: str, answer_index: int, parent=None):
        super().__init__(parent)
        self._model = model
        self._question_id = question_id
        self._answer_index = answer_index
        self._deleted_answer: Answer | None = None
        self.setText("Eliminar respuesta")
    
    def redo(self) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question and 0 <= self._answer_index < len(question.answers):
            self._deleted_answer = question.answers.pop(self._answer_index)
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)
    
    def undo(self) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question and self._deleted_answer:
            question.answers.insert(self._answer_index, self._deleted_answer)
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)


class EditAnswerCommand(QUndoCommand):
    """Command to edit an answer field."""
    
    def __init__(self, model: QuizModel, question_id: str, answer_index: int,
                 field_name: str, old_value: str, new_value: str, parent=None):
        super().__init__(parent)
        self._model = model
        self._question_id = question_id
        self._answer_index = answer_index
        self._field_name = field_name
        self._old_value = old_value
        self._new_value = new_value
        self.setText(f"Editar respuesta")
    
    def redo(self) -> None:
        self._set_value(self._new_value)
    
    def undo(self) -> None:
        self._set_value(self._old_value)
    
    def _set_value(self, value: str) -> None:
        question = self._model.get_question_by_id(self._question_id)
        if question and 0 <= self._answer_index < len(question.answers):
            setattr(question.answers[self._answer_index], self._field_name, value)
            index = self._model.get_index_by_id(self._question_id)
            self._model.update_question(index)
