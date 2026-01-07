# Usage Guide

This guide explains how to use the Helm Documentation MCP Server.

## Prerequisites

- Python 3.12 or later
- [uv](https://github.com/astral-sh/uv) package manager
- Git (for cloning helm-www repository during indexing)

## Setup

### 1. Initialise the Environment

```bash
make init
```

This installs all dependencies using uv.

### 2. Build the Documentation Index

```bash
make index
```

This clones the [helm-www](https://github.com/helm/helm-www) repository and indexes
all documentation pages into a local SQLite database.

### 3. Run the Server

```bash
make run
```

The server runs using STDIO transport and is ready to receive MCP requests.

## MCP Tools

### search_documentation

Search the Helm documentation using full-text search with stemming support.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search terms |
| `section` | string | No | None | Filter by section |
| `limit` | integer | No | 10 | Max results (1-50) |

**Available Sections:**

- `overview` - General Helm overview
- `intro` - Getting started guides
- `topics` - Core concepts (charts, plugins, architecture)
- `chart_template_guide` - Template authoring guide
- `chart_best_practices` - Best practices for charts
- `helm` - CLI command reference
- `howto` - How-to guides
- `sdk` - Go SDK documentation
- `plugins` - Plugin documentation
- `faq` - Frequently asked questions
- `glossary` - Terminology

**Example Response:**

```json
{
  "query": "install chart",
  "section_filter": null,
  "result_count": 5,
  "results": [
    {
      "title": "Helm Install",
      "url": "https://helm.sh/docs/helm/helm_install",
      "path": "helm/helm_install.md",
      "section": "helm",
      "snippet": "...command <mark>installs</mark> a <mark>chart</mark> archive...",
      "relevance_score": 12.5432
    }
  ]
}
```

### read_documentation

Retrieve the full content of a specific documentation page.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to document |

**Example Response:**

```json
{
  "path": "intro/quickstart.md",
  "title": "Quickstart Guide",
  "description": "How to install and get started with Helm",
  "section": "intro",
  "url": "https://helm.sh/docs/intro/quickstart",
  "content": "# Quickstart\n\nThis guide covers..."
}
```

## CLI Commands

### Index Documentation

```bash
# Index from main branch
make index

# Or use the CLI directly
uv run helm-docs-index index

# Index from a specific branch
uv run helm-docs-index index --branch release-3.x

# Rebuild index (clear existing data first)
uv run helm-docs-index index --rebuild
```

### Show Index Statistics

```bash
uv run helm-docs-index stats
```

## Configuration

### Database Location

By default, the SQLite database is stored at `data/helm_docs.db` relative to the
project directory. You can specify a custom location:

```bash
uv run helm-docs-index --database /path/to/custom.db index
```

## Integrating with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "helm-docs": {
      "command": "uv",
      "args": ["run", "mcp-helm-docs"],
      "cwd": "/path/to/mcp-helm-documentation"
    }
  }
}
```

### Other MCP Clients

The server uses STDIO transport, so it can be integrated with any MCP client that
supports STDIO-based servers.
