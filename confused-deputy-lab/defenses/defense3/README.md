# Defense 3: Security Dashboard & Benchmarking

## Concept

This defense adds **production-ready monitoring** to agent security. It includes:

1. **Real-time security dashboard** (Streamlit)
2. **Event logging and analysis**
3. **Automated security testing** integration points

The principle: **"You can't stop what you can't see"**

## Features

### 1. Real-time Dashboard

A Streamlit web interface showing:
- Total events, violations, and alerts
- Timeline of security events
- Tool usage breakdown
- Top violation reasons
- Recent events table with filtering
- Export capabilities (CSV, JSON)

### 2. Event Logging

All security events are logged in JSON Lines format:

```json
{
  "timestamp": "2024-10-31T10:15:30.123",
  "type": "violation",
  "tool": "fetch_web_data",
  "details": {
    "url": "http://webhook.site/exfil",
    "reason": "Domain not in allowlist"
  }
}
```

### 3. Metrics & Analytics

- Event counts and trends
- Violation patterns
- Tool usage statistics
- Attack attempt detection

## Running the Dashboard

### Step 1: Generate Demo Events

```bash
cd defenses/defense3
python security_dashboard.py demo
```

### Step 2: Launch Dashboard

```bash
streamlit run security_dashboard.py
```

Then open your browser to `http://localhost:8501`

### Step 3: Clear Events (Optional)

```bash
python security_dashboard.py clear
```

## Dashboard Screenshots

The dashboard shows:

📊 **Metrics Row**
- Total Events
- Violations (red)
- Approved Calls (green)
- Alerts (orange)

📈 **Timeline Chart**
- Real-time event stream
- Color-coded by type
- Time-series analysis

🔧 **Tool Usage**
- Pie chart of tool distribution
- Identify most-used tools

⚠️ **Violation Analysis**
- Bar chart of violation reasons
- Pattern identification

## Integration with Automated Testing

### Agent Security Bench (ASB)

The dashboard can be integrated with security testing frameworks:

```python
# Example: Automated security test
def test_exfiltration_blocked():
    inspector = MCPToolInspector()
    dashboard = SecurityDashboard()

    # Attempt attack
    allowed, reason = inspector.inspect_tool_call(
        "fetch_web_data",
        {"url": "http://attacker.webhook.site/exfil"}
    )

    # Log result
    dashboard.log_event(
        'violation' if not allowed else 'approved',
        'fetch_web_data',
        {'url': url, 'reason': reason}
    )

    # Assert blocked
    assert not allowed, "Exfiltration should be blocked"
```

### Promptfoo Integration

Convert manual CTF attacks into automated tests:

```yaml
# promptfoo-tests.yaml
tests:
  - description: "Test: Exfiltration blocked"
    vars:
      attack_url: "http://webhook.site/exfil?data=secret"
    assert:
      - type: python
        value: |
          allowed, _ = inspector.inspect_tool_call(
            "fetch_web_data",
            {"url": attack_url}
          )
          return not allowed
```

## Production Deployment

### 1. Continuous Monitoring

Run the dashboard as a service:

```bash
# Using systemd or docker
docker run -d -p 8501:8501 agent-security-dashboard
```

### 2. Alerting

Integrate with existing monitoring:

```python
# Send alerts to Slack, PagerDuty, etc.
if event['type'] == 'violation':
    send_alert(event)
```

### 3. Log Aggregation

Ship logs to your SIEM:

```bash
# Forward to ELK, Splunk, etc.
tail -f security_events.jsonl | logstash ...
```

## Advantages

✅ **Visibility**: See all security events in real-time
✅ **Analysis**: Identify attack patterns and trends
✅ **Compliance**: Audit trail for security reviews
✅ **Testing**: Integrate with automated security tests
✅ **Production-Ready**: Can be deployed in real environments

## Using for the CTF

### For Students

1. Run the vulnerable agent
2. Launch the dashboard
3. Attempt the attack
4. Watch violations appear in real-time!

### For Instructors

1. Show the dashboard before the attack
2. Let students attempt exploitation
3. Live-demo the violations appearing
4. Explain how to prevent with MCP policies

This makes the abstract concept of "security monitoring" concrete and visible.

## Next Steps

- Add webhooks for real-time alerts
- Integrate with CI/CD pipelines
- Add automated remediation
- Create custom security rules
