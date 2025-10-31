#!/bin/bash

# Helper script to fetch GitHub issue content
# Usage: ./fetch-issue.sh <issue_number>

ISSUE_NUMBER=${1:-1}
REPO="prashantkul/agent-tools-attack-vectors"

echo "Fetching issue #${ISSUE_NUMBER} from ${REPO}..."

# Create directory if it doesn't exist
mkdir -p .lab-issues

# Fetch issue using curl (no auth needed for public repos)
curl -s "https://api.github.com/repos/${REPO}/issues/${ISSUE_NUMBER}" | \
  jq -r '"# Issue #\(.number): \(.title)\n\n**Author:** @\(.user.login)\n**Created:** \(.created_at)\n**URL:** \(.html_url)\n\n## Description\n\n\(.body)\n\n---\n\n**Labels:** \([.labels[].name] | join(", "))"' \
  > ".lab-issues/issue-${ISSUE_NUMBER}.md"

echo "Issue content saved to .lab-issues/issue-${ISSUE_NUMBER}.md"
cat ".lab-issues/issue-${ISSUE_NUMBER}.md"
