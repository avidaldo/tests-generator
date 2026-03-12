"""
QuizModel - Qt Model for question list.

Wraps question data for use with QListView. Emits signals on changes.
"""

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from models.question import Question, QuestionStatus


class QuizModel(QAbstractListModel):
    """Qt model for quiz questions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._questions: list[Question] = []
    
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._questions)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._questions)):
            return None
        
        question = self._questions[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if question.status == QuestionStatus.LISTA:
                status_icon = "✓"
            elif question.status == QuestionStatus.REVISAR:
                status_icon = "↻"
            else:  # PENDIENTE
                status_icon = "⋯"
            return f"{status_icon} {question.name}"
        
        elif role == Qt.ItemDataRole.UserRole:
            return question
        
        elif role == Qt.ItemDataRole.ForegroundRole:
            if question.status == QuestionStatus.LISTA:
                return QColor("#2E7D32")  # Dark green
            elif question.status == QuestionStatus.REVISAR:
                return QColor("#E65100")  # Dark orange
            else:  # PENDIENTE
                return QColor("#1565C0")  # Blue
        
        return None
    
    def get_question(self, index: int) -> Question | None:
        if 0 <= index < len(self._questions):
            return self._questions[index]
        return None
    
    def get_question_by_id(self, question_id: str) -> Question | None:
        for q in self._questions:
            if q.id == question_id:
                return q
        return None
    
    def add_questions(self, questions: list[Question]) -> int:
        """Add questions to the model, skipping duplicates by name.
        
        Returns the number of questions actually added.
        """
        if not questions:
            return 0
        
        # Get existing question names for duplicate detection
        existing_names = {q.name for q in self._questions}
        
        # Filter out duplicates
        new_questions = [q for q in questions if q.name not in existing_names]
        
        if not new_questions:
            return 0
        
        start = len(self._questions)
        self.beginInsertRows(QModelIndex(), start, start + len(new_questions) - 1)
        self._questions.extend(new_questions)
        self.endInsertRows()
        
        return len(new_questions)
    
    def remove_question(self, index: int) -> Question | None:
        if not (0 <= index < len(self._questions)):
            return None
        
        self.beginRemoveRows(QModelIndex(), index, index)
        question = self._questions.pop(index)
        self.endRemoveRows()
        return question
    
    def insert_question(self, index: int, question: Question) -> None:
        index = max(0, min(index, len(self._questions)))
        self.beginInsertRows(QModelIndex(), index, index)
        self._questions.insert(index, question)
        self.endInsertRows()
    
    def update_question(self, index: int) -> None:
        if 0 <= index < len(self._questions):
            model_index = self.index(index, 0)
            self.dataChanged.emit(model_index, model_index)
    
    def get_index_by_id(self, question_id: str) -> int:
        for i, q in enumerate(self._questions):
            if q.id == question_id:
                return i
        return -1
    
    def clear(self) -> None:
        self.beginResetModel()
        self._questions.clear()
        self.endResetModel()
    
    @property
    def questions(self) -> list[Question]:
        return self._questions
    
    @property
    def categories(self) -> list[str]:
        return sorted(set(q.category_path for q in self._questions if q.category_path))
