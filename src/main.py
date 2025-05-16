"""
Standalone entry point for running the Perplexity MCP server.
This file provides a convenient way to run the server directly.
"""

import asyncio
import logging
from perplexity_mcp.server import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())