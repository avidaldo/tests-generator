"""UI string catalogs, one dict per language.

Keys are stable, semantic identifiers (e.g. ``menu.file``). Spanish is the source
language; English mirrors the same keys. Add new strings here, never inline in views.
"""

ES = {
    # Menus
    "menu.file": "Archivo",
    "menu.edit": "Editar",
    "menu.view": "Vista",
    "menu.add": "Añadir",
    "menu.legacy": "Legado",
    "menu.export": "Exportar",
    "menu.theme": "Tema",
    "menu.language": "Idioma",
    "menu.open_recent": "Abrir reciente",
    # File actions
    "action.new_session": "Nueva sesión de revisión",
    "action.open_session": "Abrir sesión de revisión...",
    "action.save_as": "Guardar sesión como...",
    "action.session_notes": "Notas de sesión...",
    "action.add_stage3": "Archivos Stage 3...",
    "action.add_stage3_folder": "Carpeta Stage 3...",
    "action.import_xml": "Banco XML de Moodle...",
    "action.export_xml": "Moodle XML...",
    "action.export_xml_easy": "Moodle XML (solo fáciles)...",
    "action.quit": "Salir",
    # Edit actions
    "action.undo": "Deshacer",
    "action.redo": "Rehacer",
    "action.delete_question": "Eliminar pregunta",
    # View actions
    "action.zoom_in": "Aumentar zoom",
    "action.zoom_out": "Reducir zoom",
    "action.reset_zoom": "Restablecer zoom",
    # Recent submenu
    "recent.empty": "(sin sesiones recientes)",
    "recent.clear": "Borrar lista",
    # Theme labels
    "theme.system": "Sistema",
    "theme.light": "Claro",
    "theme.dark": "Oscuro",
    # Toolbar
    "toolbar.main": "Principal",
    "toolbar.add_stage3": "Añadir Stage 3",
    "toolbar.add_folder": "Añadir carpeta",
    "toolbar.open_session": "Abrir sesión",
    "toolbar.session_notes": "Notas de sesión",
    # Filters sidebar
    "filters.group": "Filtros",
    "filter.all": "Todas",
    "filter.pending": "● Pendiente",
    "filter.review": "↻ Revisar",
    "filter.ready": "✓ Lista",
    "filter.ready_easy": "★ Lista fácil",
    "group.categories": "Categorías",
    "group.questions": "Preguntas",
    # Stats bar
    "stats.summary": "Total: {total} | ⋯ Pendiente: {pending} | ↻ Revisar: {review} | ✓ Lista: {ready} | ★ Fácil: {easy} | ! Warnings: {warnings}",
    # Detail panel
    "detail.select_question": "Selecciona una pregunta",
    "btn.pending": "⋯ Pendiente",
    "btn.review": "↻ Revisar",
    "btn.ready": "✓ Lista",
    "btn.easy": "★ Fácil",
    "btn.delete": "🗑 Eliminar",
    "btn.purge": "🗑 Eliminar no marcados",
    "btn.hide_feedback": "💬 Ocultar Feedback",
    "btn.show_feedback": "💬 Mostrar Feedback",
    "label.answers": "Respuestas",
    "status.ready": "Estado: ✓ LISTA",
    "status.review": "Estado: ↻ REVISAR",
    "status.pending": "Estado: ⋯ PENDIENTE",
    "status.ready_easy_suffix": " (★ Fácil)",
    # Tooltips / hints
    "tooltip.ready": "Marcar como revisada y lista para el examen",
    "tooltip.review": "Marcar para revisión posterior",
    "tooltip.pending": "Marcar como pendiente de revisar",
    "tooltip.ready_incomplete": "Formato incompleto: {errors}",
    "tooltip.purge_ready": "Eliminar todos los distractores no marcados",
    "tooltip.purge_blocked": "Marca al menos 3 distractores como correcto-revisado para poder usar esto",
    "hint.not_ready": "No se puede marcar como LISTA: {errors}",
    "validate.need_one_correct": "Debe haber exactamente 1 respuesta correcta (actual: {count}).",
    "validate.need_three_distractors": "Debe haber exactamente 3 distractores (respuestas incorrectas) (actual: {count}).",
    # Language change
    "language.restart_title": "Idioma",
    "language.restart_body": "Reinicia la aplicación para aplicar el idioma seleccionado.",
}

EN = {
    # Menus
    "menu.file": "File",
    "menu.edit": "Edit",
    "menu.view": "View",
    "menu.add": "Add",
    "menu.legacy": "Legacy",
    "menu.export": "Export",
    "menu.theme": "Theme",
    "menu.language": "Language",
    "menu.open_recent": "Open recent",
    # File actions
    "action.new_session": "New review session",
    "action.open_session": "Open review session...",
    "action.save_as": "Save session as...",
    "action.session_notes": "Session notes...",
    "action.add_stage3": "Stage 3 files...",
    "action.add_stage3_folder": "Stage 3 folder...",
    "action.import_xml": "Moodle XML bank...",
    "action.export_xml": "Moodle XML...",
    "action.export_xml_easy": "Moodle XML (easy only)...",
    "action.quit": "Quit",
    # Edit actions
    "action.undo": "Undo",
    "action.redo": "Redo",
    "action.delete_question": "Delete question",
    # View actions
    "action.zoom_in": "Zoom in",
    "action.zoom_out": "Zoom out",
    "action.reset_zoom": "Reset zoom",
    # Recent submenu
    "recent.empty": "(no recent sessions)",
    "recent.clear": "Clear list",
    # Theme labels
    "theme.system": "System",
    "theme.light": "Light",
    "theme.dark": "Dark",
    # Toolbar
    "toolbar.main": "Main",
    "toolbar.add_stage3": "Add Stage 3",
    "toolbar.add_folder": "Add folder",
    "toolbar.open_session": "Open session",
    "toolbar.session_notes": "Session notes",
    # Filters sidebar
    "filters.group": "Filters",
    "filter.all": "All",
    "filter.pending": "● Pending",
    "filter.review": "↻ Review",
    "filter.ready": "✓ Ready",
    "filter.ready_easy": "★ Ready easy",
    "group.categories": "Categories",
    "group.questions": "Questions",
    # Stats bar
    "stats.summary": "Total: {total} | ⋯ Pending: {pending} | ↻ Review: {review} | ✓ Ready: {ready} | ★ Easy: {easy} | ! Warnings: {warnings}",
    # Detail panel
    "detail.select_question": "Select a question",
    "btn.pending": "⋯ Pending",
    "btn.review": "↻ Review",
    "btn.ready": "✓ Ready",
    "btn.easy": "★ Easy",
    "btn.delete": "🗑 Delete",
    "btn.purge": "🗑 Delete unmarked",
    "btn.hide_feedback": "💬 Hide feedback",
    "btn.show_feedback": "💬 Show feedback",
    "label.answers": "Answers",
    "status.ready": "Status: ✓ READY",
    "status.review": "Status: ↻ REVIEW",
    "status.pending": "Status: ⋯ PENDING",
    "status.ready_easy_suffix": " (★ Easy)",
    # Tooltips / hints
    "tooltip.ready": "Mark as reviewed and ready for the exam",
    "tooltip.review": "Flag for later review",
    "tooltip.pending": "Mark as pending review",
    "tooltip.ready_incomplete": "Incomplete format: {errors}",
    "tooltip.purge_ready": "Delete every distractor that is not marked",
    "tooltip.purge_blocked": "Mark at least 3 distractors as correct-reviewed to use this",
    "hint.not_ready": "Cannot mark as READY: {errors}",
    "validate.need_one_correct": "There must be exactly 1 correct answer (currently: {count}).",
    "validate.need_three_distractors": "There must be exactly 3 distractors (incorrect answers) (currently: {count}).",
    # Language change
    "language.restart_title": "Language",
    "language.restart_body": "Restart the application to apply the selected language.",
}

CATALOGS = {"es": ES, "en": EN}
