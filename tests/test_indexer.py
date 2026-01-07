"""Tests for indexer module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_helm_documentation.database import DocumentDatabase
from mcp_helm_documentation.indexer import HelmDocsIndexer


class TestHelmDocsIndexer:
    """Tests for HelmDocsIndexer class."""

    def test_index_from_path_indexes_markdown_files(self, database: DocumentDatabase) -> None:
        """Test indexing markdown files from a local path."""
        indexer = HelmDocsIndexer(database)

        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)

            # Create sample markdown files
            intro_dir = docs_path / "intro"
            intro_dir.mkdir()

            quickstart = intro_dir / "quickstart.md"
            quickstart.write_text("""---
title: Quickstart Guide
description: Getting started with Helm
sidebar_position: 1
---

# Quickstart

Content here.
""")

            install = intro_dir / "install.md"
            install.write_text("""---
title: Installing Helm
description: How to install Helm
sidebar_position: 2
---

# Installing Helm

Installation instructions.
""")

            count = indexer.index_from_path(docs_path)

            assert count == 2
            assert database.get_document_count() == 2

    def test_index_from_path_handles_mdx_files(self, database: DocumentDatabase) -> None:
        """Test that .mdx files are also indexed."""
        indexer = HelmDocsIndexer(database)

        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)

            mdx_file = docs_path / "index.mdx"
            mdx_file.write_text("""---
title: Overview
description: Helm overview
---

import DocCardList from '@theme/DocCardList';

# Overview

<DocCardList />
""")

            count = indexer.index_from_path(docs_path)

            assert count == 1
            doc = database.get_document("index.mdx")
            assert doc is not None
            assert doc.title == "Overview"

    def test_index_from_path_raises_on_missing_path(self, database: DocumentDatabase) -> None:
        """Test that indexing raises error for missing path."""
        indexer = HelmDocsIndexer(database)

        with pytest.raises(ValueError, match="does not exist"):
            indexer.index_from_path(Path("/nonexistent/path"))

    def test_rebuild_index_clears_existing_data(self, database: DocumentDatabase) -> None:
        """Test that rebuild clears existing data before indexing."""
        indexer = HelmDocsIndexer(database)

        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)

            # Create initial file
            file1 = docs_path / "file1.md"
            file1.write_text("---\ntitle: File 1\n---\nContent 1")

            indexer.index_from_path(docs_path)
            assert database.get_document_count() == 1

            # Mock git clone to avoid actual network call
            with patch.object(indexer, "_clone_repository"):
                with patch.object(indexer, "_index_directory", return_value=5) as mock_index:
                    # Create a mock temp directory with docs
                    mock_index.return_value = 5
                    database.clear()  # Simulate rebuild clearing
                    mock_index(docs_path)

                    assert database.get_document_count() == 0  # Cleared by rebuild

    def test_index_from_path_handles_files_without_frontmatter(self, database: DocumentDatabase) -> None:
        """Test that files without frontmatter are indexed with default title."""
        indexer = HelmDocsIndexer(database)

        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)

            # Create a file without frontmatter
            no_frontmatter = docs_path / "no_frontmatter.md"
            no_frontmatter.write_text("# Just content\n\nNo YAML frontmatter here.")

            count = indexer.index_from_path(docs_path)

            assert count == 1
            doc = database.get_document("no_frontmatter.md")
            assert doc is not None
            assert doc.title == "Untitled"  # Default title when frontmatter missing
