#!/usr/bin/env python3
"""Deprecated: use `uv run qb export <input.json> <output.xml>` (same arguments).

Kept so that existing commands keep working until the documentation cleanup; it delegates to qb.export,
the single Moodle XML writer shared with the editor.
"""

import sys

from qb.cli import main


if __name__ == "__main__":
    sys.exit(main(["export", *sys.argv[1:]]))
