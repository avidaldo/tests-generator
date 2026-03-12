"""
Main Window for Moodle Quiz Editor v3.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListView, QTreeWidget, QTreeWidgetItem, QMenuBar, QMenu,
    QToolBar, QStatusBar, QFileDialog, QMessageBox, QPushButton,
    QLabel, QGroupBox, QScrollArea, QGridLayout, QApplication
)
from PyQt6.QtCore import Qt, QModelIndex, QSortFilterProxyModel, QSettings, QTimer
from PyQt6.QtGui import QAction, QUndoStack, QKeySequence, QFont, QWheelEvent

from models.quiz_model import QuizModel
from models.question import QuestionStatus
from models.undo_commands import DeleteQuestionCommand
from views.question_detail import QuestionDetailPanel
from file_io.xml_parser import parse_multiple_files
from file_io.xml_writer import generate_xml
from file_io.state_io import save_state, load_state


class StatusFilterProxyModel(QSortFilterProxyModel):
    """Proxy model that filters questions by status and category."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._status_filter: QuestionStatus | None = None
        self._category_filter: str | None = None
    
    def set_status_filter(self, status: QuestionStatus | None):
        """Set the status filter. None shows all questions."""
        self._status_filter = status
        self.invalidateFilter()
    
    def set_category_filter(self, category_path: str | None):
        """Set the category filter. None shows all categories."""
        self._category_filter = category_path
        self.invalidateFilter()
    
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_model = self.sourceModel()
        question = source_model.get_question(source_row)
        if question is None:
            return False
        
        # Check status filter
        if self._status_filter is not None and question.status != self._status_filter:
            return False
        
        # Check category filter
        if self._category_filter is not None and question.category_path != self._category_filter:
            return False
        
        return True


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moodle Quiz Editor v3")
        self.setMinimumSize(1000, 700)
        
        # Store normal geometry for restore from maximized
        self._normal_geometry = (100, 100, 1400, 900)
        self.resize(1400, 900)
        self.move(100, 100)
        self.showMaximized()  # Start maximized
        
        # Data model and undo stack
        self._model = QuizModel()
        self._undo_stack = QUndoStack(self)
        
        # Proxy model for filtering
        self._proxy_model = StatusFilterProxyModel()
        self._proxy_model.setSourceModel(self._model)
        
        # Current filter
        self._filter_status: QuestionStatus | None = None
        self._filter_category: str | None = None
        
        # Settings for state persistence
        self._settings = QSettings()
        self._current_state_file: Path | None = None
        
        # Autosave: backup file path (in user's home or current dir)
        self._autosave_file = Path.home() / ".moodle_editor_autosave.json"
        self._autosave_timer = QTimer(self)
        self._autosave_timer.setSingleShot(True)
        self._autosave_timer.setInterval(1000)  # 1 second debounce
        self._autosave_timer.timeout.connect(self._do_autosave)
        
        # Connect model changes to autosave
        self._model.dataChanged.connect(self._schedule_autosave)
        self._model.rowsInserted.connect(self._schedule_autosave)
        self._model.rowsRemoved.connect(self._schedule_autosave)
        
        # Font scaling (Ctrl+Scroll)
        self._base_font_size = self._settings.value("font_size", 10, type=int)
        self._min_font_size = 8
        self._max_font_size = 24
        
        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_shortcuts()
        self._update_stats()
        self._apply_font_size()  # Apply saved font size
        
        # Auto-load last state on startup (defer to after window is shown)
        QTimer.singleShot(100, self._auto_load_last_state)
    
    def _setup_ui(self):
        # Central widget with splitter
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(5, 5, 5, 5)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: filters + category tree
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Filter buttons in 2x2 grid
        filter_group = QGroupBox("Filtros")
        filter_layout = QGridLayout(filter_group)
        filter_layout.setSpacing(4)
        
        self._btn_all = QPushButton("Todas")
        self._btn_all.setCheckable(True)
        self._btn_all.setChecked(True)
        self._btn_all.clicked.connect(lambda: self._set_status_filter(None))
        filter_layout.addWidget(self._btn_all, 0, 0)
        
        self._btn_pendiente = QPushButton("● Pendiente")
        self._btn_pendiente.setCheckable(True)
        self._btn_pendiente.clicked.connect(lambda: self._set_status_filter(QuestionStatus.PENDIENTE))
        filter_layout.addWidget(self._btn_pendiente, 0, 1)
        
        self._btn_revisar = QPushButton("↻ Revisar")
        self._btn_revisar.setCheckable(True)
        self._btn_revisar.clicked.connect(lambda: self._set_status_filter(QuestionStatus.REVISAR))
        filter_layout.addWidget(self._btn_revisar, 1, 0)
        
        self._btn_lista = QPushButton("✓ Lista")
        self._btn_lista.setCheckable(True)
        self._btn_lista.clicked.connect(lambda: self._set_status_filter(QuestionStatus.LISTA))
        filter_layout.addWidget(self._btn_lista, 1, 1)
        
        left_layout.addWidget(filter_group)
        
        # Category tree
        cat_group = QGroupBox("Categorías")
        cat_layout = QVBoxLayout(cat_group)
        self._category_tree = QTreeWidget()
        self._category_tree.setHeaderHidden(True)
        self._category_tree.itemClicked.connect(self._on_category_selected)
        cat_layout.addWidget(self._category_tree)
        left_layout.addWidget(cat_group)
        
        splitter.addWidget(left_panel)
        
        # Middle panel: question list
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        
        list_group = QGroupBox("Preguntas")
        list_layout = QVBoxLayout(list_group)
        self._question_list = QListView()
        self._question_list.setModel(self._proxy_model)  # Use proxy model for filtering
        self._question_list.selectionModel().currentChanged.connect(self._on_question_selected)
        list_layout.addWidget(self._question_list)
        middle_layout.addWidget(list_group)
        
        splitter.addWidget(middle_panel)
        
        # Right panel: question detail
        self._detail_panel = QuestionDetailPanel(self._model, self._undo_stack)
        self._detail_panel.question_changed.connect(self._update_stats)
        self._detail_panel.question_changed.connect(self._schedule_autosave)
        self._detail_panel.question_changed.connect(self._refresh_category_tree)
        self._detail_panel.delete_question_requested.connect(self._delete_selected)
        
        scroll = QScrollArea()
        scroll.setWidget(self._detail_panel)
        scroll.setWidgetResizable(True)
        splitter.addWidget(scroll)
        
        splitter.setSizes([200, 350, 650])  # Larger detail panel
        layout.addWidget(splitter)
        
        # Status bar
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._stats_label = QLabel("Total: 0 | Lista: 0 | Revisar: 0")
        self._status_bar.addWidget(self._stats_label)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("Archivo")
        
        open_action = QAction("Abrir XML...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_files)
        file_menu.addAction(open_action)
        
        save_action = QAction("Guardar estado...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_state)
        file_menu.addAction(save_action)
        
        load_action = QAction("Cargar estado...", self)
        load_action.triggered.connect(self._load_state)
        file_menu.addAction(load_action)
        
        export_action = QAction("Exportar XML...", self)
        export_action.triggered.connect(self._export_xml)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Salir", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Editar")
        
        undo_action = self._undo_stack.createUndoAction(self, "Deshacer")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = self._undo_stack.createRedoAction(self, "Rehacer")
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        delete_action = QAction("Eliminar pregunta", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self._delete_selected)
        edit_menu.addAction(delete_action)
        
        # View menu
        view_menu = menubar.addMenu("Vista")
        
        zoom_in_action = QAction("Aumentar zoom", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self._zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Reducir zoom", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self._zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Restablecer zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self._reset_zoom)
        view_menu.addAction(reset_zoom_action)
    
    def _setup_toolbar(self):
        toolbar = QToolBar("Principal")
        self.addToolBar(toolbar)
        
        toolbar.addAction("Abrir", self._open_files)
        toolbar.addAction("Guardar", self._save_state)
    
    def _setup_shortcuts(self):
        pass  # Shortcuts defined in menu actions
    
    def _open_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Abrir archivos XML", "", "XML Files (*.xml)"
        )
        if files:
            try:
                paths = [Path(f) for f in files]
                _, questions = parse_multiple_files(paths)
                added_count = self._model.add_questions(questions)
                self._refresh_category_tree()
                self._update_stats()
                
                # Build status message
                if added_count == len(questions):
                    msg = f"Importadas {added_count} preguntas de {len(files)} archivo(s)"
                else:
                    skipped = len(questions) - added_count
                    msg = f"Importadas {added_count} preguntas ({skipped} duplicadas omitidas)"
                self._status_bar.showMessage(msg, 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al importar: {e}")
    
    def _save_state(self):
        if not self._model.questions:
            QMessageBox.warning(self, "Aviso", "No hay preguntas para guardar.")
            return
        
        # Suggest current file or last directory
        default_dir = str(self._current_state_file) if self._current_state_file else ""
        file, _ = QFileDialog.getSaveFileName(
            self, "Guardar estado", default_dir, "JSON Files (*.json)"
        )
        if file:
            try:
                if not file.endswith(".json"):
                    file += ".json"
                save_state(self._model.questions, Path(file))
                self._current_state_file = Path(file)
                self._settings.setValue("last_state_file", file)
                self._status_bar.showMessage(f"Estado guardado en {file}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar: {e}")
    
    def _load_state(self):
        # Suggest last directory
        default_dir = str(self._current_state_file.parent) if self._current_state_file else ""
        file, _ = QFileDialog.getOpenFileName(
            self, "Cargar estado", default_dir, "JSON Files (*.json)"
        )
        if file:
            try:
                questions = load_state(Path(file))
                self._model.clear()
                self._model.add_questions(questions)
                self._current_state_file = Path(file)
                self._settings.setValue("last_state_file", file)
                self._refresh_category_tree()
                self._update_stats()
                self._status_bar.showMessage(
                    f"Cargadas {len(questions)} preguntas de {file}", 3000
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar: {e}")
    
    def _export_xml(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "Exportar XML", "", "XML Files (*.xml)"
        )
        if file:
            try:
                xml_content = generate_xml(self._model.questions)
                Path(file).write_text(xml_content, encoding="utf-8")
                self._status_bar.showMessage(f"Exportado a {file}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar: {e}")
    
    def _delete_selected(self):
        proxy_index = self._question_list.currentIndex()
        if proxy_index.isValid():
            # Map proxy index to source index
            source_index = self._proxy_model.mapToSource(proxy_index)
            cmd = DeleteQuestionCommand(self._model, source_index.row())
            self._undo_stack.push(cmd)
            self._update_stats()
            self._refresh_category_tree()  # Update categories (remove empty ones)
            
            # Select next item in proxy view
            if self._proxy_model.rowCount() > 0:
                new_row = min(proxy_index.row(), self._proxy_model.rowCount() - 1)
                self._question_list.setCurrentIndex(self._proxy_model.index(new_row, 0))
    
    def _on_question_selected(self, current: QModelIndex, previous: QModelIndex):
        # Map proxy index to source index
        source_index = self._proxy_model.mapToSource(current)
        question = self._model.get_question(source_index.row())
        self._detail_panel.set_question(question)
    
    def _on_category_selected(self, item: QTreeWidgetItem, column: int):
        cat_path = item.data(0, Qt.ItemDataRole.UserRole)
        self._filter_category = cat_path
        # Apply category filter to proxy model
        self._proxy_model.set_category_filter(cat_path)
        # Clear selection when filter changes
        self._detail_panel.set_question(None)
        if cat_path:
            self._status_bar.showMessage(f"Categoría: {item.text(0)}", 2000)
        else:
            self._status_bar.showMessage("Mostrando todas las categorías", 2000)
    
    def _set_status_filter(self, status: QuestionStatus | None):
        self._filter_status = status
        self._btn_all.setChecked(status is None)
        self._btn_pendiente.setChecked(status == QuestionStatus.PENDIENTE)
        self._btn_revisar.setChecked(status == QuestionStatus.REVISAR)
        self._btn_lista.setChecked(status == QuestionStatus.LISTA)
        # Apply filter to proxy model
        self._proxy_model.set_status_filter(status)
        # Clear selection when filter changes
        self._detail_panel.set_question(None)
    
    def _refresh_category_tree(self):
        self._category_tree.clear()
        root = QTreeWidgetItem(self._category_tree, ["Todas"])
        root.setData(0, Qt.ItemDataRole.UserRole, None)
        
        for cat_path in self._model.categories:
            name = cat_path.split("/")[-1]
            item = QTreeWidgetItem(self._category_tree, [name])
            item.setData(0, Qt.ItemDataRole.UserRole, cat_path)
        
        self._category_tree.expandAll()
    
    def _update_stats(self):
        total = self._model.rowCount()
        lista = sum(1 for q in self._model.questions if q.status == QuestionStatus.LISTA)
        revisar = sum(1 for q in self._model.questions if q.status == QuestionStatus.REVISAR)
        pendiente = sum(1 for q in self._model.questions if q.status == QuestionStatus.PENDIENTE)
        
        self._stats_label.setText(f"Total: {total} | ⋯ Pendiente: {pendiente} | ↻ Revisar: {revisar} | ✓ Lista: {lista}")
    
    def _schedule_autosave(self, *args):
        """Schedule an autosave after changes (debounced)."""
        if self._model.questions:
            self._autosave_timer.start()
    
    def _do_autosave(self):
        """Perform the actual autosave to backup file."""
        if not self._model.questions:
            return
        try:
            save_state(self._model.questions, self._autosave_file)
            self._settings.setValue("autosave_file", str(self._autosave_file))
        except Exception:
            pass  # Silent fail for autosave
    
    def _auto_load_last_state(self):
        """Check for autosave or last state file and offer to load it."""
        # First check autosave file (most recent backup)
        autosave_exists = self._autosave_file.exists()
        last_state = self._settings.value("last_state_file", "")
        last_state_exists = last_state and Path(last_state).exists()
        
        if autosave_exists or last_state_exists:
            # Determine which file to suggest
            if autosave_exists and last_state_exists:
                # Compare modification times
                autosave_mtime = self._autosave_file.stat().st_mtime
                state_mtime = Path(last_state).stat().st_mtime
                if autosave_mtime > state_mtime:
                    suggested_file = self._autosave_file
                    label = "copia de seguridad automática"
                else:
                    suggested_file = Path(last_state)
                    label = last_state
            elif autosave_exists:
                suggested_file = self._autosave_file
                label = "copia de seguridad automática"
            else:
                suggested_file = Path(last_state)
                label = last_state
            
            reply = QMessageBox.question(
                self,
                "Restaurar sesión",
                f"¿Desea restaurar la última sesión?\n\n({label})",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    questions = load_state(suggested_file)
                    self._model.clear()
                    self._model.add_questions(questions)
                    if last_state_exists:
                        self._current_state_file = Path(last_state)
                    self._refresh_category_tree()
                    self._update_stats()
                    self._status_bar.showMessage(
                        f"Restauradas {len(questions)} preguntas", 3000
                    )
                except Exception as e:
                    QMessageBox.warning(self, "Aviso", f"No se pudo restaurar la sesión: {e}")
    
    def closeEvent(self, event):
        """Handle window close event - prompt to save state."""
        # Always do a final autosave
        self._do_autosave()
        
        if not self._model.questions:
            event.accept()
            return
        
        reply = QMessageBox.question(
            self,
            "Guardar cambios",
            "¿Desea guardar el estado actual antes de salir?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )
        
        if reply == QMessageBox.StandardButton.Cancel:
            event.ignore()
            return
        
        if reply == QMessageBox.StandardButton.Save:
            if self._current_state_file:
                # Save to the current file directly
                try:
                    save_state(self._model.questions, self._current_state_file)
                    self._settings.setValue("last_state_file", str(self._current_state_file))
                    self._status_bar.showMessage(f"Estado guardado en {self._current_state_file}", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al guardar: {e}")
                    event.ignore()
                    return
            else:
                # Ask for file location
                file, _ = QFileDialog.getSaveFileName(
                    self, "Guardar estado", "", "JSON Files (*.json)"
                )
                if file:
                    try:
                        if not file.endswith(".json"):
                            file += ".json"
                        save_state(self._model.questions, Path(file))
                        self._settings.setValue("last_state_file", file)
                        self._current_state_file = Path(file)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Error al guardar: {e}")
                        event.ignore()
                        return
                else:
                    # User cancelled the save dialog
                    event.ignore()
                    return
        
        event.accept()
    
    def _apply_font_size(self):
        """Apply the current font size to the entire application."""
        font = QFont()
        font.setPointSize(self._base_font_size)
        # Set application-wide font
        QApplication.instance().setFont(font)
        # Force update on all widgets recursively
        self._apply_font_recursive(self, font)
    
    def _apply_font_recursive(self, widget, font):
        """Recursively apply font to widget and all children."""
        widget.setFont(font)
        for child in widget.findChildren(QWidget):
            child.setFont(font)
    
    def _zoom_in(self):
        """Increase font size."""
        if self._base_font_size < self._max_font_size:
            self._base_font_size += 1
            self._apply_font_size()
            self._settings.setValue("font_size", self._base_font_size)
            self._status_bar.showMessage(f"Zoom: {self._base_font_size}pt", 1000)
    
    def _zoom_out(self):
        """Decrease font size."""
        if self._base_font_size > self._min_font_size:
            self._base_font_size -= 1
            self._apply_font_size()
            self._settings.setValue("font_size", self._base_font_size)
            self._status_bar.showMessage(f"Zoom: {self._base_font_size}pt", 1000)
    
    def _reset_zoom(self):
        """Reset font size to default."""
        self._base_font_size = 10
        self._apply_font_size()
        self._settings.setValue("font_size", self._base_font_size)
        self._status_bar.showMessage("Zoom: 10pt (default)", 1000)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle Ctrl+Scroll for font scaling."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self._zoom_in()
            elif delta < 0:
                self._zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)
    
    def changeEvent(self, event):
        """Handle window state changes - restore to normal size when unmaximizing."""
        from PyQt6.QtCore import QEvent
        if event.type() == QEvent.Type.WindowStateChange:
            # If we were maximized and now we're not
            if (event.oldState() & Qt.WindowState.WindowMaximized and 
                not (self.windowState() & Qt.WindowState.WindowMaximized)):
                # Apply stored normal geometry
                x, y, w, h = self._normal_geometry
                self.setGeometry(x, y, w, h)
        super().changeEvent(event)
