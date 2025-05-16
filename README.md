# Perplexity MCP

MCP server for Perplexity AI web search integration. This MCP allows you to search the web using Perplexity AI's API with options for filtering results by recency.

## Features

- Fast web search using Perplexity AI
- Recency filtering (day, week, month, year)
- Support for various Perplexity AI models
- Results include citations to sources

## Prerequisites

- Python 3.12+
- Perplexity API key

## Installation

### Using pip

```bash
pip install perplexity-mcp
```

### From Source

Clone this repository:

```bash
git clone https://github.com/yourusername/perplexity-mcp.git
cd perplexity-mcp
```

Install dependencies:

```bash
pip install -e .
```

### Using Docker (Recommended)

Build the Docker image:

```bash
docker build -t perplexity-mcp --build-arg PORT=8055 .
```

## Configuration

The following environment variables can be configured:

| Variable | Description | Default |
| --- | --- | --- |
| PERPLEXITY_API_KEY | Your Perplexity API key (required) | - |
| PERPLEXITY_MODEL | Model to use for queries | sonar |
| TRANSPORT | Transport protocol (sse or stdio) | sse |
| HOST | Host to bind to when using SSE transport | 0.0.0.0 |
| PORT | Port to listen on when using SSE transport | 8055 |

## Available Models

- `sonar-deep-research`: 128k context - Enhanced research capabilities
- `sonar-reasoning-pro`: 128k context - Advanced reasoning with professional focus
- `sonar-reasoning`: 128k context - Enhanced reasoning capabilities
- `sonar-pro`: 200k context - Professional grade model
- `sonar`: 128k context - Default model
- `r1-1776`: 128k context - Alternative architecture

## Running the Server

### Using pip

SSE Transport:
```bash
# Set TRANSPORT=sse in your environment
perplexity-mcp
```

Stdio Transport:
With stdio, the MCP client itself can spin up the MCP server.

### Using Docker

SSE Transport:
```bash
docker run -e PERPLEXITY_API_KEY=your-api-key -p 8055:8055 perplexity-mcp
```

Stdio Transport:
With stdio, the MCP client itself can spin up the MCP server container.

## Integration with MCP Clients

### SSE Configuration

Once you have the server running with SSE transport, you can connect to it using this configuration:

```json
{
  "mcpServers": {
    "perplexity": {
      "transport": "sse",
      "url": "http://localhost:8055/sse"
    }
  }
}
```

Note for Windsurf users: Use serverUrl instead of url in your configuration:

```json
{
  "mcpServers": {
    "perplexity": {
      "transport": "sse",
      "serverUrl": "http://localhost:8055/sse"
    }
  }
}
```

Note for n8n users: Use host.docker.internal instead of localhost:

```
http://host.docker.internal:8055/sse
```

### Python with Stdio Configuration

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["-m", "perplexity_mcp"],
      "env": {
        "TRANSPORT": "stdio",
        "PERPLEXITY_API_KEY": "YOUR-API-KEY",
        "PERPLEXITY_MODEL": "sonar"
      }
    }
  }
}
```

### Docker with Stdio Configuration

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "docker",
      "args": ["run", "--rm", "-i", 
               "-e", "TRANSPORT", 
               "-e", "PERPLEXITY_API_KEY", 
               "-e", "PERPLEXITY_MODEL", 
               "perplexity-mcp"],
      "env": {
        "TRANSPORT": "stdio",
        "PERPLEXITY_API_KEY": "YOUR-API-KEY",
        "PERPLEXITY_MODEL": "sonar"
      }
    }
  }
}
```