"""Shared theme helpers for editor views."""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

THEME_SYSTEM = "system"
THEME_LIGHT = "light"
THEME_DARK = "dark"

THEME_OPTIONS: tuple[tuple[str, str], ...] = (
    (THEME_SYSTEM, "Sistema"),
    (THEME_LIGHT, "Claro"),
    (THEME_DARK, "Oscuro"),
)

_LIGHT_COLORS = {
    "window": "#F5F6F8",
    "text": "#1F2328",
    "muted": "#5F6B76",
    "base": "#FFFFFF",
    "alternate": "#EEF1F4",
    "button": "#FFFFFF",
    "button_text": "#1F2328",
    "border": "#C9D1D9",
    "highlight": "#2F6FEB",
    "highlighted_text": "#FFFFFF",
    "correct_frame": "#E8F5E9",
    "correct_border": "#2E7D32",
    "correct_input": "#F1F8E9",
    "correct_input_border": "#81C784",
    "correct_text": "#1B5E20",
    "incorrect_frame": "#F7F7F8",
    "incorrect_border": "#CDD3D8",
    "incorrect_input": "#FFFFFF",
    "incorrect_input_border": "#D8DEE4",
    "incorrect_text": "#1F2328",
}

_DARK_COLORS = {
    "window": "#1B1F24",
    "text": "#E6EDF3",
    "muted": "#9BA7B4",
    "base": "#22272E",
    "alternate": "#2D333B",
    "button": "#2D333B",
    "button_text": "#E6EDF3",
    "border": "#4B5563",
    "highlight": "#539BF5",
    "highlighted_text": "#0D1117",
    "correct_frame": "#173026",
    "correct_border": "#58A06A",
    "correct_input": "#10241C",
    "correct_input_border": "#3FB950",
    "correct_text": "#D7FBE8",
    "incorrect_frame": "#2A3038",
    "incorrect_border": "#59636E",
    "incorrect_input": "#1F242C",
    "incorrect_input_border": "#4B5563",
    "incorrect_text": "#E6EDF3",
}


def _theme_colors(theme_variant: str) -> dict[str, str]:
    return _DARK_COLORS if theme_variant == THEME_DARK else _LIGHT_COLORS


def _relative_luminance(color: QColor) -> float:
    return (0.2126 * color.redF()) + (0.7152 * color.greenF()) + (0.0722 * color.blueF())


def palette_is_dark(palette: QPalette) -> bool:
    return _relative_luminance(palette.color(QPalette.ColorRole.Window)) < 0.5


def effective_theme_variant(theme_mode: str, palette: QPalette | None = None) -> str:
    if theme_mode == THEME_DARK:
        return THEME_DARK
    if theme_mode == THEME_LIGHT:
        return THEME_LIGHT
    active_palette = palette
    if active_palette is None:
        app = QApplication.instance()
        active_palette = app.palette() if app is not None else None
    if active_palette is not None and palette_is_dark(active_palette):
        return THEME_DARK
    return THEME_LIGHT


def build_light_palette() -> QPalette:
    colors = _LIGHT_COLORS
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(colors["window"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(colors["base"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alternate"]))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["base"]))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(colors["button"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["button_text"]))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Link, QColor(colors["highlight"]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["highlight"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["highlighted_text"]))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["muted"]))
    return palette


def build_dark_palette() -> QPalette:
    colors = _DARK_COLORS
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(colors["window"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(colors["base"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alternate"]))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["base"]))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(colors["button"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["button_text"]))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Link, QColor(colors["highlight"]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["highlight"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["highlighted_text"]))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["muted"]))
    return palette


def apply_app_theme(
    app: QApplication,
    theme_mode: str,
    system_palette: QPalette,
    system_style_name: str,
) -> str:
    if theme_mode == THEME_SYSTEM:
        app.setStyle(system_style_name)
        app.setPalette(QPalette(system_palette))
        app.setStyleSheet("")
        return effective_theme_variant(THEME_SYSTEM, app.palette())

    app.setStyle("Fusion")
    if theme_mode == THEME_DARK:
        app.setPalette(build_dark_palette())
    else:
        app.setPalette(build_light_palette())

    colors = _theme_colors(theme_mode)
    app.setStyleSheet(
        "\n".join((
            "QToolTip {",
            f"    color: {colors['text']};",
            f"    background-color: {colors['base']};",
            f"    border: 1px solid {colors['border']};",
            "    padding: 4px;",
            "}",
        ))
    )
    return theme_mode


def _font_rule(font_size: int | None) -> str:
    return f"    font-size: {font_size}pt;" if font_size is not None else ""


def build_text_edit_style(theme_variant: str, font_size: int | None = None) -> str:
    colors = _theme_colors(theme_variant)
    rules = [
        "QTextEdit {",
        f"    color: {colors['text']};",
        f"    background-color: {colors['base']};",
        f"    border: 1px solid {colors['border']};",
        "    border-radius: 4px;",
        "    padding: 4px;",
    ]
    if font_size is not None:
        rules.append(_font_rule(font_size))
    rules.append("}")
    return "\n".join(rules)


def build_line_edit_style(theme_variant: str, font_size: int | None = None) -> str:
    colors = _theme_colors(theme_variant)
    rules = [
        "QLineEdit {",
        f"    color: {colors['text']};",
        f"    background-color: {colors['base']};",
        f"    border: 1px solid {colors['border']};",
        "    border-radius: 4px;",
        "    padding: 4px 6px;",
    ]
    if font_size is not None:
        rules.append(_font_rule(font_size))
    rules.append("}")
    return "\n".join(rules)


def build_muted_label_style(theme_variant: str) -> str:
    colors = _theme_colors(theme_variant)
    return f"color: {colors['muted']};"


def build_answer_frame_style(theme_variant: str, is_correct: bool) -> str:
    colors = _theme_colors(theme_variant)
    background_key = "correct_frame" if is_correct else "incorrect_frame"
    border_key = "correct_border" if is_correct else "incorrect_border"
    border_width = "2px" if is_correct else "1px"
    return "\n".join((
        "QFrame {",
        f"    border: {border_width} solid {colors[border_key]};",
        f"    background-color: {colors[background_key]};",
        "    border-radius: 6px;",
        "}",
    ))


def build_answer_editor_style(theme_variant: str, is_correct: bool, font_size: int | None = None) -> str:
    colors = _theme_colors(theme_variant)
    if is_correct:
        background = colors["correct_input"]
        border = colors["correct_input_border"]
        text = colors["correct_text"]
    else:
        background = colors["incorrect_input"]
        border = colors["incorrect_input_border"]
        text = colors["incorrect_text"]

    rules = [
        "QTextEdit {",
        f"    color: {text};",
        f"    background-color: {background};",
        f"    border: 1px solid {border};",
        "    border-radius: 4px;",
        "    padding: 4px;",
    ]
    if font_size is not None:
        rules.append(_font_rule(font_size))
    rules.append("}")
    return "\n".join(rules)