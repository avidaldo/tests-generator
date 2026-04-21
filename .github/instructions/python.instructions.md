---
name: Python Standards
description: Coding conventions and tooling for Python files in this project (Python ≥3.13).
applyTo: "**/*.py"
---

Canonical Python guidelines live in [AGENTS.md](../../AGENTS.md). Key rules for quick reference:

- Python ≥3.13. Modern type-hint syntax: `str | None`, `list[str]`, `dict[str, int]`, `tuple[int, ...]`, `collections.abc.Callable`, `collections.abc.Iterator`.
- Environment: `uv` for virtual environments and dependency management (`uv sync` to update).
- Formatting: YAPF (configured in `pyproject.toml`, 120 char limit). Treat warnings as errors where possible.
- Imports: explicit only; no `__init__.py` wildcard re-exports.
- Code should be self-documenting with verbose variable names. Use docstrings only when necessary.
- Comments explain only the most complex code lines or blocks; no general narration in comments.
- No logger statements.
