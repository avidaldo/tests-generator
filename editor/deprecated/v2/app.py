"""
Moodle Quiz Editor v2 - Main TUI Application

A Textual-based terminal interface for editing Moodle XML quiz files.
Run with: uv run python moodle-tests/editor/v2/app.py
"""

import sys
from pathlib import Path

# Add v2 directory to path for imports
_v2_dir = Path(__file__).parent
if str(_v2_dir) not in sys.path:
    sys.path.insert(0, str(_v2_dir))

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header,
    Footer,
    Static,
    ListView,
    ListItem,
    Label,
    Button,
    Input,
    TextArea,
    Tree,
    DirectoryTree,
)
from textual.screen import Screen, ModalScreen
from textual.message import Message
from textual import on

from models.question import Question, QuestionStatus
from models.quiz_store import QuizStore
from file_io.xml_parser import parse_xml_file, parse_multiple_files
from file_io.xml_writer import generate_xml


# --- File Selection Modal ---

class FileSelectModal(ModalScreen[list[Path] | None]):
    """Modal dialog for selecting XML files to import."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancelar"),
        Binding("enter", "confirm", "Confirmar"),
    ]
    
    CSS = """
    FileSelectModal {
        align: center middle;
    }
    
    #file-dialog {
        width: 80%;
        height: 80%;
        background: $surface;
        border: tall $primary;
        padding: 1;
    }
    
    #file-dialog-title {
        dock: top;
        text-style: bold;
        background: $primary;
        padding: 0 1;
        margin-bottom: 1;
    }
    
    #file-list {
        height: 1fr;
        border: round $secondary;
    }
    
    #file-path-input {
        dock: bottom;
        margin-top: 1;
    }
    
    #file-buttons {
        dock: bottom;
        height: 3;
        align: right middle;
        margin-top: 1;
    }
    """
    
    def __init__(self, start_dir: Path | None = None) -> None:
        super().__init__()
        self.start_dir = start_dir or Path.cwd()
        self.selected_paths: list[Path] = []
    
    def compose(self) -> ComposeResult:
        with Container(id="file-dialog"):
            yield Static("Seleccionar archivos XML", id="file-dialog-title")
            yield DirectoryTree(str(self.start_dir), id="file-list")
            yield Input(placeholder="Ruta del archivo (Enter para añadir)", id="file-path-input")
            with Horizontal(id="file-buttons"):
                yield Button("Cancelar [Esc]", variant="default", id="btn-cancel")
                yield Button("Importar [Enter]", variant="primary", id="btn-confirm")
    
    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        path = Path(event.path)
        if path.suffix.lower() == ".xml":
            if path not in self.selected_paths:
                self.selected_paths.append(path)
                self.notify(f"Añadido: {path.name}")
    
    @on(Input.Submitted)
    def on_path_submitted(self, event: Input.Submitted) -> None:
        path = Path(event.value)
        if path.exists() and path.suffix.lower() == ".xml":
            if path not in self.selected_paths:
                self.selected_paths.append(path)
                self.notify(f"Añadido: {path.name}")
            event.input.clear()
        else:
            self.notify("Archivo no válido", severity="error")
    
    @on(Button.Pressed, "#btn-cancel")
    def on_cancel_pressed(self) -> None:
        self.dismiss(None)
    
    @on(Button.Pressed, "#btn-confirm")
    def on_confirm_pressed(self) -> None:
        self.dismiss(self.selected_paths if self.selected_paths else None)
    
    def action_cancel(self) -> None:
        self.dismiss(None)
    
    def action_confirm(self) -> None:
        self.dismiss(self.selected_paths if self.selected_paths else None)


# --- Question Item Widget ---

class QuestionItem(ListItem):
    """A list item representing a single question."""
    
    def __init__(self, question: Question) -> None:
        super().__init__()
        self.question = question
    
    def compose(self) -> ComposeResult:
        status_icon = "✓" if self.question.status == QuestionStatus.LISTA else "○"
        status_class = "lista" if self.question.status == QuestionStatus.LISTA else "revisar"
        
        yield Static(
            f"[{status_class}]{status_icon}[/] {self.question.name}",
            markup=True,
            classes="question-title"
        )


# --- Question Detail Panel ---

class QuestionDetail(Static):
    """Panel showing detailed question information with editing capabilities."""
    
    CSS = """
    QuestionDetail {
        height: 100%;
        padding: 1;
        background: $surface;
    }
    
    .field-label {
        color: $text-muted;
        margin-bottom: 0;
    }
    
    .field-value {
        margin-bottom: 1;
        padding: 0 1;
    }
    
    .answer-correct {
        color: $success;
    }
    
    .answer-wrong {
        color: $error;
    }
    
    #detail-empty {
        text-align: center;
        color: $text-muted;
    }
    
    .action-buttons {
        dock: bottom;
        height: 3;
        align: center middle;
    }
    """
    
    def __init__(self, question: Question | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._question: Question | None = question
    
    @property
    def question(self) -> Question | None:
        return self._question
    
    @question.setter
    def question(self, value: Question | None) -> None:
        self._question = value
        self.refresh_display()
    
    def compose(self) -> ComposeResult:
        if self._question is None:
            yield Static("Selecciona una pregunta", id="detail-empty")
        else:
            self._compose_question_detail()
    
    def _compose_question_detail(self) -> ComposeResult:
        q = self._question
        if q is None:
            return
        
        status_text = "✓ LISTA" if q.status == QuestionStatus.LISTA else "○ REVISAR"
        
        yield Static(f"[bold]{q.name}[/]", markup=True)
        yield Static(f"Estado: {status_text} | Categoría: {q.category_name}")
        yield Static("─" * 40)
        yield Static("[dim]Pregunta:[/]", markup=True, classes="field-label")
        yield Static(q.question_text, classes="field-value")
        
        if q.general_feedback:
            yield Static("[dim]Feedback general:[/]", markup=True, classes="field-label")
            yield Static(q.general_feedback, classes="field-value")
        
        yield Static(f"[dim]Respuestas ({q.correct_count} correctas, {q.wrong_count} incorrectas):[/]", markup=True, classes="field-label")
        
        for i, ans in enumerate(q.answers):
            icon = "✓" if ans.is_correct else "✗"
            style = "answer-correct" if ans.is_correct else "answer-wrong"
            fraction_str = f" [{ans.fraction}%]" if not ans.is_correct else ""
            yield Static(f"  {icon} {ans.text}{fraction_str}", classes=style)
    
    def refresh_display(self) -> None:
        """Refresh the display with current question."""
        self.remove_children()
        if self._question is None:
            self.mount(Static("Selecciona una pregunta", id="detail-empty"))
        else:
            q = self._question
            status_text = "✓ LISTA" if q.status == QuestionStatus.LISTA else "○ REVISAR"
            
            self.mount(Static(f"[bold]{q.name}[/]", markup=True))
            self.mount(Static(f"Estado: {status_text} | Categoría: {q.category_name}"))
            self.mount(Static("─" * 50))
            self.mount(Static("[dim]Pregunta:[/]", markup=True, classes="field-label"))
            self.mount(Static(q.question_text, classes="field-value"))
            
            if q.general_feedback:
                self.mount(Static("[dim]Feedback general:[/]", markup=True, classes="field-label"))
                self.mount(Static(q.general_feedback, classes="field-value"))
            
            self.mount(Static(f"[dim]Respuestas ({q.correct_count} correctas, {q.wrong_count} incorrectas):[/]", markup=True, classes="field-label"))
            
            for i, ans in enumerate(q.answers):
                icon = "✓" if ans.is_correct else "✗"
                style = "answer-correct" if ans.is_correct else "answer-wrong"
                fraction_str = f" [{ans.fraction}%]" if not ans.is_correct else ""
                self.mount(Static(f"  {icon} {ans.text}{fraction_str}", classes=style))


# --- Main Application ---

class MoodleQuizEditor(App):
    """Main TUI application for editing Moodle quizzes."""
    
    TITLE = "Moodle Quiz Editor v2"
    SUB_TITLE = "Terminal UI"
    
    BINDINGS = [
        Binding("ctrl+o", "open_files", "Abrir XML", show=True),
        Binding("ctrl+s", "save", "Guardar", show=True),
        Binding("ctrl+z", "undo", "Deshacer", show=True),
        Binding("ctrl+shift+z", "redo", "Rehacer", show=True),
        Binding("ctrl+y", "redo", "Rehacer", show=False),
        Binding("delete", "delete_question", "Eliminar", show=True),
        Binding("space", "toggle_status", "Cambiar estado", show=True),
        Binding("f1", "show_help", "Ayuda", show=True),
        Binding("q", "quit", "Salir", show=True),
    ]
    
    CSS = """
    Screen {
        layout: horizontal;
    }
    
    #sidebar {
        width: 35%;
        min-width: 30;
        border-right: tall $primary;
    }
    
    #main-panel {
        width: 65%;
    }
    
    #question-list-container {
        height: 1fr;
    }
    
    #stats-bar {
        dock: bottom;
        height: 3;
        background: $surface;
        border-top: solid $primary;
        padding: 0 1;
    }
    
    #filter-bar {
        dock: top;
        height: 3;
        padding: 0 1;
        background: $surface-darken-1;
    }
    
    .filter-btn {
        margin-right: 1;
    }
    
    .filter-btn-active {
        background: $primary;
    }
    
    #category-filter {
        dock: top;
        height: auto;
        max-height: 10;
        background: $surface;
        border-bottom: solid $secondary;
        display: none;
    }
    
    #category-filter.visible {
        display: block;
    }
    
    .lista {
        color: $success;
    }
    
    .revisar {
        color: $warning;
    }
    
    .question-title {
        padding: 0 1;
    }
    
    ListView > ListItem.--highlight {
        background: $primary-darken-2;
    }
    
    #detail-scroll {
        height: 100%;
    }
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.store = QuizStore()
        self.current_filter_status: QuestionStatus | None = None
        self.current_filter_category: str | None = None
        self._question_items: dict[str, QuestionItem] = {}
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            with Vertical(id="sidebar"):
                with Horizontal(id="filter-bar"):
                    yield Button("Todas", id="btn-filter-all", classes="filter-btn filter-btn-active")
                    yield Button("Lista", id="btn-filter-lista", classes="filter-btn")
                    yield Button("Revisar", id="btn-filter-revisar", classes="filter-btn")
                    yield Button("Categorías", id="btn-filter-category", classes="filter-btn")
                
                with ScrollableContainer(id="category-filter"):
                    yield Tree("Categorías", id="category-tree")
                
                with ScrollableContainer(id="question-list-container"):
                    yield ListView(id="question-list")
                
                yield Static("Total: 0 | Lista: 0 | Revisar: 0", id="stats-bar")
            
            with ScrollableContainer(id="main-panel"):
                with ScrollableContainer(id="detail-scroll"):
                    yield QuestionDetail(id="question-detail")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up listeners when app mounts."""
        self.store.add_listener(self._on_store_changed)
        self._update_stats()
    
    # --- Store Listener ---
    
    def _on_store_changed(self) -> None:
        """Called when store state changes."""
        self._refresh_question_list()
        self._update_stats()
    
    # --- UI Updates ---
    
    def _refresh_question_list(self) -> None:
        """Refresh the question list based on current filters."""
        list_view = self.query_one("#question-list", ListView)
        list_view.clear()
        self._question_items.clear()
        
        questions = self.store.get_filtered_questions(
            category_path=self.current_filter_category,
            status=self.current_filter_status
        )
        
        for q in questions:
            item = QuestionItem(q)
            self._question_items[q.id] = item
            list_view.append(item)
    
    def _update_stats(self) -> None:
        """Update the stats bar."""
        total = len(self.store.questions)
        lista = len(self.store.get_questions_by_status(QuestionStatus.LISTA))
        revisar = len(self.store.get_questions_by_status(QuestionStatus.REVISAR))
        
        dirty_marker = " *" if self.store.is_dirty else ""
        stats_text = f"Total: {total} | Lista: {lista} | Revisar: {revisar}{dirty_marker}"
        
        self.query_one("#stats-bar", Static).update(stats_text)
    
    def _get_selected_question(self) -> Question | None:
        """Get the currently selected question."""
        list_view = self.query_one("#question-list", ListView)
        if list_view.highlighted_child is not None:
            if isinstance(list_view.highlighted_child, QuestionItem):
                return list_view.highlighted_child.question
        return None
    
    def _update_category_tree(self) -> None:
        """Update the category tree with current categories."""
        tree = self.query_one("#category-tree", Tree)
        tree.clear()
        
        categories = self.store.categories
        for cat_path in categories:
            tree.root.add_leaf(cat_path.split("/")[-1], data=cat_path)
        
        tree.root.expand()
    
    # --- Event Handlers ---
    
    @on(ListView.Highlighted)
    def on_question_selected(self, event: ListView.Highlighted) -> None:
        """Handle question selection."""
        detail = self.query_one("#question-detail", QuestionDetail)
        if event.item is not None and isinstance(event.item, QuestionItem):
            detail.question = event.item.question
        else:
            detail.question = None
    
    @on(Button.Pressed, "#btn-filter-all")
    def on_filter_all(self) -> None:
        self.current_filter_status = None
        self._update_filter_buttons("all")
        self._refresh_question_list()
    
    @on(Button.Pressed, "#btn-filter-lista")
    def on_filter_lista(self) -> None:
        self.current_filter_status = QuestionStatus.LISTA
        self._update_filter_buttons("lista")
        self._refresh_question_list()
    
    @on(Button.Pressed, "#btn-filter-revisar")
    def on_filter_revisar(self) -> None:
        self.current_filter_status = QuestionStatus.REVISAR
        self._update_filter_buttons("revisar")
        self._refresh_question_list()
    
    @on(Button.Pressed, "#btn-filter-category")
    def on_filter_category(self) -> None:
        cat_filter = self.query_one("#category-filter")
        cat_filter.toggle_class("visible")
        self._update_category_tree()
    
    @on(Tree.NodeSelected)
    def on_category_selected(self, event: Tree.NodeSelected) -> None:
        """Handle category selection in tree."""
        if event.node.data:
            self.current_filter_category = event.node.data
        else:
            self.current_filter_category = None
        self._refresh_question_list()
    
    def _update_filter_buttons(self, active: str) -> None:
        """Update filter button styles."""
        for btn_id in ["btn-filter-all", "btn-filter-lista", "btn-filter-revisar"]:
            btn = self.query_one(f"#{btn_id}", Button)
            btn.remove_class("filter-btn-active")
        
        self.query_one(f"#btn-filter-{active}", Button).add_class("filter-btn-active")
    
    # --- Actions ---
    
    def action_open_files(self) -> None:
        """Open file selection dialog."""
        def handle_file_result(result: list[Path] | None) -> None:
            if result:
                try:
                    _, questions = parse_multiple_files(result)
                    self.store.add_questions(questions)
                    self._update_category_tree()
                    self.notify(f"Importadas {len(questions)} preguntas de {len(result)} archivo(s)")
                except Exception as e:
                    self.notify(f"Error al importar: {e}", severity="error")
        
        self.push_screen(FileSelectModal(start_dir=Path.cwd()), handle_file_result)
    
    def action_save(self) -> None:
        """Save to JSON state file."""
        state_file = Path.cwd() / "quiz_state.json"
        try:
            self.store.save_to_file(state_file)
            self.notify(f"Guardado en {state_file.name}")
        except Exception as e:
            self.notify(f"Error al guardar: {e}", severity="error")
    
    def action_undo(self) -> None:
        """Undo last action."""
        description = self.store.undo()
        if description:
            self.notify(f"Deshacer: {description}")
            # Refresh detail view
            detail = self.query_one("#question-detail", QuestionDetail)
            detail.refresh_display()
        else:
            self.notify("Nada que deshacer")
    
    def action_redo(self) -> None:
        """Redo last undone action."""
        description = self.store.redo()
        if description:
            self.notify(f"Rehacer: {description}")
            detail = self.query_one("#question-detail", QuestionDetail)
            detail.refresh_display()
        else:
            self.notify("Nada que rehacer")
    
    def action_delete_question(self) -> None:
        """Delete the selected question."""
        question = self._get_selected_question()
        if question:
            self.store.delete_question(question.id)
            self.notify(f"Eliminada: {question.name[:30]}...")
    
    def action_toggle_status(self) -> None:
        """Toggle the status of the selected question."""
        question = self._get_selected_question()
        if question:
            self.store.toggle_status(question.id)
            # Refresh detail
            detail = self.query_one("#question-detail", QuestionDetail)
            updated_q = self.store.get_question(question.id)
            detail.question = updated_q
            
            new_status = "Lista" if updated_q and updated_q.status == QuestionStatus.LISTA else "Revisar"
            self.notify(f"Estado: {new_status}")
    
    def action_show_help(self) -> None:
        """Show help overlay."""
        help_text = """
[bold]Atajos de teclado:[/]

Ctrl+O    Abrir archivos XML
Ctrl+S    Guardar estado
Ctrl+Z    Deshacer
Ctrl+Y    Rehacer
Delete    Eliminar pregunta
Space     Cambiar estado (Lista/Revisar)
↑/↓       Navegar preguntas
Q         Salir
"""
        self.notify(help_text, timeout=10)
    
    def action_quit(self) -> None:
        """Quit the application."""
        if self.store.is_dirty:
            self.notify("Hay cambios sin guardar. Pulsa Q de nuevo para salir.")
            # Simple dirty check - could be improved with confirmation modal
        self.exit()


def main() -> None:
    """Entry point for the application."""
    app = MoodleQuizEditor()
    app.run()


if __name__ == "__main__":
    main()
