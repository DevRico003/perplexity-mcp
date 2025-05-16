# Perplexity MCP

MCP server for Perplexity AI web search integration. This MCP allows you to search the web using Perplexity AI's API with options for filtering results by recency.

## Features

- Fast web search using Perplexity AI
- Recency filtering (day, week, month, year)
- Support for various Perplexity AI models
- Results include citations to sources

## Installation

```bash
pip install perplexity-mcp
```

## Configuration

Set the following environment variables:

- `PERPLEXITY_API_KEY` (required): Your Perplexity API key
- `PERPLEXITY_MODEL` (optional): The model to use (defaults to "sonar")
- `PORT` (optional): The port to run the server on (defaults to 8055)
- `HOST` (optional): The host to run the server on (defaults to "0.0.0.0")
- `TRANSPORT` (optional): The transport method to use ("sse" or "stdio", defaults to "sse")

## Available Models

- `sonar-deep-research`: 128k context - Enhanced research capabilities
- `sonar-reasoning-pro`: 128k context - Advanced reasoning with professional focus
- `sonar-reasoning`: 128k context - Enhanced reasoning capabilities
- `sonar-pro`: 200k context - Professional grade model
- `sonar`: 128k context - Default model
- `r1-1776`: 128k context - Alternative architecture

## Usage

Start the server:

```bash
perplexity-mcp
```

Or with Docker:

```bash
docker run -e PERPLEXITY_API_KEY=your-api-key perplexity-mcp
```