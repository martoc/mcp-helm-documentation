"""Pytest fixtures for Helm documentation MCP server tests."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from mcp_helm_documentation.database import DocumentDatabase
from mcp_helm_documentation.models import Document


@pytest.fixture
def temp_db_path() -> Generator[Path, None, None]:
    """Provide a temporary database path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir) / "test_helm_docs.db"


@pytest.fixture
def database(temp_db_path: Path) -> DocumentDatabase:
    """Provide a fresh database instance."""
    return DocumentDatabase(temp_db_path)


@pytest.fixture
def sample_document() -> Document:
    """Provide a sample document for testing."""
    return Document(
        path="intro/quickstart.md",
        title="Quickstart Guide",
        description="How to install and get started with Helm",
        section="intro",
        content="# Quickstart\n\nThis guide covers how you can quickly get started using Helm.",
        url="https://helm.sh/docs/intro/quickstart",
        sidebar_position=1,
    )


@pytest.fixture
def sample_documents() -> list[Document]:
    """Provide multiple sample documents for testing."""
    return [
        Document(
            path="intro/quickstart.md",
            title="Quickstart Guide",
            description="How to install and get started with Helm",
            section="intro",
            content="# Quickstart\n\nThis guide covers how you can quickly get started using Helm.",
            url="https://helm.sh/docs/intro/quickstart",
            sidebar_position=1,
        ),
        Document(
            path="topics/charts.md",
            title="Charts",
            description="Learn about Helm charts",
            section="topics",
            content="# Charts\n\nHelm uses a packaging format called charts.",
            url="https://helm.sh/docs/topics/charts",
            sidebar_position=1,
        ),
        Document(
            path="helm/helm_install.md",
            title="Helm Install",
            description="Install a chart",
            section="helm",
            content="# helm install\n\nThis command installs a chart archive.",
            url="https://helm.sh/docs/helm/helm_install",
            sidebar_position=None,
        ),
    ]


@pytest.fixture
def sample_markdown_content() -> str:
    """Provide sample markdown with frontmatter."""
    return """---
title: "Quickstart Guide"
description: "How to install and get started with Helm"
sidebar_position: 1
---

# Quickstart

This guide covers how you can quickly get started using Helm.

## Prerequisites

- A Kubernetes cluster
- kubectl configured
"""
