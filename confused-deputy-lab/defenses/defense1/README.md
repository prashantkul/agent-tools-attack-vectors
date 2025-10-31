# Defense 1: Tool Permission Model (URL Allowlist)

## Concept

This defense implements a **strict allowlist** on the `fetch_web_data` tool. The security policy lives inside the tool's code and validates every URL before making a request.

## How It Works

1. **Define allowed domains**: A list of trusted internal domains is hardcoded or configured
2. **Validate on every call**: Before making any HTTP request, the tool checks if the domain is in the allowlist
3. **Block malicious requests**: If the domain is not allowed, the request is rejected with a clear error message

## Code Changes

```python
# Security policy
ALLOWED_DOMAINS = [
    "internal-wiki.company.com",
    "api.company.com",
    "docs.company.com"
]

def is_url_allowed(url: str) -> tuple[bool, str]:
    """Check if a URL is allowed according to the security policy."""
    parsed = urlparse(url)
    domain = parsed.netloc

    for allowed_domain in ALLOWED_DOMAINS:
        if domain == allowed_domain or domain.endswith(f".{allowed_domain}"):
            return True, f"Domain {domain} is in allowlist"

    return False, f"Domain {domain} is not in allowlist"

def fetch_web_data(url: str) -> str:
    """Perform HTTP GET with security controls."""
    allowed, reason = is_url_allowed(url)

    if not allowed:
        return f"[SECURITY] Request blocked: {reason}"

    # Proceed with request...
```

## Running the Demo

```bash
cd defenses/defense1
python secure_agent_allowlist.py demo
```

This will demonstrate:
1. The attack being attempted
2. The security check blocking the malicious URL
3. How legitimate internal URLs would be allowed

## Pros and Cons

**Pros:**
- Simple to implement
- Clear and auditable
- Effective against basic exfiltration

**Cons:**
- Security policy is embedded in code (hard to update)
- Requires code changes for policy updates
- No centralized security governance
- Difficult to audit across multiple tools

## Next Step

See **Defense 2** for a better approach using the Model Context Protocol (MCP) to externalize security policies.
