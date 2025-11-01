"""
Defense 1: Embedded Security (Tool-Level Allowlist)
Security checks hardcoded directly in tool implementations.
"""

from .adk_agent_allowlist import root_agent, create_agent_with_embedded_security

__all__ = ['root_agent', 'create_agent_with_embedded_security']
