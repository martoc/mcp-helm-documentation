"""Parser for Helm documentation markdown files."""

import re
from pathlib import Path

import frontmatter

from mcp_helm_documentation.models import Document, DocumentMetadata


class DocumentParser:
    """Parses markdown files with YAML frontmatter."""

    HELM_DOCS_BASE_URL = "https://helm.sh/docs"

    def parse_file(self, file_path: Path, base_path: Path) -> Document | None:
        """Parse a markdown file and extract metadata and content.

        Args:
            file_path: Path to the markdown file.
            base_path: Base path of the documentation directory.

        Returns:
            Document instance or None if parsing fails.
        """
        try:
            post = frontmatter.load(file_path)
            metadata = self._extract_metadata(post.metadata)
            relative_path = file_path.relative_to(base_path)
            section = self._extract_section(relative_path)
            url = self._compute_url(relative_path)
            content = self._clean_content(post.content)

            return Document(
                path=str(relative_path),
                title=metadata.title,
                description=metadata.description,
                section=section,
                content=content,
                url=url,
                sidebar_position=metadata.sidebar_position,
            )
        except Exception:  # noqa: BLE001
            return None

    def _extract_metadata(self, metadata: dict[str, object]) -> DocumentMetadata:
        """Extract structured metadata from frontmatter.

        Args:
            metadata: Dictionary of frontmatter fields.

        Returns:
            DocumentMetadata instance.
        """
        title = metadata.get("title")
        if not isinstance(title, str):
            title = "Untitled"

        description = metadata.get("description")
        if not isinstance(description, str):
            description = None

        sidebar_position = metadata.get("sidebar_position")
        if not isinstance(sidebar_position, int):
            sidebar_position = None

        sidebar_label = metadata.get("sidebar_label")
        if not isinstance(sidebar_label, str):
            sidebar_label = None

        return DocumentMetadata(
            title=title,
            description=description,
            sidebar_position=sidebar_position,
            sidebar_label=sidebar_label,
        )

    def _extract_section(self, relative_path: Path) -> str:
        """Extract the top-level section from the path.

        Args:
            relative_path: Path relative to docs directory.

        Returns:
            Section name (first directory component or 'root').
        """
        parts = relative_path.parts
        return parts[0] if len(parts) > 1 else "root"

    def _compute_url(self, relative_path: Path) -> str:
        """Compute the helm.sh documentation URL.

        Args:
            relative_path: Path relative to docs directory.

        Returns:
            Full URL to the documentation page.
        """
        # Remove .md/.mdx extension and convert to URL path
        path_str = str(relative_path).replace(".mdx", "").replace(".md", "")
        return f"{self.HELM_DOCS_BASE_URL}/{path_str}"

    def _clean_content(self, content: str) -> str:
        """Clean markdown content for indexing.

        Removes MDX-specific syntax like imports and JSX components.

        Args:
            content: Raw markdown content.

        Returns:
            Cleaned content suitable for indexing.
        """
        # Remove import statements (MDX)
        content = re.sub(r"^import\s+.*$", "", content, flags=re.MULTILINE)
        # Remove JSX components (self-closing)
        content = re.sub(r"<[A-Z][a-zA-Z]*[^>]*/>", "", content)
        # Remove JSX components (with children)
        content = re.sub(r"<[A-Z][a-zA-Z]*[^>]*>.*?</[A-Z][a-zA-Z]*>", "", content, flags=re.DOTALL)
        return content.strip()
