"""MCP server for Perplexity AI web search integration."""

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import aiohttp
import sys
import logging
import json
import os

from .utils import (
    validate_perplexity_key,
    log_model_info,
    format_response_with_citations,
    get_perplexity_payload
)

load_dotenv()

# Create a dataclass for our application context
@dataclass
class PerplexityContext:
    """Context for the Perplexity MCP server."""
    api_key: str

@asynccontextmanager
async def perplexity_lifespan(server: FastMCP) -> AsyncIterator[PerplexityContext]:
    """
    Manages the Perplexity client lifecycle.
    
    Args:
        server: The FastMCP server instance
        
    Yields:
        PerplexityContext: The context containing the Perplexity API key
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable is required")
    
    log_model_info()
    
    try:
        yield PerplexityContext(api_key=api_key)
    finally:
        # No explicit cleanup needed for the Perplexity API
        pass

# Initialize FastMCP server with the Perplexity context
mcp = FastMCP(
    "perplexity-mcp",
    description="MCP server for Perplexity AI web search integration",
    lifespan=perplexity_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8055")
)        

@mcp.tool()
async def search_web(
    ctx: Context, 
    query: str, 
    recency: str = "month"
) -> str:
    """Search the web using Perplexity AI with recency filtering.
    
    This tool uses Perplexity AI to search the web and provide up-to-date information
    with citations to sources. Results can be filtered by recency.
    
    Args:
        ctx: The MCP server provided context
        query: The search query to find information about
        recency: Filter results by how recent they are. Options: 'day' (last 24h), 
                'week' (last 7 days), 'month' (last 30 days), 'year' (last 365 days). 
                Defaults to 'month'.
    """
    try:
        api_key = ctx.request_context.lifespan_context.api_key
        url = "https://api.perplexity.ai/chat/completions"
        
        payload = get_perplexity_payload(query, recency)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Format response with citations if available
                if "citations" in data:
                    return format_response_with_citations(content, data["citations"])
                
                return content
    except Exception as e:
        return f"Error searching with Perplexity: {str(e)}"

async def main():
    """Main entry point for the MCP server."""
    if not validate_perplexity_key():
        logging.error("PERPLEXITY_API_KEY environment variable is required")
        sys.exit(1)
    
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())