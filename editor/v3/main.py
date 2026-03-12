"""
Moodle Quiz Editor v3 - Entry Point

Run with: uv run python moodle-tests/editor/v3/main.py
"""

import sys
from pathlib import Path

# Add v3 directory to path for imports
_v3_dir = Path(__file__).parent
if str(_v3_dir) not in sys.path:
    sys.path.insert(0, str(_v3_dir))

from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Moodle Quiz Editor")
    app.setOrganizationName("avidaldo")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
