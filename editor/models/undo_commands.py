"""
Undo Commands for Quiz Editor.

QUndoCommand subclasses for undoable operations.
"""

from PyQt6.QtGui import QUndoCommand

from models.question import Question, Answer, QuestionStatus
from models.quiz_model import QuizModel


def _get_question_index(model: QuizModel, question: Question) -> int:
    """Resolve the row for the exact question instance currently stored in the model."""
    return model.get_index_of_question(question)


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

    def __init__(self, model: QuizModel, question: Question, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self.setText("Cambiar estado")

    def _toggle(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            self._question.status = (
                QuestionStatus.LISTA
                if self._question.status == QuestionStatus.REVISAR
                else QuestionStatus.REVISAR
            )
            self._model.update_question(index)

    def redo(self) -> None:
        self._toggle()

    def undo(self) -> None:
        self._toggle()


class SetStatusCommand(QUndoCommand):
    """Command to set question status to a specific value."""

    def __init__(self, model: QuizModel, question: Question, new_status: QuestionStatus, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self._new_status = new_status
        self._old_status: QuestionStatus | None = None
        self.setText(f"Estado → {new_status.value}")

    def redo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            self._old_status = self._question.status
            self._question.status = self._new_status
            self._model.update_question(index)

    def undo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1 and self._old_status is not None:
            self._question.status = self._old_status
            self._model.update_question(index)


class ToggleEasyCommand(QUndoCommand):
    """Command to toggle the is_easy flag on a question."""

    def __init__(self, model: QuizModel, question: Question, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self.setText("Alternar fácil")

    def _toggle(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            self._question.is_easy = not self._question.is_easy
            self._model.update_question(index)

    def redo(self) -> None:
        self._toggle()

    def undo(self) -> None:
        self._toggle()


class EditQuestionFieldCommand(QUndoCommand):
    """Command to edit a question field."""

    def __init__(self, model: QuizModel, question: Question,
                 field_name: str, old_value: str, new_value: str, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self._field_name = field_name
        self._old_value = old_value
        self._new_value = new_value
        self.setText(f"Editar {field_name}")

    def redo(self) -> None:
        self._set_value(self._new_value)

    def undo(self) -> None:
        self._set_value(self._old_value)

    def _set_value(self, value: str) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            setattr(self._question, self._field_name, value)
            self._model.update_question(index)


class DeleteAnswerCommand(QUndoCommand):
    """Command to delete an answer from a question."""

    def __init__(self, model: QuizModel, question: Question, answer_index: int, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self._answer_index = answer_index
        self._deleted_answer: Answer | None = None
        self.setText("Eliminar respuesta")

    def redo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1 and 0 <= self._answer_index < len(self._question.answers):
            self._deleted_answer = self._question.answers.pop(self._answer_index)
            self._model.update_question(index)

    def undo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1 and self._deleted_answer:
            self._question.answers.insert(self._answer_index, self._deleted_answer)
            self._model.update_question(index)


class EditAnswerCommand(QUndoCommand):
    """Command to edit an answer field."""

    def __init__(self, model: QuizModel, question: Question, answer_index: int,
                 field_name: str, old_value: any, new_value: any, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self._answer_index = answer_index
        self._field_name = field_name
        self._old_value = old_value
        self._new_value = new_value
        self.setText("Editar respuesta")

    def redo(self) -> None:
        self._set_value(self._new_value)

    def undo(self) -> None:
        self._set_value(self._old_value)

    def _set_value(self, value: any) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1 and 0 <= self._answer_index < len(self._question.answers):
            setattr(self._question.answers[self._answer_index], self._field_name, value)
            self._model.update_question(index)


class PurgeAnswersCommand(QUndoCommand):
    """Command to remove all distractors not marked as correct or correct-reviewed."""

    def __init__(self, model: QuizModel, question: Question, parent=None):
        super().__init__(parent)
        self._model = model
        self._question = question
        self._old_answers = list(question.answers)
        self.setText("Eliminar respuestas no marcadas")

    def redo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            # Keep correct answers or those marked as correct-reviewed
            self._question.answers = [
                ans for ans in self._old_answers
                if ans.is_correct or ans.correct_reviewed
            ]
            self._model.update_question(index)

    def undo(self) -> None:
        index = _get_question_index(self._model, self._question)
        if index != -1:
            self._question.answers = list(self._old_answers)
            self._model.update_question(index)

