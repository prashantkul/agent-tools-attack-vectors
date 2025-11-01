#!/usr/bin/env python3
"""
Real MCP Security Server
A Model Context Protocol server that enforces security policies on agent tools.

This is a TRUE MCP server implementation (unlike the original "MCP-inspired" inspector).
It runs as a separate process and communicates via stdio using the MCP protocol.
"""

import os
import sys
import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Sequence
from datetime import datetime
import requests

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Import our existing security inspector
from mcp_tool_inspector import MCPToolInspector

# Configuration
DOCS_DIR = Path(__file__).parent.parent.parent / "documents"
POLICY_PATH = Path(__file__).parent / "mcp_security_policy.yaml"
LOG_FILE = Path(__file__).parent / "mcp_server.log"

# Set up file logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [MCP-SERVER] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stderr)
    ]
)


class SecurityMCPServer:
    """
    MCP Server with integrated security policy enforcement.

    This server exposes agent tools through the MCP protocol while enforcing
    security policies defined in the YAML configuration file.
    """

    def __init__(self):
        """Initialize the MCP server with security policies."""
        self.server = Server("financial-analyst-security")
        self.inspector = MCPToolInspector(POLICY_PATH)

        # Log server startup
        logging.info("🔒 Security MCP Server initializing...")
        logging.info(f"📋 Policy: {self.inspector.policy['policy_name']}")
        logging.info(f"📂 Documents directory: {DOCS_DIR}")
        logging.info(f"📝 Logging to: {LOG_FILE}")

        # Register request handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP protocol handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools with their schemas."""
            logging.info("📋 Client requested tool list")

            return [
                Tool(
                    name="read_document",
                    description=(
                        "Read a document from the internal file system. "
                        "Use this to access financial reports, market data, and internal documents. "
                        "Security: Subject to policy validation and rate limiting."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "The name of the file to read (e.g., 'market_summary.pdf')",
                            }
                        },
                        "required": ["filename"],
                    },
                ),
                Tool(
                    name="fetch_web_data",
                    description=(
                        "Perform an HTTP GET request to retrieve data from a URL. "
                        "Use this to fetch external data or perform web searches. "
                        "Security: Only allowed domains can be accessed. Blocked domains will be rejected."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The full URL to fetch data from",
                            }
                        },
                        "required": ["url"],
                    },
                ),
                Tool(
                    name="list_documents",
                    description=(
                        "List all available documents in the internal system. "
                        "Use this to discover what files are available."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """
            Execute a tool with security validation.

            This is the critical security boundary - ALL tool calls go through
            the security inspector before execution.
            """
            logging.info(f"🔧 Tool call request: {name}({arguments})")

            # SECURITY CHECK: Validate with policy inspector
            allowed, reason = self.inspector.inspect_tool_call(name, arguments)

            if not allowed:
                logging.warning(f"⛔ BLOCKED: {reason}")
                return [
                    TextContent(
                        type="text",
                        text=f"⛔ Security Policy Violation: {reason}"
                    )
                ]

            # Execute the approved tool
            try:
                result = await self._execute_tool(name, arguments)
                logging.info(f"✅ Tool executed successfully: {name}")
                return [TextContent(type="text", text=result)]

            except Exception as e:
                error_msg = f"Error executing tool: {str(e)}"
                logging.error(f"❌ {error_msg}")
                return [TextContent(type="text", text=error_msg)]

    async def _execute_tool(self, name: str, arguments: dict) -> str:
        """Execute the actual tool logic."""

        if name == "read_document":
            return self._read_document(arguments.get("filename", ""))

        elif name == "fetch_web_data":
            return self._fetch_web_data(arguments.get("url", ""))

        elif name == "list_documents":
            return self._list_documents()

        else:
            raise ValueError(f"Unknown tool: {name}")

    def _read_document(self, filename: str) -> str:
        """
        Read a document from the internal file system.
        Note: This is called AFTER security validation.
        """
        try:
            file_path = DOCS_DIR / filename

            if not file_path.exists():
                available_files = [f.name for f in DOCS_DIR.glob("*") if f.is_file()]
                return f"Error: File '{filename}' not found. Available files: {', '.join(available_files)}"

            with open(file_path, 'r') as f:
                content = f.read()

            logging.info(f"📄 Read {len(content)} bytes from {filename}")
            return content

        except Exception as e:
            return f"Error reading file: {str(e)}"

    def _fetch_web_data(self, url: str) -> str:
        """
        Fetch data from a URL.
        Note: This is called AFTER security validation (domain checks, etc.)
        """
        try:
            logging.info(f"🌐 Fetching: {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            result = response.text[:500]  # Limit response size
            logging.info(f"📥 Received {len(response.text)} bytes")

            return result

        except Exception as e:
            return f"Error fetching URL: {str(e)}"

    def _list_documents(self) -> str:
        """List all available documents."""
        try:
            files = [f.name for f in DOCS_DIR.glob("*") if f.is_file()]
            logging.info(f"📑 Listed {len(files)} documents")
            return f"Available documents: {', '.join(files)}"

        except Exception as e:
            return f"Error listing documents: {str(e)}"

    async def run(self):
        """Run the MCP server with stdio transport."""
        logging.info("🚀 Starting MCP server on stdio...")
        logging.info("📡 Waiting for client connection...")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the MCP server."""
    server = SecurityMCPServer()
    await server.run()


if __name__ == "__main__":
    # Run the async server
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[MCP-SERVER] 👋 Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"\n[MCP-SERVER] ❌ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
