[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io/)

# MCP Helm Documentation Server

An MCP (Model Context Protocol) server that provides search and retrieval tools for [Helm](https://helm.sh) documentation. This server enables AI assistants like Claude to search and read Helm documentation directly.

## Features

- **Full-text search** using SQLite FTS5 with BM25 ranking and Porter stemming
- **Section filtering** to narrow search results by documentation category
- **Pre-built index** containing ~130 documentation pages from the official helm-www repository
- **Docker support** for portable deployment across projects
- **STDIO transport** for seamless MCP client integration

## Quick Start

### Using Docker (Recommended)

```bash
# Build the Docker image (includes pre-indexed documentation)
make docker-build

# Test the server
make docker-run
```

### Using uv (Local Development)

```bash
# Initialise the environment
make init

# Build the documentation index
make index

# Run the server
make run
```

## Configuration

### Claude Code / Claude Desktop

Add to your `.mcp.json` or global settings:

```json
{
  "mcpServers": {
    "helm-docs": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "martoc/mcp-helm-documentation:latest"]
    }
  }
}
```

For a locally built Docker image:

```json
{
  "mcpServers": {
    "helm-docs": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-helm-documentation"]
    }
  }
}
```

For local development without Docker:

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

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_documentation` | Search Helm documentation by keyword query with optional section filtering |
| `read_documentation` | Retrieve the full content of a specific documentation page |

### search_documentation

Search Helm documentation using full-text search with stemming support.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search terms (supports stemming) |
| `section` | string | No | None | Filter by section (see below) |
| `limit` | integer | No | 10 | Maximum results (1-50) |

**Available Sections:** `overview`, `intro`, `topics`, `chart_template_guide`, `chart_best_practices`, `helm`, `howto`, `sdk`, `plugins`, `faq`, `glossary`

### read_documentation

Retrieve the full content of a documentation page.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to document (from search results) |

## CLI Commands

```bash
# Build/rebuild the documentation index
uv run helm-docs-index index
uv run helm-docs-index index --rebuild
uv run helm-docs-index index --branch release-3.x

# Show index statistics
uv run helm-docs-index stats
```

## Development

```bash
make init       # Initialise development environment
make build      # Run full build (lint, typecheck, test)
make test       # Run tests with coverage
make format     # Format code
make lint       # Run linter
make typecheck  # Run type checker
```

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage instructions
- [CODESTYLE.md](CODESTYLE.md) - Code style guidelines
- [CLAUDE.md](CLAUDE.md) - Claude Code instructions

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.
