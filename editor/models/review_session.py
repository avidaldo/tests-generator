"""Review-session models for the Stage 4 editor workflow."""

from dataclasses import dataclass, field

from models.question import Question


REVIEW_SESSION_ARTIFACT_TYPE = "review_session"
REVIEW_SESSION_VERSION = "1.0"


@dataclass(frozen=True)
class ImportedSource:
    """Represents one imported source tracked by a review session."""

    origin_kind: str
    origin_path: str = ""
    label: str = ""


@dataclass
class ReviewSession:
    """Represents one editor-owned review session."""

    questions: list[Question] = field(default_factory=list)
    imported_sources: list[ImportedSource] = field(default_factory=list)
    artifact_type: str = REVIEW_SESSION_ARTIFACT_TYPE
    version: str = REVIEW_SESSION_VERSION

    @classmethod
    def from_questions(cls, questions: list[Question]) -> "ReviewSession":
        imported_sources: list[ImportedSource] = []
        seen_sources: set[tuple[str, str, str]] = set()

        for question in questions:
            key = (
                question.origin_kind or "",
                question.origin_path or "",
                question.source_label or "",
            )
            if key == ("", "", "") or key in seen_sources:
                continue
            seen_sources.add(key)
            imported_sources.append(
                ImportedSource(
                    origin_kind=question.origin_kind,
                    origin_path=question.origin_path,
                    label=question.source_label,
                )
            )

        return cls(questions=list(questions), imported_sources=imported_sources)