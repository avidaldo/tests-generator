"""
Question Detail Panel - View and edit questions with answers.
Always-editable fields, 3-state workflow: PENDIENTE → REVISAR → LISTA
"""

from functools import partial

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPlainTextEdit, QPushButton, QLineEdit,
    QGroupBox, QFrame, QSizePolicy, QSpacerItem, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QUndoStack, QFont
import re

from models.question import Question, QuestionStatus
from models.quiz_model import QuizModel
from models.undo_commands import (
    ToggleStatusCommand, EditQuestionFieldCommand,
    DeleteAnswerCommand, EditAnswerCommand
)


class AnswerWidget(QFrame):
    """Widget for a single answer with edit and delete controls."""
    
    delete_requested = pyqtSignal(int)  # answer index
    text_changed = pyqtSignal(int, str)  # answer index, new text
    feedback_changed = pyqtSignal(int, str)  # answer index, new feedback
    
    def __init__(self, index: int, text: str, fraction: str, is_correct: bool, 
                 feedback: str = "", show_feedback: bool = True, parent=None):
        super().__init__(parent)
        self._index = index
        self._text = text
        self._feedback = feedback
        self._is_updating = False
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(1)
        
        # Color based on correct/incorrect - dark text for readability
        if is_correct:
            self.setStyleSheet("""
                QFrame { 
                    border: 2px solid #2E7D32; 
                    background-color: #E8F5E9; 
                }
                QTextEdit {
                    color: #1B5E20;
                    background-color: #F1F8E9;
                    border: 1px solid #81C784;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame { 
                    border: 1px solid #ccc; 
                    background-color: #FAFAFA;
                }
                QTextEdit {
                    border: 1px solid #ddd;
                }
            """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Header row with status icon and delete button
        header = QHBoxLayout()
        
        icon = "✓" if is_correct else "✗"
        color = "#2E7D32" if is_correct else "#C62828"
        fraction_text = f" ({fraction}%)" if not is_correct else " (correcta)"
        
        self._header_label = QLabel(f"<b style='color:{color};'>{icon} Respuesta {index + 1}{fraction_text}</b>")
        header.addWidget(self._header_label)
        
        header.addStretch()
        
        self._delete_btn = QPushButton("🗑")
        self._delete_btn.setFixedSize(30, 30)
        self._delete_btn.setToolTip("Eliminar esta respuesta")
        self._delete_btn.setStyleSheet("background-color: #C62828; color: white;")
        self._delete_btn.clicked.connect(lambda: self.delete_requested.emit(self._index))
        header.addWidget(self._delete_btn)
        layout.addLayout(header)
        
        # Text edit - auto-sizing based on content
        self._text_edit = QTextEdit()
        self._text_edit.setHtml(text)
        self._text_edit.textChanged.connect(self._on_text_changed)
        self._text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self._text_edit)
        
        # Feedback row (label on left, edit on right - same height)
        self._feedback_row = QHBoxLayout()
        self._feedback_row.setSpacing(8)
        
        self._feedback_label = QLabel("💬")
        self._feedback_label.setStyleSheet("color: #666;")
        self._feedback_label.setFixedWidth(20)
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._feedback_row.addWidget(self._feedback_label)
        
        self._feedback_edit = QTextEdit()
        self._feedback_edit.setHtml(feedback)
        self._feedback_edit.setPlaceholderText("Feedback...")
        self._feedback_edit.textChanged.connect(self._on_feedback_changed)
        self._feedback_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._feedback_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._feedback_row.addWidget(self._feedback_edit, 1)
        
        layout.addLayout(self._feedback_row)
        
        # Show/hide feedback based on toggle
        self._feedback_label.setVisible(show_feedback)
        self._feedback_edit.setVisible(show_feedback)
    
    def _adjust_text_height(self, text_edit: QTextEdit):
        """Adjust text edit height to fit content exactly."""
        doc = text_edit.document()
        # Set text width to available width for proper wrapping
        width = text_edit.viewport().width()
        if width <= 0:
            width = text_edit.width() - 10  # fallback
        if width > 0:
            doc.setTextWidth(width)
        # Get ideal height
        doc_height = doc.size().height()
        # Add minimal padding
        final_height = int(doc_height) + 6
        # Minimum of one line height
        font_metrics = text_edit.fontMetrics()
        min_height = font_metrics.height() + 10
        final_height = max(min_height, final_height)
        text_edit.setFixedHeight(final_height)
    
    def _on_text_changed(self):
        if self._is_updating:
            return
        self._adjust_text_height(self._text_edit)
        new_text = self._text_edit.toHtml()
        if new_text != self._text:
            self._text = new_text
            self.text_changed.emit(self._index, new_text)
    
    def _on_feedback_changed(self):
        if self._is_updating:
            return
        self._adjust_text_height(self._feedback_edit)
        new_feedback = self._feedback_edit.toHtml()
        if new_feedback != self._feedback:
            self._feedback = new_feedback
            self.feedback_changed.emit(self._index, new_feedback)
    
    def set_feedback_visible(self, visible: bool):
        """Show or hide the feedback section."""
        self._feedback_label.setVisible(visible)
        self._feedback_edit.setVisible(visible)
    
    def setFont(self, font: QFont):
        """Override to apply font to QTextEdit documents."""
        super().setFont(font)
        font_size = font.pointSize()
        # Apply to text edits - their documents need font set explicitly
        self._text_edit.setFont(font)
        self._text_edit.document().setDefaultFont(font)
        self._text_edit.setStyleSheet(f"font-size: {font_size}pt;")
        self._feedback_edit.setFont(font)
        self._feedback_edit.document().setDefaultFont(font)
        self._feedback_edit.setStyleSheet(f"font-size: {font_size}pt;")
        # Refresh heights
        self._adjust_text_height(self._text_edit)
        self._adjust_text_height(self._feedback_edit)


class QuestionDetailPanel(QWidget):
    """Panel for viewing and editing question details. 
    3-state workflow: PENDIENTE → REVISAR → LISTA
    """
    
    question_changed = pyqtSignal()
    delete_question_requested = pyqtSignal()
    
    def __init__(self, model: QuizModel, undo_stack: QUndoStack, parent=None):
        super().__init__(parent)
        self._model = model
        self._undo_stack = undo_stack
        self._current_question: Question | None = None
        self._answer_widgets: list[AnswerWidget] = []
        self._is_updating = False
        self._show_feedback = True  # Toggle state for feedback visibility
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header with name and actions
        header = QHBoxLayout()
        
        self._name_label = QLabel("Selecciona una pregunta")
        self._name_label.setStyleSheet("font-weight: bold;")
        self._name_label.setWordWrap(True)
        header.addWidget(self._name_label, 1)
        
        # Status buttons - 3 states
        self._lista_btn = QPushButton("✓ Lista")
        self._lista_btn.setMinimumWidth(90)
        self._lista_btn.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold;")
        self._lista_btn.clicked.connect(lambda: self._set_status(QuestionStatus.LISTA))
        self._lista_btn.setToolTip("Marcar como revisada y lista para el examen")
        header.addWidget(self._lista_btn)
        
        self._revisar_btn = QPushButton("↻ Revisar")
        self._revisar_btn.setMinimumWidth(90)
        self._revisar_btn.setStyleSheet("background-color: #F57C00; color: white; font-weight: bold;")
        self._revisar_btn.clicked.connect(lambda: self._set_status(QuestionStatus.REVISAR))
        self._revisar_btn.setToolTip("Marcar para revisión posterior")
        header.addWidget(self._revisar_btn)
        
        self._delete_question_btn = QPushButton("🗑 Eliminar")
        self._delete_question_btn.setStyleSheet("background-color: #C62828; color: white;")
        self._delete_question_btn.clicked.connect(lambda: self.delete_question_requested.emit())
        header.addWidget(self._delete_question_btn)
        
        layout.addLayout(header)
        
        # Category row (editable) and source info
        cat_row = QHBoxLayout()
        cat_row.setSpacing(8)
        
        cat_icon = QLabel("📁")
        cat_icon.setFixedWidth(20)
        cat_row.addWidget(cat_icon)
        
        self._category_edit = QLineEdit()
        self._category_edit.setPlaceholderText("Categoría (ej: $course$/Tema1/Subtema)")
        self._category_edit.setStyleSheet("color: #333;")
        self._category_edit.editingFinished.connect(self._on_category_changed)
        cat_row.addWidget(self._category_edit, 1)
        
        self._source_label = QLabel("")
        self._source_label.setStyleSheet("color: #666;")
        cat_row.addWidget(self._source_label)
        
        layout.addLayout(cat_row)
        
        # Current status indicator
        self._status_label = QLabel("")
        self._status_label.setStyleSheet("padding: 5px;")
        layout.addWidget(self._status_label)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)
        
        # Question text - always editable, auto-sizing
        self._question_group = QGroupBox("Texto de la pregunta")
        question_layout = QVBoxLayout(self._question_group)
        self._question_edit = QTextEdit()
        self._question_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._question_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._question_edit.textChanged.connect(self._on_question_text_changed)
        self._question_edit.textChanged.connect(lambda: self._adjust_textedit_height(self._question_edit, 30, 300))
        question_layout.addWidget(self._question_edit)
        layout.addWidget(self._question_group)
        
        # Feedback - always editable, auto-sizing
        self._feedback_group = QGroupBox("Feedback general")
        feedback_layout = QVBoxLayout(self._feedback_group)
        self._feedback_edit = QTextEdit()
        self._feedback_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._feedback_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._feedback_edit.textChanged.connect(self._on_feedback_changed)
        self._feedback_edit.textChanged.connect(lambda: self._adjust_textedit_height(self._feedback_edit, 30, 120))
        feedback_layout.addWidget(self._feedback_edit)
        layout.addWidget(self._feedback_group)
        
        # Answers section with toggle button
        answers_header = QHBoxLayout()
        answers_title = QLabel("<b>Respuestas</b>")
        answers_header.addWidget(answers_title)
        answers_header.addStretch()
        
        self._toggle_feedback_btn = QPushButton("💬 Ocultar Feedback")
        self._toggle_feedback_btn.setCheckable(True)
        self._toggle_feedback_btn.setChecked(True)
        self._toggle_feedback_btn.clicked.connect(self._toggle_feedback_visibility)
        answers_header.addWidget(self._toggle_feedback_btn)
        layout.addLayout(answers_header)
        
        self._answers_group = QGroupBox()
        self._answers_layout = QVBoxLayout(self._answers_group)
        self._answers_layout.setSpacing(8)
        layout.addWidget(self._answers_group, 1)
        
        layout.addStretch()
    
    def setFont(self, font: QFont):
        """Override to apply font to all QTextEdit documents."""
        super().setFont(font)
        # Apply to all QTextEdit widgets
        for text_edit in self.findChildren(QTextEdit):
            self._apply_font_to_text_edit(text_edit, font)
        
        # Refresh heights after font change
        if hasattr(self, '_question_edit'):
            self._adjust_textedit_height(self._question_edit)
        if hasattr(self, '_feedback_edit'):
            self._adjust_textedit_height(self._feedback_edit)
        # Refresh answer widgets
        for widget in self._answer_widgets:
            widget.setFont(font)
            
    def _apply_font_to_text_edit(self, text_edit: QTextEdit, font: QFont):
        """Apply font to QTextEdit and its document, ensuring style persists."""
        text_edit.setFont(font)
        doc = text_edit.document()
        doc.setDefaultFont(font)
        # Force re-render with new font by using stylesheet
        text_edit.setStyleSheet(f"font-size: {font.pointSize()}pt;")

    def _adjust_textedit_height(self, text_edit: QTextEdit, min_height: int = 30, max_height: int = 600):
        """Dynamically adjust QTextEdit height based on content."""
        doc = text_edit.document()
        # Set text width to available width for proper wrapping
        width = text_edit.viewport().width()
        if width <= 0:
            width = text_edit.width() - 10
        if width > 0:
            doc.setTextWidth(width)
        # Get ideal height
        doc_height = doc.size().height()
        # Add minimal padding
        target_height = int(doc_height) + 6
        # Minimum of one line height
        font_metrics = text_edit.fontMetrics()
        min_h = max(min_height, font_metrics.height() + 10)
        final_height = max(min_h, min(target_height, max_height))
        text_edit.setFixedHeight(final_height)
    
    def set_question(self, question: Question | None):
        """Set the question to display."""
        self._current_question = question
        self._refresh_display()
    
    def _clean_html(self, html: str) -> str:
        """Extract body content if present to avoid fixed body styles."""
        if not html:
            return ""
        # Check if it's a full HTML doc with body
        match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return html

    def _refresh_display(self):
        """Refresh the display with current question."""
        self._is_updating = True
        
        if self._current_question is None:
            self._name_label.setText("Selecciona una pregunta")
            self._category_edit.clear()
            self._category_edit.setEnabled(False)
            self._source_label.setText("")
            self._status_label.setText("")
            self._question_edit.clear()
            self._feedback_edit.clear()
            self._clear_answers()
            self._lista_btn.setEnabled(False)
            self._revisar_btn.setEnabled(False)
            self._delete_question_btn.setEnabled(False)
            self._is_updating = False
            return
        
        q = self._current_question
        self._name_label.setText(q.name)
        self._category_edit.setText(q.category_path or "")
        self._category_edit.setEnabled(True)
        self._source_label.setText(f"📄 {q.source_file or 'Nuevo'}")
        
        # Enable buttons
        self._delete_question_btn.setEnabled(True)
        
        # Status indicator and button states
        if q.status == QuestionStatus.LISTA:
            self._status_label.setText("Estado: ✓ LISTA")
            self._status_label.setStyleSheet(
                "padding: 5px; background-color: #C8E6C9; "
                "color: #1B5E20; border-radius: 3px; font-weight: bold;"
            )
            self._lista_btn.setEnabled(False)
            self._revisar_btn.setEnabled(True)
        elif q.status == QuestionStatus.REVISAR:
            self._status_label.setText("Estado: ↻ REVISAR")
            self._status_label.setStyleSheet(
                "padding: 5px; background-color: #FFE0B2; "
                "color: #E65100; border-radius: 3px; font-weight: bold;"
            )
            self._lista_btn.setEnabled(True)
            self._revisar_btn.setEnabled(False)
        else:  # PENDIENTE
            self._status_label.setText("Estado: ⋯ PENDIENTE")
            self._status_label.setStyleSheet(
                "padding: 5px; background-color: #E3F2FD; "
                "color: #1565C0; border-radius: 3px; font-weight: bold;"
            )
            self._lista_btn.setEnabled(True)
            self._revisar_btn.setEnabled(True)
        
        # Question text - clean HTML to allow font resizing
        self._question_edit.setHtml(self._clean_html(q.question_text))
        self._apply_font_to_text_edit(self._question_edit, self.font())
        
        # Feedback - clean HTML
        self._feedback_edit.setHtml(self._clean_html(q.general_feedback or ""))
        self._apply_font_to_text_edit(self._feedback_edit, self.font())
        
        # Adjust heights after content is set (use timer to ensure viewport is sized)
        QTimer.singleShot(0, lambda: self._adjust_textedit_height(self._question_edit, 30, 300))
        QTimer.singleShot(0, lambda: self._adjust_textedit_height(self._feedback_edit, 30, 120))
        
        # Answers
        self._refresh_answers()
        
        self._is_updating = False
    
    def _clear_answers(self):
        self._answer_widgets.clear()
        while self._answers_layout.count():
            item = self._answers_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _refresh_answers(self):
        self._clear_answers()
        if not self._current_question:
            return
        
        for i, ans in enumerate(self._current_question.answers):
            widget = AnswerWidget(
                index=i,
                text=self._clean_html(ans.text),
                fraction=ans.fraction,
                is_correct=ans.is_correct,
                feedback=self._clean_html(ans.feedback),
                show_feedback=self._show_feedback
            )
            # Apply current font to the new widget
            widget.setFont(self.font())
            
            widget.delete_requested.connect(self._on_delete_answer)
            widget.text_changed.connect(self._on_answer_text_changed)
            widget.feedback_changed.connect(self._on_answer_feedback_changed)
            self._answer_widgets.append(widget)
            self._answers_layout.addWidget(widget)
        
        self._answers_layout.addStretch()
        
        # Adjust heights after widgets are added to layout (deferred)
        QTimer.singleShot(10, self._adjust_answer_heights)
    
    def _adjust_answer_heights(self):
        """Adjust heights of all answer widgets."""
        for widget in self._answer_widgets:
            widget._adjust_text_height(widget._text_edit)
            widget._adjust_text_height(widget._feedback_edit)
    
    def _toggle_feedback_visibility(self):
        """Toggle feedback visibility for all answer widgets."""
        self._show_feedback = self._toggle_feedback_btn.isChecked()
        self._toggle_feedback_btn.setText(
            "💬 Ocultar Feedback" if self._show_feedback else "💬 Mostrar Feedback"
        )
        for widget in self._answer_widgets:
            widget.set_feedback_visible(self._show_feedback)
    
    def _set_status(self, new_status: QuestionStatus):
        """Set the question to a specific status. If already at that status, reset to PENDIENTE."""
        if not self._current_question:
            return
        
        # Toggle: if already at this status, go back to PENDIENTE
        if self._current_question.status == new_status:
            new_status = QuestionStatus.PENDIENTE
        
        if self._current_question.status != new_status:
            from models.undo_commands import SetStatusCommand
            cmd = SetStatusCommand(self._model, self._current_question.id, new_status)
            self._undo_stack.push(cmd)
            self._refresh_display()
            self.question_changed.emit()
    
    def _on_question_text_changed(self):
        if self._is_updating or not self._current_question:
            return
        new_text = self._question_edit.toHtml()
        if new_text != self._current_question.question_text:
            cmd = EditQuestionFieldCommand(
                self._model, self._current_question.id,
                "question_text", self._current_question.question_text, new_text
            )
            self._undo_stack.push(cmd)
    
    def _on_feedback_changed(self):
        if self._is_updating or not self._current_question:
            return
        new_text = self._feedback_edit.toHtml()
        if new_text != self._current_question.general_feedback:
            cmd = EditQuestionFieldCommand(
                self._model, self._current_question.id,
                "general_feedback", self._current_question.general_feedback, new_text
            )
            self._undo_stack.push(cmd)
    
    def _on_delete_answer(self, answer_index: int):
        if not self._current_question:
            return
        cmd = DeleteAnswerCommand(self._model, self._current_question.id, answer_index)
        self._undo_stack.push(cmd)
        self._refresh_answers()
        self.question_changed.emit()
    
    def _on_answer_text_changed(self, answer_index: int, new_text: str):
        if self._is_updating or not self._current_question:
            return
        if answer_index < len(self._current_question.answers):
            old_text = self._current_question.answers[answer_index].text
            if new_text != old_text:
                cmd = EditAnswerCommand(
                    self._model, self._current_question.id, answer_index,
                    "text", old_text, new_text
                )
                self._undo_stack.push(cmd)
    
    def _on_answer_feedback_changed(self, answer_index: int, new_feedback: str):
        if self._is_updating or not self._current_question:
            return
        if answer_index < len(self._current_question.answers):
            old_feedback = self._current_question.answers[answer_index].feedback
            if new_feedback != old_feedback:
                cmd = EditAnswerCommand(
                    self._model, self._current_question.id, answer_index,
                    "feedback", old_feedback, new_feedback
                )
                self._undo_stack.push(cmd)
    
    def _on_category_changed(self):
        """Handle category path edit."""
        if self._is_updating or not self._current_question:
            return
        new_category = self._category_edit.text().strip()
        if new_category != self._current_question.category_path:
            cmd = EditQuestionFieldCommand(
                self._model, self._current_question.id,
                "category_path", self._current_question.category_path, new_category
            )
            self._undo_stack.push(cmd)
            self.question_changed.emit()
