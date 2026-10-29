"""Learner-facing HTML: visible text for analysis, and a whitelist sanitizer for storage and export.

Qt's QTextEdit.toHtml() returns a whole document (DOCTYPE, <head> with a stylesheet, a styled <body>) and
turns semantic tags into styled spans: <code> becomes <span style="font-family:'monospace'">, <strong> a span
with font-weight:700, and every line of a <pre> its own <pre>. sanitize() maps those spans back to semantic
tags, merges the split <pre> blocks and drops everything else, so plain semantic HTML reaches Moodle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
import re


_WHITESPACE = re.compile(r"\s+")
_TAG_NAME = re.compile(r"<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)")
_STYLE_ATTRIBUTE = re.compile(r"\sstyle\s*=", re.IGNORECASE)

# Visible-text extraction (unchanged from the editor's original diagnostics).
_BLOCK_TAGS = {"br", "div", "li", "p", "tr", "td", "th", "hr", "section", "article"}
_IGNORED_TAGS = {"head", "script", "style", "title"}

# Sanitizer whitelist: these tags survive, without attributes (a link keeps its href, an image src and alt).
_KEPT_TAGS = {
    "p", "br", "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td",
    "strong", "em", "u", "code", "pre", "sub", "sup", "a", "img",
}
_RENAMED_TAGS = {"b": "strong", "i": "em"}
_DROPPED_TAGS = {"head", "style", "script", "title", "meta", "link"}
_VOID_TAGS = {"br", "hr", "img", "meta", "link", "input"}
_CELL_TAGS = {"td", "th"}
_MONOSPACE_FAMILIES = ("monospace", "courier", "mono")

ALLOWED_TAGS = frozenset(_KEPT_TAGS | set(_RENAMED_TAGS))


class _VisibleTextExtractor(HTMLParser):
    """Extract visible text while ignoring rich-text boilerplate."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        lowered_tag = tag.lower()
        if lowered_tag in _IGNORED_TAGS:
            self._ignored_depth += 1
            return
        if lowered_tag in _BLOCK_TAGS:
            self._chunks.append(" ")

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        lowered_tag = tag.lower()
        if lowered_tag in _IGNORED_TAGS and self._ignored_depth > 0:
            self._ignored_depth -= 1
            return
        if lowered_tag in _BLOCK_TAGS:
            self._chunks.append(" ")

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._ignored_depth == 0 and data:
            self._chunks.append(data)

    def get_text(self) -> str:
        return "".join(self._chunks)


def visible_text(html_text: str) -> str:
    """Return the normalized visible text of a rich-text HTML string."""
    if not html_text:
        return ""

    extractor = _VisibleTextExtractor()
    extractor.feed(html_text)
    extractor.close()
    return _WHITESPACE.sub(" ", extractor.get_text()).strip()


def is_qt_document(html_text: str) -> bool:
    """Tell whether the text is a whole Qt rich-text document rather than an HTML fragment."""
    return 'name="qrichtext"' in html_text or html_text.lstrip().upper().startswith("<!DOCTYPE HTML PUBLIC")


def markup_problems(html_text: str) -> list[str]:
    """Describe what sanitize() would remove: a Qt document, inline styles, tags outside the whitelist."""
    problems: list[str] = []
    if is_qt_document(html_text):
        problems.append("Qt rich-text document")
    if _STYLE_ATTRIBUTE.search(html_text):
        problems.append("inline style")
    unknown_tags = sorted({name.lower() for name in _TAG_NAME.findall(html_text)} - ALLOWED_TAGS)
    if unknown_tags:
        problems.append("tags " + ", ".join(f"<{name}>" for name in unknown_tags))
    return problems


@dataclass
class _Element:
    tag: str
    attrs: dict[str, str]
    children: list[_Element | str] = field(default_factory=list)


class _TreeBuilder(HTMLParser):
    """Build a small element tree; unmatched end tags are ignored, unclosed elements end with their parent."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Element("#root", {})
        self._open: list[_Element] = [self.root]

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        element = _Element(tag.lower(), {name.lower(): value or "" for name, value in attrs})
        self._open[-1].children.append(element)
        if element.tag not in _VOID_TAGS:
            self._open.append(element)

    def handle_startendtag(self, tag: str, attrs) -> None:  # type: ignore[override]
        self._open[-1].children.append(_Element(tag.lower(), {name.lower(): value or "" for name, value in attrs}))

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        lowered_tag = tag.lower()
        for depth in range(len(self._open) - 1, 0, -1):
            if self._open[depth].tag == lowered_tag:
                del self._open[depth:]
                return

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        self._open[-1].children.append(data)


def sanitize(html_text: str) -> str:
    """Reduce rich text to whitelisted semantic HTML. Idempotent: sanitizing clean HTML returns it unchanged."""
    if not html_text:
        return ""

    builder = _TreeBuilder()
    builder.feed(html_text)
    builder.close()
    return _render_children(builder.root.children, in_pre=False, in_cell=False).strip()


def _render_children(children: list[_Element | str], *, in_pre: bool, in_cell: bool) -> str:
    parts: list[str] = []
    pending_pre_lines: list[str] = []
    for child in children:
        if isinstance(child, _Element) and child.tag == "pre":
            pending_pre_lines.append(_render_children(child.children, in_pre=True, in_cell=in_cell))
            continue
        if pending_pre_lines and isinstance(child, str) and not child.strip():
            continue  # the newline Qt writes between the <pre> blocks of one code listing
        if pending_pre_lines:
            parts.append("<pre>" + "\n".join(pending_pre_lines) + "</pre>")
            pending_pre_lines = []
        parts.append(_render(child, in_pre=in_pre, in_cell=in_cell))
    if pending_pre_lines:
        parts.append("<pre>" + "\n".join(pending_pre_lines) + "</pre>")
    return "".join(parts)


def _render(node: _Element | str, *, in_pre: bool, in_cell: bool) -> str:
    if isinstance(node, str):
        if in_pre:
            return escape(node, quote=False)
        if "\n" in node and not node.strip():
            return ""  # layout newline between blocks
        return escape(_WHITESPACE.sub(" ", node), quote=False)

    tag = _RENAMED_TAGS.get(node.tag, node.tag)
    if tag in _DROPPED_TAGS:
        return ""
    if tag == "br":
        return "<br>"
    if tag == "img":
        source = node.attrs.get("src", "")
        return f'<img src="{escape(source)}" alt="{escape(node.attrs.get("alt", ""))}">' if source else ""

    inner = _render_children(node.children, in_pre=in_pre, in_cell=in_cell or tag in _CELL_TAGS)
    if tag == "span":
        return _wrap(inner, _span_tags(node.attrs.get("style", ""), in_pre))
    if tag == "p":
        if not visible_text(inner) and "<img" not in inner:
            return ""  # Qt's empty paragraphs
        return inner if in_cell else f"<p>{inner}</p>"
    if tag == "code" and in_pre:
        return inner
    if tag == "a":
        href = node.attrs.get("href", "")
        if href.startswith(("http://", "https://", "mailto:")):
            return f'<a href="{escape(href)}">{inner}</a>'
        return inner
    if tag in _KEPT_TAGS:
        return f"<{tag}>{inner}</{tag}>"
    return inner  # html, body, div, font and any unknown tag: keep the content only


def _span_tags(style: str, in_pre: bool) -> list[str]:
    declarations: dict[str, str] = {}
    for declaration in style.split(";"):
        name, _, value = declaration.partition(":")
        declarations[name.strip().lower()] = value.strip().lower()

    tags: list[str] = []
    if not in_pre and any(family in declarations.get("font-family", "") for family in _MONOSPACE_FAMILIES):
        tags.append("code")
    weight = declarations.get("font-weight", "")
    if weight == "bold" or (weight.isdigit() and int(weight) >= 600):
        tags.append("strong")
    if declarations.get("font-style") == "italic":
        tags.append("em")
    if "underline" in declarations.get("text-decoration", ""):
        tags.append("u")
    return tags


def _wrap(inner: str, tags: list[str]) -> str:
    if not inner:
        return ""
    for tag in tags:
        inner = f"<{tag}>{inner}</{tag}>"
    return inner
