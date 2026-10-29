"""Tests for the entry point's cleaning of the snap paths a launcher hands down to GTK."""

from __future__ import annotations

import os
from pathlib import Path
import sys
import unittest


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


from main import snap_leak_fixes  # noqa: E402

HOME = Path("/home/user")

# A terminal opened by VS Code installed as a snap (revision 271), as observed on Ubuntu 26.04.
VSCODE_SNAP_TERMINAL = {
    "GIO_MODULE_DIR": "/home/user/snap/code/common/.cache/gio-modules",
    "GSETTINGS_SCHEMA_DIR": "/home/user/snap/code/271/.local/share/glib-2.0/schemas",
    "GTK_EXE_PREFIX": "/snap/code/271/usr",
    "GTK_IM_MODULE_FILE": "/home/user/snap/code/common/.cache/immodules/immodules.cache",
    "GTK_PATH": "/snap/code/271/usr/lib/x86_64-linux-gnu/gtk-3.0",
    "LOCPATH": "/snap/code/271/usr/lib/locale",
    "XDG_CONFIG_DIRS": "/etc/xdg/xdg-ubuntu:/etc/xdg",
    "XDG_DATA_DIRS": (
        "/home/user/snap/code/271/.local/share:/home/user/snap/code/271:/snap/code/271/usr/share"
        ":/usr/share/ubuntu:/usr/share/gnome:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop"
    ),
    "PATH": "/home/user/.local/bin:/usr/bin:/snap/bin",
}


class SnapLeakFixesTests(unittest.TestCase):

    def test_a_vscode_snap_terminal_gets_the_system_paths_back(self) -> None:
        fixes = snap_leak_fixes(VSCODE_SNAP_TERMINAL, HOME)

        self.assertEqual(fixes, {
            "XDG_DATA_DIRS": "/usr/share/ubuntu:/usr/share/gnome:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop",
            "GSETTINGS_SCHEMA_DIR": None,
            "GIO_MODULE_DIR": None,
            "GTK_PATH": None,
            "GTK_EXE_PREFIX": None,
            "GTK_IM_MODULE_FILE": None,
            "LOCPATH": None,
        })

    def test_an_environment_without_snap_paths_is_left_alone(self) -> None:
        environment = {
            "XDG_DATA_DIRS": "/usr/share/ubuntu:/usr/local/share/:/usr/share/:/var/lib/snapd/desktop",
            "LOCPATH": "/opt/locales",
        }

        self.assertEqual(snap_leak_fixes(environment, HOME), {})


if __name__ == '__main__':
    unittest.main()
