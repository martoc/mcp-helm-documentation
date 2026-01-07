"""Tests for models module."""

from mcp_helm_documentation.models import Document, DocumentMetadata, SearchResult


class TestDocumentMetadata:
    """Tests for DocumentMetadata dataclass."""

    def test_create_with_all_fields(self) -> None:
        """Test creating metadata with all fields."""
        metadata = DocumentMetadata(
            title="Test Title",
            description="Test description",
            sidebar_position=1,
            sidebar_label="Test Label",
        )
        assert metadata.title == "Test Title"
        assert metadata.description == "Test description"
        assert metadata.sidebar_position == 1
        assert metadata.sidebar_label == "Test Label"

    def test_create_with_defaults(self) -> None:
        """Test creating metadata with default values."""
        metadata = DocumentMetadata(title="Test Title")
        assert metadata.title == "Test Title"
        assert metadata.description is None
        assert metadata.sidebar_position is None
        assert metadata.sidebar_label is None


class TestDocument:
    """Tests for Document dataclass."""

    def test_create_document(self) -> None:
        """Test creating a document."""
        doc = Document(
            path="intro/quickstart.md",
            title="Quickstart",
            description="Getting started guide",
            section="intro",
            content="# Quickstart\n\nContent here.",
            url="https://helm.sh/docs/intro/quickstart",
            sidebar_position=1,
        )
        assert doc.path == "intro/quickstart.md"
        assert doc.title == "Quickstart"
        assert doc.section == "intro"


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_create_search_result(self) -> None:
        """Test creating a search result."""
        result = SearchResult(
            path="intro/quickstart.md",
            title="Quickstart",
            url="https://helm.sh/docs/intro/quickstart",
            snippet="...getting started with <mark>Helm</mark>...",
            score=15.5,
            section="intro",
        )
        assert result.path == "intro/quickstart.md"
        assert result.score == 15.5
        assert "<mark>" in result.snippet
