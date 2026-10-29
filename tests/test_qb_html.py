"""Tests for qb.html: visible text and the whitelist sanitizer."""

from qb.html import is_qt_document, markup_problems, sanitize, visible_text


# What QTextEdit.toHtml() returned (PyQt6 6.11) after setHtml() of a paragraph with <code>, <strong>, <em> and
# entities, a two-line <pre>, a list and a table with a header row.
QT_DOCUMENT = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
</style></head><body style=" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;">
<p style=" margin-top:12px; margin-bottom:12px;">Texto <span style=" font-family:'monospace';">np.all(X[:, -1, 1] == 0)</span> y <span style=" font-weight:700;">negrita</span> y <span style=" font-style:italic;">cursiva</span> &amp; 3 &lt; 4</p>
<pre style=" margin-top:12px; margin-bottom:0px;"><span style=" font-family:'monospace';">for i in range(3):</span></pre>
<pre style=" margin-top:0px; margin-bottom:12px;"><span style=" font-family:'monospace';">    print(i)</span></pre>
<ul style="margin-top: 0px; -qt-list-indent: 1;">
<li style=" margin-top:12px;">uno</li>
<li style=" margin-top:0px;">dos</li></ul>
<table border="0" style=" margin-top:0px;" cellspacing="2" cellpadding="0">
<tr>
<td>
<p align="center" style=" margin-top:0px;"><span style=" font-weight:700;">A</span></p></td>
<td>
<p align="center" style=" margin-top:0px;"><span style=" font-weight:700;">B</span></p></td></tr>
<tr>
<td>
<p style=" margin-top:0px;">1</p></td>
<td>
<p style=" margin-top:0px;">2</p></td></tr></table>
<p style="-qt-paragraph-type:empty; margin-top:0px;"><br /></p></body></html>"""

CLEAN_HTML = (
    "<p>Texto <code>np.all(X[:, -1, 1] == 0)</code> y <strong>negrita</strong> y <em>cursiva</em> &amp; 3 &lt; 4</p>"
    "<pre>for i in range(3):\n    print(i)</pre>"
    "<ul><li>uno</li><li>dos</li></ul>"
    "<table><tr><td><strong>A</strong></td><td><strong>B</strong></td></tr><tr><td>1</td><td>2</td></tr></table>"
)


def test_sanitize_turns_a_qt_document_into_semantic_html() -> None:
    assert sanitize(QT_DOCUMENT) == CLEAN_HTML


def test_sanitize_is_idempotent() -> None:
    assert sanitize(CLEAN_HTML) == CLEAN_HTML


def test_sanitize_keeps_only_whitelisted_tags_and_safe_attributes() -> None:
    html_text = (
        '<div class="x"><p style="color:red">Ver <a href="https://scikit-learn.org" onclick="x()">docs</a>'
        ' y <a href="javascript:alert(1)">esto</a> <font color="red">rojo</font></p></div>'
    )

    assert sanitize(html_text) == '<p>Ver <a href="https://scikit-learn.org">docs</a> y esto rojo</p>'


def test_visible_text_ignores_the_rich_text_wrapper() -> None:
    assert visible_text(QT_DOCUMENT).startswith("Texto np.all(X[:, -1, 1] == 0) y negrita")


def test_markup_problems_names_what_sanitize_would_remove() -> None:
    assert is_qt_document(QT_DOCUMENT)
    assert markup_problems(QT_DOCUMENT)[:2] == ["Qt rich-text document", "inline style"]
    assert markup_problems('<p><span class="x">a</span></p>') == ["tags <span>"]
    assert markup_problems(CLEAN_HTML) == []
