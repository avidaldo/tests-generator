"""
Moodle Quiz Editor v3 - Entry Point

Run with: uv run python editor/main.py
"""

import sys
from pathlib import Path

# Add editor directory to path for imports
_editor_dir = Path(__file__).parent
if str(_editor_dir) not in sys.path:
    sys.path.insert(0, str(_editor_dir))

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication
from i18n import DEFAULT_LANGUAGE, set_language
from views.main_window import MainWindow
from views.theme import THEME_SYSTEM, apply_app_theme


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Moodle Quiz Editor")
    app.setOrganizationName("avidaldo")

    settings = QSettings()
    set_language(settings.value("language", DEFAULT_LANGUAGE, type=str))
    theme_mode = settings.value("theme_mode", THEME_SYSTEM, type=str)
    system_palette = QPalette(app.palette())
    style = app.style()
    system_style_name = style.objectName() if style is not None else "Fusion"
    apply_app_theme(app, theme_mode, system_palette, system_style_name)

    window = MainWindow(
        theme_mode=theme_mode,
        system_palette=system_palette,
        system_style_name=system_style_name,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
