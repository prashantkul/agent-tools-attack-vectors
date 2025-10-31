#!/usr/bin/env python3
"""
Defense 3: Security Dashboard with Real-time Monitoring
A Streamlit-based dashboard for visualizing agent security events.
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "defense2"))
from mcp_tool_inspector import MCPToolInspector


class SecurityDashboard:
    """Security monitoring dashboard for agent tool calls."""

    def __init__(self):
        self.log_file = Path(__file__).parent / "security_events.jsonl"
        self.inspector = None

    def load_events(self):
        """Load security events from log file."""
        events = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        return events

    def log_event(self, event_type: str, tool: str, details: dict):
        """Log a security event."""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'tool': tool,
            'details': details
        }

        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def render_dashboard(self):
        """Render the Streamlit dashboard."""
        st.set_page_config(
            page_title="Agent Security Dashboard",
            page_icon="🛡️",
            layout="wide"
        )

        st.title("🛡️ Agent Security Dashboard")
        st.markdown("**Real-time monitoring of agent tool calls and security violations**")

        # Load events
        events = self.load_events()

        if not events:
            st.info("No security events logged yet. Run the demo to generate events.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(events)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Events", len(df))

        with col2:
            violations = df[df['type'] == 'violation']
            st.metric("Violations", len(violations), delta=f"-{len(violations)}", delta_color="inverse")

        with col3:
            approvals = df[df['type'] == 'approved']
            st.metric("Approved Calls", len(approvals))

        with col4:
            alerts = df[df['type'] == 'alert']
            st.metric("Alerts", len(alerts), delta=f"-{len(alerts)}", delta_color="inverse")

        # Timeline
        st.subheader("📊 Event Timeline")

        # Create timeline chart
        timeline_data = df.groupby([df['timestamp'].dt.floor('1min'), 'type']).size().reset_index(name='count')
        fig = px.line(
            timeline_data,
            x='timestamp',
            y='count',
            color='type',
            title='Security Events Over Time',
            color_discrete_map={
                'violation': 'red',
                'approved': 'green',
                'alert': 'orange'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tool usage breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔧 Tool Usage")
            tool_counts = df['tool'].value_counts()
            fig_tools = px.pie(
                values=tool_counts.values,
                names=tool_counts.index,
                title='Tool Call Distribution'
            )
            st.plotly_chart(fig_tools, use_container_width=True)

        with col2:
            st.subheader("⚠️ Violation Types")
            violations_df = df[df['type'] == 'violation']
            if len(violations_df) > 0:
                violation_reasons = violations_df['details'].apply(
                    lambda x: x.get('reason', 'Unknown')[:50]
                ).value_counts()
                fig_violations = px.bar(
                    x=violation_reasons.values,
                    y=violation_reasons.index,
                    orientation='h',
                    title='Top Violation Reasons'
                )
                st.plotly_chart(fig_violations, use_container_width=True)
            else:
                st.success("No violations detected!")

        # Recent events table
        st.subheader("📋 Recent Events")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            event_type_filter = st.multiselect(
                "Filter by type",
                options=['all'] + list(df['type'].unique()),
                default=['all']
            )
        with col2:
            tool_filter = st.multiselect(
                "Filter by tool",
                options=['all'] + list(df['tool'].unique()),
                default=['all']
            )

        # Apply filters
        filtered_df = df
        if 'all' not in event_type_filter and event_type_filter:
            filtered_df = filtered_df[filtered_df['type'].isin(event_type_filter)]
        if 'all' not in tool_filter and tool_filter:
            filtered_df = filtered_df[filtered_df['tool'].isin(tool_filter)]

        # Display table
        st.dataframe(
            filtered_df.sort_values('timestamp', ascending=False).head(50),
            use_container_width=True
        )

        # Export options
        st.subheader("💾 Export")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export as CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "security_events.csv",
                    "text/csv"
                )
        with col2:
            if st.button("Export as JSON"):
                json_str = df.to_json(orient='records', indent=2)
                st.download_button(
                    "Download JSON",
                    json_str,
                    "security_events.json",
                    "application/json"
                )


def generate_demo_events():
    """Generate demo security events for testing."""
    dashboard = SecurityDashboard()

    print("Generating demo security events...")

    # Simulate various events
    events = [
        ('approved', 'read_document', {'filename': 'public_report.txt'}),
        ('approved', 'read_document', {'filename': 'market_summary.pdf'}),
        ('violation', 'read_document', {'filename': '../etc/passwd', 'reason': 'Path traversal detected'}),
        ('approved', 'list_documents', {}),
        ('violation', 'fetch_web_data', {'url': 'http://webhook.site/exfil', 'reason': 'Domain not in allowlist'}),
        ('alert', 'fetch_web_data', {'reason': 'Exfiltration pattern detected'}),
        ('approved', 'fetch_web_data', {'url': 'https://internal-wiki.company.com/search'}),
        ('violation', 'fetch_web_data', {'url': 'http://attacker.com/steal?data=secret', 'reason': 'Blocked domain'}),
        ('approved', 'read_document', {'filename': 'project_M&A_targets.pdf'}),
        ('violation', 'fetch_web_data', {'url': 'http://evil.com/x?q=' + 'A'*300, 'reason': 'URL too long - possible exfiltration'}),
    ]

    for event_type, tool, details in events:
        dashboard.log_event(event_type, tool, details)

    print(f"Generated {len(events)} demo events")
    print(f"Log file: {dashboard.log_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        generate_demo_events()
        print("\nDemo events generated! Now run:")
        print("  streamlit run security_dashboard.py")
    elif len(sys.argv) > 1 and sys.argv[1] == "clear":
        dashboard = SecurityDashboard()
        if dashboard.log_file.exists():
            dashboard.log_file.unlink()
        print("Event log cleared")
    else:
        dashboard = SecurityDashboard()
        dashboard.render_dashboard()
