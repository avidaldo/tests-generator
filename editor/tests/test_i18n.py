"""Unit tests for the UI i18n layer."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


EDITOR_DIR = Path(__file__).resolve().parents[1]
if str(EDITOR_DIR) not in sys.path:
    sys.path.insert(0, str(EDITOR_DIR))


import i18n  # noqa: E402
from i18n.catalogs import EN, ES  # noqa: E402


class I18nTests(unittest.TestCase):
    def setUp(self) -> None:
        self.addCleanup(i18n.set_language, i18n.DEFAULT_LANGUAGE)

    def test_spanish_and_english_catalogs_share_the_same_keys(self) -> None:
        self.assertEqual(set(ES.keys()), set(EN.keys()))

    def test_tr_returns_language_specific_string(self) -> None:
        i18n.set_language("es")
        self.assertEqual(i18n.tr("menu.file"), "Archivo")
        i18n.set_language("en")
        self.assertEqual(i18n.tr("menu.file"), "File")

    def test_tr_formats_placeholders(self) -> None:
        i18n.set_language("en")
        self.assertIn("3", i18n.tr("validate.need_one_correct", count=3))

    def test_unknown_key_falls_back_to_key(self) -> None:
        self.assertEqual(i18n.tr("does.not.exist"), "does.not.exist")

    def test_unknown_language_falls_back_to_default(self) -> None:
        i18n.set_language("fr")
        self.assertEqual(i18n.current_language(), i18n.DEFAULT_LANGUAGE)


if __name__ == "__main__":
    unittest.main()
