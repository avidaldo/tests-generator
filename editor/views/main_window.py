"""
Main Window for Moodle Quiz Editor v3.
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListView, QTreeWidget, QTreeWidgetItem, QMenuBar, QMenu,
    QToolBar, QStatusBar, QFileDialog, QMessageBox, QPushButton,
    QLabel, QGroupBox, QScrollArea, QGridLayout, QApplication,
    QDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QModelIndex, QSortFilterProxyModel, QSettings, QTimer
from PyQt6.QtGui import QAction, QActionGroup, QUndoStack, QKeySequence, QFont, QPalette, QWheelEvent

from models.quiz_model import QuizModel
from models.question import QuestionStatus
from i18n import tr, set_language, current_language, available_languages
from models.question_diagnostics import analyze_question
from models.undo_commands import DeleteQuestionCommand
from views.question_detail import QuestionDetailPanel
from views.theme import THEME_OPTIONS, THEME_SYSTEM, apply_app_theme, effective_theme_variant, build_text_edit_style
from file_io.stage3_batch_finder import discover_stage3_batch_files
from file_io.xml_parser import parse_multiple_files
from file_io.xml_writer import generate_xml
from file_io.state_io import load_review_session, load_stage3_batch, save_state


class StatusFilterProxyModel(QSortFilterProxyModel):
    """Proxy model that filters questions by status and category."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status_filter: QuestionStatus | None = None
        self._category_filter: str | None = None
        self._easy_only: bool = False

    def set_status_filter(self, status: QuestionStatus | None):
        """Set the status filter. None shows all questions."""
        self._status_filter = status
        self.invalidateFilter()

    def set_category_filter(self, category_path: str | None):
        """Set the category filter. None shows all categories."""
        self._category_filter = category_path
        self.invalidateFilter()

    def set_easy_only(self, easy_only: bool):
        """Show only Lista+easy questions when True."""
        self._easy_only = easy_only
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_model = self.sourceModel()
        question = source_model.get_question(source_row)
        if question is None:
            return False

        # Easy-only mode overrides status filter (implies LISTA + is_easy)
        if self._easy_only:
            if question.status != QuestionStatus.READY or not question.is_easy:
                return False
        elif self._status_filter is not None and question.status != self._status_filter:
            return False

        # Check category filter
        if self._category_filter is not None and question.category_path != self._category_filter:
            return False

        return True


class SessionNotesDialog(QDialog):
    """Dialog for editing general session notes."""

    def __init__(self, notes: str, theme_mode: str = THEME_SYSTEM, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notas de la sesión")
        self.setMinimumSize(500, 400)
        self.resize(600, 450)

        layout = QVBoxLayout(self)

        self.label = QLabel("Notas generales de la sesión (lista de problemas, especificaciones futuras, etc.):")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(notes)

        theme_variant = effective_theme_variant(theme_mode)
        self.text_edit.setStyleSheet(build_text_edit_style(theme_variant))

        layout.addWidget(self.text_edit)

        # Standard buttons
        buttons_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton("Guardar")
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self.accept)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)

        layout.addLayout(buttons_layout)

    def get_notes(self) -> str:
        return self.text_edit.toPlainText()


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        theme_mode: str = THEME_SYSTEM,
        system_palette: QPalette | None = None,
        system_style_name: str | None = None,
    ):
        super().__init__()
        self.setWindowTitle("Moodle Quiz Editor v3[*]")
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
        self._filter_easy_only: bool = False

        # Settings for state persistence
        self._settings = QSettings()
        self._current_state_file: Path | None = None
        self._session_dirty = False
        self._session_notes = ""
        self._suspend_dirty_tracking = False
        self._theme_mode = theme_mode
        self._next_question_to_select = None
        app = QApplication.instance()
        current_palette = app.palette() if app is not None else QPalette()
        self._system_palette = QPalette(system_palette) if system_palette is not None else QPalette(current_palette)
        self._system_style_name = system_style_name or (app.style().objectName() if app is not None else "Fusion")
        self._theme_actions: dict[str, QAction] = {}

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
        self._model.dataChanged.connect(self._update_stats)
        self._model.dataChanged.connect(self._mark_session_dirty)
        self._model.rowsInserted.connect(self._mark_session_dirty)
        self._model.rowsRemoved.connect(self._mark_session_dirty)

        # Font scaling (Ctrl+Scroll)
        self._base_font_size = self._settings.value("font_size", 10, type=int)
        self._min_font_size = 8
        self._max_font_size = 24

        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_shortcuts()
        self._apply_theme_mode(self._theme_mode, persist=False)
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
        filter_group = QGroupBox(tr("filters.group"))
        filter_layout = QGridLayout(filter_group)
        filter_layout.setSpacing(4)

        self._btn_all = QPushButton(tr("filter.all"))
        self._btn_all.setCheckable(True)
        self._btn_all.setChecked(True)
        self._btn_all.clicked.connect(lambda: self._set_status_filter(None))
        filter_layout.addWidget(self._btn_all, 0, 0)

        self._btn_pendiente = QPushButton(tr("filter.pending"))
        self._btn_pendiente.setCheckable(True)
        self._btn_pendiente.clicked.connect(lambda: self._set_status_filter(QuestionStatus.PENDING))
        filter_layout.addWidget(self._btn_pendiente, 0, 1)

        self._btn_revisar = QPushButton(tr("filter.review"))
        self._btn_revisar.setCheckable(True)
        self._btn_revisar.clicked.connect(lambda: self._set_status_filter(QuestionStatus.REVIEW))
        filter_layout.addWidget(self._btn_revisar, 1, 0)

        self._btn_lista = QPushButton(tr("filter.ready"))
        self._btn_lista.setCheckable(True)
        self._btn_lista.clicked.connect(lambda: self._set_status_filter(QuestionStatus.READY))
        filter_layout.addWidget(self._btn_lista, 1, 1)

        self._btn_lista_facil = QPushButton(tr("filter.ready_easy"))
        self._btn_lista_facil.setCheckable(True)
        self._btn_lista_facil.clicked.connect(self._set_easy_filter)
        filter_layout.addWidget(self._btn_lista_facil, 2, 0, 1, 2)

        left_layout.addWidget(filter_group)

        # Category tree
        cat_group = QGroupBox(tr("group.categories"))
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

        list_group = QGroupBox(tr("group.questions"))
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
        self._detail_panel.question_changed.connect(self._mark_session_dirty)
        self._detail_panel.question_changed.connect(self._refresh_category_tree)
        self._detail_panel.delete_question_requested.connect(self._delete_selected)
        self._detail_panel.status_about_to_change.connect(self._on_status_about_to_change)
        self._detail_panel.question_changed.connect(self._on_question_changed_nav)

        scroll = QScrollArea()
        scroll.setWidget(self._detail_panel)
        scroll.setWidgetResizable(True)
        splitter.addWidget(scroll)

        splitter.setSizes([200, 350, 650])  # Larger detail panel
        layout.addWidget(splitter)

        # Status bar
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._stats_label = QLabel("")
        self._status_bar.addWidget(self._stats_label)

    def _setup_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(tr("menu.file"))

        new_session_action = QAction(tr("action.new_session"), self)
        new_session_action.triggered.connect(self._new_review_session)
        file_menu.addAction(new_session_action)

        open_session_action = QAction(tr("action.open_session"), self)
        open_session_action.triggered.connect(self._open_review_session)
        file_menu.addAction(open_session_action)

        self._recent_menu = file_menu.addMenu(tr("menu.open_recent"))
        self._rebuild_recent_menu()

        # Sessions auto-save on every change (write-through). "Save as..." only
        # assigns a file path / renames; there is no manual "Save" action.
        save_as_action = QAction(tr("action.save_as"), self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_review_session_as)
        file_menu.addAction(save_as_action)

        session_notes_action = QAction(tr("action.session_notes"), self)
        session_notes_action.triggered.connect(self._show_session_notes_dialog)
        file_menu.addAction(session_notes_action)

        file_menu.addSeparator()

        import_menu = file_menu.addMenu(tr("menu.add"))

        import_batch_action = QAction(tr("action.add_stage3"), self)
        import_batch_action.setShortcut(QKeySequence.StandardKey.Open)
        import_batch_action.triggered.connect(self._import_stage3_batches)
        import_menu.addAction(import_batch_action)

        import_batch_folder_action = QAction(tr("action.add_stage3_folder"), self)
        import_batch_folder_action.triggered.connect(self._import_stage3_folder)
        import_menu.addAction(import_batch_folder_action)

        legacy_import_menu = import_menu.addMenu(tr("menu.legacy"))

        import_xml_action = QAction(tr("action.import_xml"), self)
        import_xml_action.triggered.connect(self._import_legacy_xml_files)
        legacy_import_menu.addAction(import_xml_action)

        file_menu.addSeparator()

        export_menu = file_menu.addMenu(tr("menu.export"))

        export_action = QAction(tr("action.export_xml"), self)
        export_action.triggered.connect(self._export_xml)
        export_menu.addAction(export_action)

        export_easy_action = QAction(tr("action.export_xml_easy"), self)
        export_easy_action.triggered.connect(self._export_xml_easy)
        export_menu.addAction(export_easy_action)

        file_menu.addSeparator()

        quit_action = QAction(tr("action.quit"), self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu(tr("menu.edit"))

        undo_action = self._undo_stack.createUndoAction(self, tr("action.undo"))
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)

        redo_action = self._undo_stack.createRedoAction(self, tr("action.redo"))
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        delete_action = QAction(tr("action.delete_question"), self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self._delete_selected)
        edit_menu.addAction(delete_action)

        # View menu
        view_menu = menubar.addMenu(tr("menu.view"))

        zoom_in_action = QAction(tr("action.zoom_in"), self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self._zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction(tr("action.zoom_out"), self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self._zoom_out)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction(tr("action.reset_zoom"), self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self._reset_zoom)
        view_menu.addAction(reset_zoom_action)

        view_menu.addSeparator()

        theme_menu = view_menu.addMenu(tr("menu.theme"))
        theme_action_group = QActionGroup(self)
        theme_action_group.setExclusive(True)

        for theme_mode, _label in THEME_OPTIONS:
            action = QAction(tr(f"theme.{theme_mode}"), self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, mode=theme_mode: self._set_theme_mode(mode))
            theme_action_group.addAction(action)
            theme_menu.addAction(action)
            self._theme_actions[theme_mode] = action

        # Language submenu
        language_menu = view_menu.addMenu(tr("menu.language"))
        language_group = QActionGroup(self)
        language_group.setExclusive(True)
        for code, native_name in available_languages():
            action = QAction(native_name, self)
            action.setCheckable(True)
            action.setChecked(code == current_language())
            action.triggered.connect(lambda checked, lang=code: self._set_language(lang))
            language_group.addAction(action)
            language_menu.addAction(action)

    def _setup_toolbar(self):
        toolbar = QToolBar(tr("toolbar.main"))
        self.addToolBar(toolbar)

        toolbar.addAction(tr("toolbar.add_stage3"), self._import_stage3_batches)
        toolbar.addAction(tr("toolbar.add_folder"), self._import_stage3_folder)
        toolbar.addAction(tr("toolbar.open_session"), self._open_review_session)
        toolbar.addAction(tr("toolbar.session_notes"), self._show_session_notes_dialog)

    def _setup_shortcuts(self):
        pass  # Shortcuts defined in menu actions

    def _set_language(self, language: str) -> None:
        """Persist the chosen UI language; applied on next launch."""
        if language == current_language():
            return
        self._settings.setValue("language", language)
        set_language(language)
        QMessageBox.information(
            self, tr("language.restart_title"), tr("language.restart_body")
        )

    _MAX_RECENT_SESSIONS = 8

    def _recent_sessions(self) -> list[str]:
        stored = self._settings.value("recent_sessions", [], type=list) or []
        return [str(path) for path in stored if path]

    def _add_recent_session(self, filepath: Path) -> None:
        path_str = str(filepath)
        recents = [p for p in self._recent_sessions() if p != path_str]
        recents.insert(0, path_str)
        self._settings.setValue("recent_sessions", recents[: self._MAX_RECENT_SESSIONS])
        self._rebuild_recent_menu()

    def _rebuild_recent_menu(self) -> None:
        menu = getattr(self, "_recent_menu", None)
        if menu is None:
            return
        menu.clear()
        recents = self._recent_sessions()
        if not recents:
            empty = QAction("(sin sesiones recientes)", self)
            empty.setEnabled(False)
            menu.addAction(empty)
            return
        for path_str in recents:
            action = QAction(Path(path_str).name, self)
            action.setToolTip(path_str)
            action.triggered.connect(lambda _checked, p=path_str: self._open_recent_session(p))
            menu.addAction(action)
        menu.addSeparator()
        clear_action = QAction("Borrar lista", self)
        clear_action.triggered.connect(self._clear_recent_sessions)
        menu.addAction(clear_action)

    def _clear_recent_sessions(self) -> None:
        self._settings.setValue("recent_sessions", [])
        self._rebuild_recent_menu()

    def _open_recent_session(self, path_str: str) -> None:
        filepath = Path(path_str)
        if not filepath.exists():
            QMessageBox.warning(self, "Aviso", f"La sesión ya no existe:\n{path_str}")
            recents = [p for p in self._recent_sessions() if p != path_str]
            self._settings.setValue("recent_sessions", recents)
            self._rebuild_recent_menu()
            return
        if not self._confirm_session_replacement(
            "Abrir sesión",
            "La sesión actual se reemplazará al abrir otro archivo. ¿Desea guardar antes de continuar?",
        ):
            return
        self._load_session_from_path(filepath)

    def _default_session_dir(self) -> str:
        if self._current_state_file is not None:
            return str(self._current_state_file.parent)

        last_state = self._settings.value("last_state_file", "")
        if last_state:
            last_state_path = Path(last_state)
            if last_state_path.exists():
                return str(last_state_path.parent)

        return ""

    def _replace_loaded_session(
        self,
        questions,
        current_state_file: Path | None,
        status_message: str,
        is_dirty: bool = False,
        notes: str = "",
    ):
        self._suspend_dirty_tracking = True
        try:
            self._undo_stack.clear()
            self._model.clear()
            self._model.add_questions(list(questions))
        finally:
            self._suspend_dirty_tracking = False
        self._session_notes = notes
        self._current_state_file = current_state_file
        self._detail_panel.set_question(None)
        self._refresh_category_tree()
        self._update_stats()
        self._set_session_dirty(is_dirty)
        if not is_dirty:
            self._clear_autosave()
        self._status_bar.showMessage(status_message, 3000)

    def _set_session_dirty(self, is_dirty: bool):
        self._session_dirty = is_dirty
        self.setWindowModified(is_dirty)

    def _mark_session_dirty(self, *args):
        if self._suspend_dirty_tracking:
            return
        self._set_session_dirty(True)

    def _save_review_session_to_path(self, filepath: Path) -> bool:
        try:
            save_state(self._model.questions, filepath, self._session_notes)
            self._current_state_file = filepath
            self._settings.setValue("last_state_file", str(filepath))
            self._add_recent_session(filepath)
            self._clear_autosave()
            self._set_session_dirty(False)
            self._status_bar.showMessage(f"Sesión guardada en {filepath}", 3000)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {e}")
            return False

    def _save_review_session(self) -> bool:
        if not self._model.questions:
            QMessageBox.warning(self, "Aviso", "No hay preguntas para guardar en la sesión.")
            return False

        if self._current_state_file is not None:
            return self._save_review_session_to_path(self._current_state_file)

        return self._save_review_session_as()

    def _save_review_session_as(self) -> bool:
        if not self._model.questions:
            QMessageBox.warning(self, "Aviso", "No hay preguntas para guardar en la sesión.")
            return False

        default_path = str(self._current_state_file) if self._current_state_file is not None else self._default_session_dir()
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar sesión de revisión",
            default_path,
            "JSON Files (*.json)",
        )
        if not file:
            return False

        filepath = Path(file)
        if filepath.suffix != ".json":
            filepath = filepath.with_suffix(".json")

        return self._save_review_session_to_path(filepath)

    def _confirm_session_replacement(self, title: str, prompt: str) -> bool:
        if not self._session_dirty:
            return True

        reply = QMessageBox.question(
            self,
            title,
            prompt,
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )

        if reply == QMessageBox.StandardButton.Cancel:
            return False
        if reply == QMessageBox.StandardButton.Save:
            return self._save_review_session()
        self._clear_autosave()
        return True

    def _import_legacy_xml_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Añadir banco XML legado a la sesión actual",
            self._default_session_dir(),
            "XML Files (*.xml)",
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
                    msg = f"Añadidas {added_count} preguntas a la sesión actual desde {len(files)} archivo(s)"
                else:
                    skipped = len(questions) - added_count
                    msg = f"Añadidas {added_count} preguntas a la sesión actual ({skipped} duplicadas omitidas)"
                self._status_bar.showMessage(msg, 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al importar: {e}")

    def _import_stage3_batches(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Añadir archivos Stage 3 a la sesión actual",
            self._default_session_dir(),
            "Stage 3 JSON (*.json)",
        )
        if not files:
            return

        self._import_stage3_paths([Path(file) for file in files], selection_label="archivo(s)")

    def _import_stage3_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Añadir carpeta Stage 3 a la sesión actual",
            self._default_session_dir(),
        )
        if not folder:
            return

        try:
            batch_files = discover_stage3_batch_files(Path(folder))
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Error al explorar la carpeta: {exc}")
            return

        if not batch_files:
            QMessageBox.information(
                self,
                "Sin lotes Stage 3",
                "No se encontraron archivos `batch-*.json` dentro de la carpeta seleccionada.",
            )
            return

        self._import_stage3_paths(batch_files, selection_label="lote(s)")

    def _import_stage3_paths(self, paths: list[Path], selection_label: str):
        """Import Stage 3 JSON files into the current review session."""
        if not paths:
            return

        added_count = 0
        skipped_count = 0
        failed_files: list[str] = []

        for path in paths:
            try:
                questions = load_stage3_batch(path)
                imported = self._model.add_questions(questions)
                added_count += imported
                skipped_count += len(questions) - imported
            except Exception as exc:
                failed_files.append(f"{path.name}: {exc}")

        self._refresh_category_tree()
        self._update_stats()

        if failed_files:
            QMessageBox.warning(
                self,
                "Importación incompleta",
                "No se pudieron importar algunos archivos:\n\n" + "\n".join(failed_files),
            )

        failed_count = len(failed_files)
        failed_summary = f" | {failed_count} archivo(s) rechazado(s)" if failed_count else ""
        self._status_bar.showMessage(
            f"Añadidas {added_count} preguntas Stage 3 a la sesión actual desde {len(paths)} {selection_label} ({skipped_count} duplicadas omitidas){failed_summary}",
            5000,
        )

    def _new_review_session(self):
        if not self._confirm_session_replacement(
            "Nueva sesión",
            "La sesión actual se reemplazará por una sesión vacía. ¿Desea guardar antes de continuar?",
        ):
            return

        self._replace_loaded_session([], None, "Nueva sesión de revisión")

    def _show_session_notes_dialog(self):
        """Show the dialog to edit general session notes."""
        dialog = SessionNotesDialog(self._session_notes, self._theme_mode, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_notes = dialog.get_notes()
            if new_notes != self._session_notes:
                self._session_notes = new_notes
                self._mark_session_dirty()
                self._schedule_autosave()

    def _open_review_session(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir sesión de revisión",
            self._default_session_dir(),
            "JSON Files (*.json)",
        )
        if not file:
            return

        if not self._confirm_session_replacement(
            "Abrir sesión",
            "La sesión actual se reemplazará al abrir otro archivo. ¿Desea guardar antes de continuar?",
        ):
            return

        self._load_session_from_path(Path(file))

    def _load_session_from_path(self, filepath: Path) -> None:
        try:
            review_session = load_review_session(filepath)
            self._settings.setValue("last_state_file", str(filepath))
            self._add_recent_session(filepath)
            self._replace_loaded_session(
                review_session.questions,
                filepath,
                f"Abierta sesión con {len(review_session.questions)} preguntas",
                notes=review_session.notes,
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar: {e}")

    def _export_xml(self):
        lista_questions = [q for q in self._model.questions if q.status == QuestionStatus.READY]
        if not lista_questions:
            QMessageBox.information(
                self,
                "Sin preguntas listas",
                "No hay preguntas marcadas como \"Lista\".\n\nRevisa las preguntas y márcalas como Lista antes de exportar.",
            )
            return

        file, _ = QFileDialog.getSaveFileName(
            self, f"Exportar XML ({len(lista_questions)} preguntas Lista)", "", "XML Files (*.xml)"
        )
        if file:
            try:
                xml_content = generate_xml(lista_questions)
                Path(file).write_text(xml_content, encoding="utf-8")
                self._status_bar.showMessage(
                    f"Exportadas {len(lista_questions)} preguntas Lista → {file}", 4000
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar: {e}")

    def _export_xml_easy(self):
        easy_questions = [
            q for q in self._model.questions
            if q.status == QuestionStatus.READY and q.is_easy
        ]
        if not easy_questions:
            QMessageBox.information(
                self,
                "Sin preguntas fáciles",
                "No hay preguntas marcadas como \"Lista\" y \"Fácil\".\n\n"
                "Marca preguntas como Lista y luego activa el botón Fácil en el panel de detalle.",
            )
            return

        file, _ = QFileDialog.getSaveFileName(
            self,
            f"Exportar XML ({len(easy_questions)} preguntas Lista-Fácil)",
            "",
            "XML Files (*.xml)",
        )
        if file:
            try:
                xml_content = generate_xml(easy_questions)
                Path(file).write_text(xml_content, encoding="utf-8")
                self._status_bar.showMessage(
                    f"Exportadas {len(easy_questions)} preguntas Lista-Fácil → {file}", 4000
                )
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

    def _on_status_about_to_change(self, question, new_status):
        self._next_question_to_select = None
        if new_status == QuestionStatus.READY:
            current_proxy_index = self._question_list.currentIndex()
            if current_proxy_index.isValid():
                next_row = current_proxy_index.row() + 1
                if next_row < self._proxy_model.rowCount():
                    next_proxy_index = self._proxy_model.index(next_row, 0)
                    next_source_index = self._proxy_model.mapToSource(next_proxy_index)
                    self._next_question_to_select = self._model.get_question(next_source_index.row())

    def _on_question_changed_nav(self):
        if self._next_question_to_select:
            target = self._next_question_to_select
            self._next_question_to_select = None
            QTimer.singleShot(0, lambda: self._select_question_by_reference(target))

    def _select_question_by_reference(self, question):
        found_index = QModelIndex()
        for r in range(self._proxy_model.rowCount()):
            proxy_idx = self._proxy_model.index(r, 0)
            src_idx = self._proxy_model.mapToSource(proxy_idx)
            q = self._model.get_question(src_idx.row())
            if q is question:
                found_index = proxy_idx
                break
        if found_index.isValid():
            self._question_list.setCurrentIndex(found_index)
        else:
            self._detail_panel.set_question(None)

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
        self._filter_easy_only = False
        self._btn_all.setChecked(status is None)
        self._btn_pendiente.setChecked(status == QuestionStatus.PENDING)
        self._btn_revisar.setChecked(status == QuestionStatus.REVIEW)
        self._btn_lista.setChecked(status == QuestionStatus.READY)
        self._btn_lista_facil.setChecked(False)
        # Apply filter to proxy model
        self._proxy_model.set_easy_only(False)
        self._proxy_model.set_status_filter(status)
        # Clear selection when filter changes
        self._detail_panel.set_question(None)

    def _set_easy_filter(self):
        self._filter_status = QuestionStatus.READY
        self._filter_easy_only = True
        self._btn_all.setChecked(False)
        self._btn_pendiente.setChecked(False)
        self._btn_revisar.setChecked(False)
        self._btn_lista.setChecked(False)
        self._btn_lista_facil.setChecked(True)
        self._proxy_model.set_easy_only(True)
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
        lista = sum(1 for q in self._model.questions if q.status == QuestionStatus.READY)
        revisar = sum(1 for q in self._model.questions if q.status == QuestionStatus.REVIEW)
        pendiente = sum(1 for q in self._model.questions if q.status == QuestionStatus.PENDING)
        easy = sum(1 for q in self._model.questions if q.status == QuestionStatus.READY and q.is_easy)
        warnings = sum(1 for q in self._model.questions if analyze_question(q).has_warnings)

        self._stats_label.setText(
            tr("stats.summary", total=total, pending=pendiente, review=revisar,
               ready=lista, easy=easy, warnings=warnings)
        )

    def _schedule_autosave(self, *args):
        """Schedule an autosave after changes (debounced)."""
        if self._model.questions:
            self._autosave_timer.start()

    def _do_autosave(self):
        """Write changes straight through to the active session file (todos §17).

        When the session already has a file path, every change is persisted directly to
        it, so there is no manual "save" step. A session with no path yet (freshly
        imported, never "Guardar como...") falls back to the crash-recovery backup file
        and stays marked dirty so it is offered for saving on close/replace.
        """
        if not self._model.questions:
            return
        if self._current_state_file is not None:
            try:
                save_state(self._model.questions, self._current_state_file, self._session_notes)
                self._settings.setValue("last_state_file", str(self._current_state_file))
                self._clear_autosave()
                self._set_session_dirty(False)
            except Exception:
                pass  # Silent fail; keep dirty so the user can still save manually.
            return
        try:
            save_state(self._model.questions, self._autosave_file, self._session_notes)
            self._settings.setValue("autosave_file", str(self._autosave_file))
        except Exception:
            pass  # Silent fail for autosave

    def _clear_autosave(self):
        """Remove the crash-recovery autosave after a clean decision."""
        self._settings.remove("autosave_file")
        try:
            self._autosave_file.unlink(missing_ok=True)
        except OSError:
            pass

    def _restore_state_file(self, source_file: Path, current_state_file: Path | None):
        """Restore editor questions from a JSON state file."""
        review_session = load_review_session(source_file)
        is_autosave_restore = source_file == self._autosave_file
        self._replace_loaded_session(
            review_session.questions,
            current_state_file,
            f"Restauradas {len(review_session.questions)} preguntas",
            is_dirty=is_autosave_restore,
            notes=review_session.notes,
        )

    def _auto_load_last_state(self):
        """Restore the last saved state automatically and only prompt for crash recovery."""
        autosave_exists = self._autosave_file.exists()
        last_state = self._settings.value("last_state_file", "")
        last_state_exists = last_state and Path(last_state).exists()
        last_state_file = Path(last_state) if last_state_exists else None

        if autosave_exists and (
            not last_state_file or self._autosave_file.stat().st_mtime > last_state_file.stat().st_mtime
        ):
            reply = QMessageBox.question(
                self,
                "Restaurar sesión",
                "¿Desea restaurar la copia de seguridad automática más reciente?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self._restore_state_file(self._autosave_file, last_state_file)
                except Exception as e:
                    QMessageBox.warning(self, "Aviso", f"No se pudo restaurar la sesión: {e}")
            else:
                self._clear_autosave()
                if last_state_file:
                    try:
                        self._restore_state_file(last_state_file, last_state_file)
                    except Exception as e:
                        QMessageBox.warning(self, "Aviso", f"No se pudo restaurar la sesión: {e}")
            return

        if last_state_file:
            try:
                self._restore_state_file(last_state_file, last_state_file)
            except Exception as e:
                QMessageBox.warning(self, "Aviso", f"No se pudo restaurar la sesión: {e}")

    def closeEvent(self, event):
        """Handle window close event - prompt to save state."""
        if not self._model.questions:
            self._clear_autosave()
            event.accept()
            return

        if not self._session_dirty:
            self._clear_autosave()
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
            if not self._save_review_session():
                event.ignore()
                return
        else:
            self._clear_autosave()
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

    def _sync_theme_actions(self):
        for theme_mode, action in self._theme_actions.items():
            action.blockSignals(True)
            action.setChecked(theme_mode == self._theme_mode)
            action.blockSignals(False)

    def _apply_theme_mode(self, theme_mode: str, persist: bool):
        app = QApplication.instance()
        if app is not None:
            apply_app_theme(app, theme_mode, self._system_palette, self._system_style_name)
        self._detail_panel.set_theme_mode(theme_mode)
        self._sync_theme_actions()
        if persist:
            self._settings.setValue("theme_mode", theme_mode)
            theme_label = dict(THEME_OPTIONS)[theme_mode]
            self._status_bar.showMessage(f"Tema: {theme_label}", 1500)

    def _set_theme_mode(self, theme_mode: str):
        self._theme_mode = theme_mode
        self._apply_theme_mode(theme_mode, persist=True)

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
