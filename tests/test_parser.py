"""Tests for parser module."""

import tempfile
from pathlib import Path

from mcp_helm_documentation.parser import DocumentParser


class TestDocumentParser:
    """Tests for DocumentParser class."""

    def test_parse_file_with_frontmatter(self, sample_markdown_content: str) -> None:
        """Test parsing a file with valid frontmatter."""
        parser = DocumentParser()
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)
            file_path = docs_path / "intro" / "quickstart.md"
            file_path.parent.mkdir(parents=True)
            file_path.write_text(sample_markdown_content)

            document = parser.parse_file(file_path, docs_path)

            assert document is not None
            assert document.title == "Quickstart Guide"
            assert document.description == "How to install and get started with Helm"
            assert document.section == "intro"
            assert document.sidebar_position == 1
            assert document.url == "https://helm.sh/docs/intro/quickstart"

    def test_parse_file_extracts_section(self) -> None:
        """Test that section is correctly extracted from path."""
        parser = DocumentParser()
        content = "---\ntitle: Test\n---\nContent"
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)

            # Test nested path
            nested_path = docs_path / "topics" / "charts" / "index.md"
            nested_path.parent.mkdir(parents=True)
            nested_path.write_text(content)

            document = parser.parse_file(nested_path, docs_path)
            assert document is not None
            assert document.section == "topics"

    def test_parse_file_handles_missing_frontmatter(self) -> None:
        """Test parsing a file without frontmatter."""
        parser = DocumentParser()
        content = "# No Frontmatter\n\nJust content."
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_path = Path(temp_dir)
            file_path = docs_path / "test.md"
            file_path.write_text(content)

            document = parser.parse_file(file_path, docs_path)
            # Should still parse but with default title
            assert document is not None
            assert document.title == "Untitled"

    def test_compute_url_removes_md_extension(self) -> None:
        """Test URL computation removes .md extension."""
        parser = DocumentParser()
        md_path = Path("intro/install.md")
        url = parser._compute_url(md_path)
        assert url == "https://helm.sh/docs/intro/install"

    def test_compute_url_removes_mdx_extension(self) -> None:
        """Test URL computation removes .mdx extension."""
        parser = DocumentParser()
        mdx_path = Path("intro/using_helm.mdx")
        url = parser._compute_url(mdx_path)
        assert url == "https://helm.sh/docs/intro/using_helm"

    def test_clean_content_removes_mdx_imports(self) -> None:
        """Test that MDX import statements are removed."""
        parser = DocumentParser()
        content = """import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Real Content

Some text here."""

        cleaned = parser._clean_content(content)
        assert "import" not in cleaned
        assert "Real Content" in cleaned

    def test_clean_content_removes_jsx_components(self) -> None:
        """Test that JSX components are removed."""
        parser = DocumentParser()
        content = """# Title

<DocCardList />

Some content here.

<CustomComponent>Inner content</CustomComponent>

More text."""

        cleaned = parser._clean_content(content)
        assert "<DocCardList" not in cleaned
        assert "<CustomComponent" not in cleaned
        assert "Title" in cleaned
        assert "Some content here" in cleaned

    def test_extract_section_for_root_file(self) -> None:
        """Test section extraction for root-level files."""
        parser = DocumentParser()
        root_path = Path("overview.md")
        section = parser._extract_section(root_path)
        assert section == "root"

    def test_extract_section_for_nested_file(self) -> None:
        """Test section extraction for nested files."""
        parser = DocumentParser()
        nested_path = Path("chart_template_guide/getting_started.md")
        section = parser._extract_section(nested_path)
        assert section == "chart_template_guide"
