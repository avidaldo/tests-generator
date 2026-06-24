"""Lightweight UI internationalization for the editor.

Clean separation: UI code calls ``tr("some.key")`` and never embeds user-facing
literals. Catalogs live in ``catalogs.py`` (one dict per language). The active
language is a module-level setting chosen at startup from QSettings.

Spanish (``es``) is the default and also the fallback when a key is missing from
another catalog, so partial translations degrade gracefully instead of showing keys.
"""

from .catalogs import CATALOGS

DEFAULT_LANGUAGE = "es"
_FALLBACK_LANGUAGE = "es"

_current_language = DEFAULT_LANGUAGE


def available_languages() -> list[tuple[str, str]]:
    """Return (code, native-name) pairs for every available language."""
    return [("es", "Español"), ("en", "English")]


def current_language() -> str:
    return _current_language


def set_language(language: str) -> None:
    """Set the active UI language. Unknown codes fall back to the default."""
    global _current_language
    _current_language = language if language in CATALOGS else DEFAULT_LANGUAGE


def tr(key: str, **kwargs: object) -> str:
    """Translate ``key`` for the active language.

    Falls back to the Spanish catalog and finally to the key itself. Any keyword
    arguments are applied with ``str.format`` so callers can interpolate values.
    """
    catalog = CATALOGS.get(_current_language, {})
    text = catalog.get(key)
    if text is None:
        text = CATALOGS.get(_FALLBACK_LANGUAGE, {}).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
