"""
Defense 2: MCP Security Server
Security policies enforced via Model Context Protocol with process isolation.
"""

from .adk_agent_with_mcp import root_agent, create_secure_agent

__all__ = ['root_agent', 'create_secure_agent']
