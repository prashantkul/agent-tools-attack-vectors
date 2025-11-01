#!/usr/bin/env python3
"""
ADK Web Server for Financial Analyst Agent
Serves the agent via ADK's web interface.
"""

import os
from adk_agent import create_financial_analyst_agent

# Ensure API key is set
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_GENAI_API_KEY"] = api_key

# Create the root agent
root_agent = create_financial_analyst_agent()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌐 Financial Analyst Agent Server")
    print("="*70)
    print("\nAgent is ready to serve!")
    print("\nTo access the web UI, the ADK framework will handle routing.")
    print("\nRun with: adk web --agent server:root_agent")
    print("="*70 + "\n")
