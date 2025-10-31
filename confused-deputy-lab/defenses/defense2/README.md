# Defense 2: MCP-Based Tool Inspector

## Concept

This defense uses the **Model Context Protocol (MCP)** to externalize security policies. Instead of embedding security logic in each tool, a security proxy (the Tool Inspector) sits between the agent and its tools, enforcing policies defined in a YAML configuration file.

## Architecture

```
┌─────────┐          ┌──────────────────┐          ┌───────┐
│  Agent  │ ────────>│  MCP Inspector   │────────> │ Tools │
└─────────┘          │  (Security Proxy)│          └───────┘
                     └──────────────────┘
                              │
                              ↓
                     ┌──────────────────┐
                     │  Security Policy │
                     │  (YAML Config)   │
                     └──────────────────┘
```

## Key Features

### 1. Externalized Security Policy

Security rules are defined in `mcp_security_policy.yaml`, not in code:

```yaml
tools:
  fetch_web_data:
    parameter_validation:
      url:
        allowed_domains:
          - "internal-wiki.company.com"
          - "*.company.com"
        blocked_domains:
          - "webhook.site"
          - "requestbin.com"
```

### 2. Cross-Tool Security Rules

Detect attack patterns across multiple tool calls:

```yaml
security_rules:
  - name: "exfiltration_detection"
    trigger:
      - tool: "fetch_web_data"
        after_tool: "read_document"
        within_seconds: 5
    action: "block"
```

### 3. Rate Limiting

Prevent abuse through automated attacks:

```yaml
rate_limit:
  max_calls_per_minute: 5
```

### 4. Pattern Detection

Block suspicious URL patterns:

```yaml
forbidden_patterns:
  - "query=.*CONFIDENTIAL"
  - "data=.*"
```

## Running the Demo

```bash
cd defenses/defense2
python mcp_tool_inspector.py demo
```

This demonstrates:
1. Legitimate calls being approved
2. Malicious URLs being blocked
3. Exfiltration attempts being detected
4. Security statistics and logging

## How It Blocks the Attack

1. **Domain Allowlist**: The attacker's `webhook.site` URL is blocked
2. **Exfiltration Detection**: `fetch_web_data` called shortly after `read_document` triggers an alert
3. **Pattern Matching**: Long URLs with suspicious patterns are blocked
4. **Rate Limiting**: Rapid automated attacks are throttled

## Advantages Over Defense 1

✅ **Separation of Concerns**: Security policy is separate from tool code
✅ **Easy Updates**: Change policy without touching code
✅ **Centralized Governance**: One policy file for all tools
✅ **Cross-Tool Rules**: Detect multi-step attacks
✅ **Auditable**: Clear YAML configuration that can be reviewed
✅ **Scalable**: Add new tools without duplicating security logic

## Integration with Real Agents

To integrate this with a real agent:

```python
from mcp_tool_inspector import MCPToolInspector

inspector = MCPToolInspector()

# Before executing any tool call:
allowed, reason = inspector.inspect_tool_call(tool_name, parameters)

if allowed:
    result = execute_tool(tool_name, parameters)
else:
    return f"Security policy violation: {reason}"
```

## Next Step

See **Defense 3** for production-ready security with dashboards and monitoring.
