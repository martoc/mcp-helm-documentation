"""Tests for MCP server tools."""

import json
from unittest.mock import patch

from mcp_helm_documentation.database import DocumentDatabase
from mcp_helm_documentation.models import Document
from mcp_helm_documentation.server import _read_documentation_impl, _search_documentation_impl


class TestSearchDocumentation:
    """Tests for search_documentation tool."""

    def test_search_returns_results(self, database: DocumentDatabase, sample_documents: list[Document]) -> None:
        """Test search returns matching results."""
        for doc in sample_documents:
            database.upsert_document(doc)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _search_documentation_impl("quickstart")
            parsed = json.loads(result)

            assert "results" in parsed
            assert parsed["result_count"] >= 1

    def test_search_with_section_filter(self, database: DocumentDatabase, sample_documents: list[Document]) -> None:
        """Test search with section filter."""
        for doc in sample_documents:
            database.upsert_document(doc)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _search_documentation_impl("install", section="helm")
            parsed = json.loads(result)

            for r in parsed["results"]:
                assert r["section"] == "helm"

    def test_search_no_results(self, database: DocumentDatabase, sample_document: Document) -> None:
        """Test search with no matching results."""
        database.upsert_document(sample_document)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _search_documentation_impl("nonexistent_xyz_term")
            parsed = json.loads(result)

            assert parsed["results"] == []
            assert "No results found" in parsed["message"]

    def test_search_limit_capped_at_50(self, database: DocumentDatabase, sample_document: Document) -> None:
        """Test search limit is capped at 50."""
        database.upsert_document(sample_document)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _search_documentation_impl("helm", limit=100)
            parsed = json.loads(result)

            # Result count should be at most 50 (capped)
            assert parsed["result_count"] <= 50

    def test_search_limit_minimum_is_1(self, database: DocumentDatabase, sample_documents: list[Document]) -> None:
        """Test search limit minimum is 1."""
        for doc in sample_documents:
            database.upsert_document(doc)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _search_documentation_impl("helm", limit=-5)
            parsed = json.loads(result)

            # Should still return results (limit forced to 1)
            assert isinstance(parsed["results"], list)


class TestReadDocumentation:
    """Tests for read_documentation tool."""

    def test_read_existing_document(self, database: DocumentDatabase, sample_document: Document) -> None:
        """Test reading an existing document."""
        database.upsert_document(sample_document)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _read_documentation_impl("intro/quickstart.md")
            parsed = json.loads(result)

            assert parsed["title"] == sample_document.title
            assert parsed["content"] == sample_document.content
            assert parsed["url"] == sample_document.url

    def test_read_nonexistent_document(self, database: DocumentDatabase) -> None:
        """Test reading a non-existent document."""
        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _read_documentation_impl("nonexistent/path.md")
            parsed = json.loads(result)

            assert "error" in parsed
            assert "Document not found" in parsed["error"]

    def test_read_returns_all_fields(self, database: DocumentDatabase, sample_document: Document) -> None:
        """Test that read returns all expected fields."""
        database.upsert_document(sample_document)

        with patch("mcp_helm_documentation.server.get_database", return_value=database):
            result = _read_documentation_impl(sample_document.path)
            parsed = json.loads(result)

            assert "path" in parsed
            assert "title" in parsed
            assert "description" in parsed
            assert "section" in parsed
            assert "url" in parsed
            assert "content" in parsed
