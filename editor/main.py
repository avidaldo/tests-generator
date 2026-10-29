"""
Moodle Quiz Editor v3 - Entry Point

Run with: uv run python editor/main.py
"""

import os
import sys
from collections.abc import Mapping
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

# Where a snap-packaged launcher (VS Code installed as a snap, and every terminal it opens) points GTK and GLib at its
# own older copies of GSettings schemas, GIO and GTK modules and locales. GTK reads them when QApplication starts.
_SNAP_LEAK_VARIABLES = (
    "XDG_DATA_DIRS",
    "XDG_CONFIG_DIRS",
    "GSETTINGS_SCHEMA_DIR",
    "GIO_MODULE_DIR",
    "GTK_PATH",
    "GTK_EXE_PREFIX",
    "GTK_IM_MODULE_FILE",
    "GDK_PIXBUF_MODULE_FILE",
    "GDK_PIXBUF_MODULEDIR",
    "LOCPATH",
)


def snap_leak_fixes(environment: Mapping[str, str], home: Path) -> dict[str, str | None]:
    """Return the GTK variables to clean of inherited snap paths: name -> new value, or None to unset it.

    The editor never runs inside a snap, so every snap path in these variables comes from whatever launched it.
    Left in place, VS Code's snap shows GTK an old org.gnome.desktop.interface schema without 'font-antialiasing';
    GTK on Wayland then reads 'antialiasing' from org.gnome.settings-daemon.plugins.xsettings, which GNOME 50's
    schema no longer has, and GLib aborts the process.
    """
    snap_roots = ("/snap/", "/var/snap/", "/var/lib/snapd/snap/", f"{home}/snap/")
    fixes: dict[str, str | None] = {}
    for name in _SNAP_LEAK_VARIABLES:
        if name not in environment:
            continue
        paths = environment[name].split(os.pathsep)
        kept_paths = [path for path in paths if not path.startswith(snap_roots)]
        if kept_paths != paths:
            fixes[name] = os.pathsep.join(kept_paths) if kept_paths else None
    return fixes


def main():
    for name, value in snap_leak_fixes(os.environ, Path.home()).items():
        if value is None:
            del os.environ[name]
        else:
            os.environ[name] = value

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
