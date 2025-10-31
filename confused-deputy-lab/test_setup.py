#!/usr/bin/env python3
"""
Setup Test Script
Verifies that the lab environment is correctly configured.
"""

import sys
import os
from pathlib import Path


def test_python_version():
    """Check Python version."""
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.9+)")
        return False


def test_imports():
    """Check if required packages are installed."""
    print("\nTesting required packages:")
    packages = [
        ("google.genai", "google-genai"),
        ("requests", "requests"),
        ("yaml", "pyyaml"),
        ("streamlit", "streamlit"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
    ]

    all_ok = True
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} (run: pip install {package_name})")
            all_ok = False

    return all_ok


def test_api_key():
    """Check if GOOGLE_API_KEY is set."""
    print("\nTesting API key...", end=" ")
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print(f"✅ Set ({len(api_key)} characters)")
        return True
    else:
        print("❌ GOOGLE_API_KEY not set")
        print("   Run: export GOOGLE_API_KEY='your-key'")
        return False


def test_documents():
    """Check if document files exist."""
    print("\nTesting document files:")
    docs_dir = Path(__file__).parent / "documents"
    required_files = [
        "market_summary.pdf",
        "public_report.txt",
        "project_M&A_targets.pdf"
    ]

    all_ok = True
    for filename in required_files:
        file_path = docs_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {filename} ({size} bytes)")
        else:
            print(f"  ❌ {filename} (missing)")
            all_ok = False

    return all_ok


def test_agent_files():
    """Check if agent files exist."""
    print("\nTesting agent files:")
    agent_dir = Path(__file__).parent / "agent"
    required_files = [
        "vulnerable_agent.py",
        "interactive_agent.py"
    ]

    all_ok = True
    for filename in required_files:
        file_path = agent_dir / filename
        if file_path.exists():
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} (missing)")
            all_ok = False

    return all_ok


def test_defense_files():
    """Check if defense files exist."""
    print("\nTesting defense files:")
    defenses_dir = Path(__file__).parent / "defenses"
    required_files = [
        "defense1/secure_agent_allowlist.py",
        "defense2/mcp_tool_inspector.py",
        "defense2/mcp_security_policy.yaml",
        "defense3/security_dashboard.py"
    ]

    all_ok = True
    for filename in required_files:
        file_path = defenses_dir / filename
        if file_path.exists():
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} (missing)")
            all_ok = False

    return all_ok


def test_google_api():
    """Test connection to Google API."""
    print("\nTesting Google API connection...", end=" ")

    if not os.environ.get("GOOGLE_API_KEY"):
        print("⏭️  Skipped (API key not set)")
        return None

    try:
        from google import genai
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

        # Try to list models (lightweight check)
        response = client.models.list()
        print("✅ Connection successful")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)[:50]}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("CONFUSED DEPUTY LAB - SETUP TEST")
    print("="*60)

    tests = [
        test_python_version(),
        test_imports(),
        test_api_key(),
        test_documents(),
        test_agent_files(),
        test_defense_files(),
    ]

    # Optional API test
    api_test = test_google_api()
    if api_test is not None:
        tests.append(api_test)

    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)

    passed = sum(1 for t in tests if t)
    total = len(tests)

    print(f"\nPassed: {passed}/{total}")

    if all(tests):
        print("\n✅ All tests passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Run the interactive agent: python agent/interactive_agent.py")
        print("  2. Try the attack demonstrations")
        print("  3. Explore the defenses")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nSee SETUP.md for detailed setup instructions.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
