"""Data models for Helm documentation."""

from dataclasses import dataclass


@dataclass
class DocumentMetadata:
    """Metadata extracted from markdown frontmatter."""

    title: str
    description: str | None = None
    sidebar_position: int | None = None
    sidebar_label: str | None = None


@dataclass
class Document:
    """Represents a documentation page."""

    path: str
    title: str
    description: str | None
    section: str
    content: str
    url: str
    sidebar_position: int | None = None


@dataclass
class SearchResult:
    """Represents a search result."""

    path: str
    title: str
    url: str
    snippet: str
    score: float
    section: str
