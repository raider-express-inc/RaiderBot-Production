#!/usr/bin/env python3
"""
Comprehensive Zapier MCP Integration Test
Test and demonstrate all available Zapier MCP capabilities
"""

import os
import sys
import json
import subprocess
from typing import Dict, List

sys.path.append(os.path.dirname(__file__))


def test_mcp_cli_zapier_access():
    """Test mcp-cli access to Zapier servers"""
    print("🔍 Testing mcp-cli Zapier Access")
    print("-" * 40)

    test_configs = [
        {
            "name": "Direct Zapier Server",
            "config": {"mcpServers": {"zapier": {"command": "zapier-mcp-server"}}},
        },
        {
            "name": "Zapier Integration Server",
            "config": {
                "mcpServers": {
                    "zapier-integration": {
                        "command": "python",
                        "args": ["-m", "mcp_zapier"],
                    }
                }
            },
        },
        {
            "name": "Zapier Webhook Server",
            "config": {
                "mcpServers": {"zapier-webhook": {"command": "zapier-webhook-server"}}
            },
        },
    ]

    results = []
    for test in test_configs:
        try:
            config_json = json.dumps(test["config"])
            result = subprocess.run(
                ["mcp-cli", "tool", "list", "--config", config_json],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and "Tools available" in result.stdout:
                print(f"   ✅ {test['name']}: FOUND")
                results.append(
                    {
                        "name": test["name"],
                        "status": "available",
                        "output": result.stdout,
                    }
                )
            else:
                print(f"   ❌ {test['name']}: Not available")
                results.append(
                    {
                        "name": test["name"],
                        "status": "unavailable",
                        "error": result.stderr,
                    }
                )
        except Exception as e:
            print(f"   ❌ {test['name']}: Error - {e}")
            results.append({"name": test["name"], "status": "error", "error": str(e)})

    return results


def test_existing_mcp_servers_for_zapier():
    """Test existing MCP servers for Zapier-related tools"""
    print("\n🔍 Testing Existing MCP Servers for Zapier Tools")
    print("-" * 50)

    config_path = "/home/ubuntu/repos/raiderbot-foundry-functions/mcp-config.json"
    if not os.path.exists(config_path):
        print("   ❌ MCP config file not found")
        return []

    try:
        result = subprocess.run(
            ["mcp-cli", "tool", "list", "--config", f"$(cat {config_path})"],
            capture_output=True,
            text=True,
            timeout=30,
            shell=True,
        )

        if result.returncode == 0:
            zapier_tools = []
            lines = result.stdout.split("\n")
            current_server = None

            for line in lines:
                if "Tools available on server" in line:
                    current_server = line.split("'")[1] if "'" in line else "unknown"
                elif "Tool:" in line and any(
                    keyword in line.lower()
                    for keyword in ["zapier", "webhook", "automation"]
                ):
                    tool_name = line.replace("Tool:", "").strip()
                    zapier_tools.append({"server": current_server, "tool": tool_name})

            if zapier_tools:
                print("   ✅ Found Zapier-related tools:")
                for tool in zapier_tools:
                    print(f"      - {tool['tool']} (server: {tool['server']})")
            else:
                print("   ℹ️ No Zapier-specific tools found in existing servers")

            return zapier_tools
        else:
            print(f"   ❌ Failed to list tools: {result.stderr}")
            return []
    except Exception as e:
        print(f"   ❌ Error testing existing servers: {e}")
        return []


def test_python_zapier_packages():
    """Test for Python Zapier packages that might provide MCP integration"""
    print("\n🔍 Testing Python Zapier Packages")
    print("-" * 35)

    packages_to_check = [
        "zapier",
        "zapier-platform",
        "mcp-zapier",
        "zapier-mcp",
        "zapier-webhook",
        "zapier-cli",
    ]

    available_packages = []
    for package in packages_to_check:
        try:
            result = subprocess.run(
                [
                    "python",
                    "-c",
                    f'import {package.replace("-", "_")}; print("✅ {package} available")',
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"   ✅ {package}: Available")
                available_packages.append(package)
            else:
                print(f"   ❌ {package}: Not available")
        except Exception as e:
            print(f"   ❌ {package}: Error - {e}")

    return available_packages


def test_environment_zapier_config():
    """Test for Zapier configuration in environment"""
    print("\n🔍 Testing Environment Zapier Configuration")
    print("-" * 45)

    zapier_env_vars = [
        "ZAPIER_API_KEY",
        "ZAPIER_WEBHOOK_URL",
        "MCP_ZAPIER_ENABLED",
        "ZAPIER_CLIENT_ID",
        "ZAPIER_CLIENT_SECRET",
    ]

    found_config = {}
    for var in zapier_env_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: Configured")
            found_config[var] = "***configured***"
        else:
            print(f"   ❌ {var}: Not set")

    return found_config


def demonstrate_zapier_capabilities(zapier_tools: List[Dict]):
    """Demonstrate any found Zapier capabilities"""
    print("\n🚀 Demonstrating Zapier Capabilities")
    print("-" * 35)

    if not zapier_tools:
        print("   ℹ️ No Zapier tools available to demonstrate")
        return []

    demonstrations = []
    for tool in zapier_tools:
        try:
            print(f"   🧪 Testing {tool['tool']} on {tool['server']}...")

            config_path = (
                "/home/ubuntu/repos/raiderbot-foundry-functions/mcp-config.json"
            )
            result = subprocess.run(
                [
                    "mcp-cli",
                    "tool",
                    "call",
                    "--server",
                    tool["server"],
                    "--tool",
                    tool["tool"],
                    "--config",
                    f"$(cat {config_path})",
                    "--args",
                    "{}",
                ],
                capture_output=True,
                text=True,
                timeout=15,
                shell=True,
            )

            if result.returncode == 0:
                print(f"      ✅ Successfully called {tool['tool']}")
                demonstrations.append(
                    {
                        "tool": tool["tool"],
                        "server": tool["server"],
                        "result": result.stdout[:500] + "..."
                        if len(result.stdout) > 500
                        else result.stdout,
                    }
                )
            else:
                print(f"      ❌ Failed to call {tool['tool']}: {result.stderr}")
        except Exception as e:
            print(f"      ❌ Error demonstrating {tool['tool']}: {e}")

    return demonstrations


def main():
    """Run comprehensive Zapier MCP integration test"""
    print("🧪 Comprehensive Zapier MCP Integration Test")
    print("=" * 50)

    mcp_cli_results = test_mcp_cli_zapier_access()

    zapier_tools = test_existing_mcp_servers_for_zapier()

    python_packages = test_python_zapier_packages()

    env_config = test_environment_zapier_config()

    demonstrations = demonstrate_zapier_capabilities(zapier_tools)

    print("\n📊 Zapier MCP Integration Summary")
    print("=" * 35)

    total_capabilities = (
        len([r for r in mcp_cli_results if r["status"] == "available"])
        + len(zapier_tools)
        + len(python_packages)
    )

    print(
        f"🔍 MCP CLI Zapier Servers: {len([r for r in mcp_cli_results if r['status'] == 'available'])}"
    )
    print(f"🛠️ Zapier Tools in Existing Servers: {len(zapier_tools)}")
    print(f"📦 Python Zapier Packages: {len(python_packages)}")
    print(f"⚙️ Environment Variables: {len(env_config)}")
    print(f"🚀 Successful Demonstrations: {len(demonstrations)}")
    print(f"📈 Total Zapier Capabilities: {total_capabilities}")

    if total_capabilities > 0:
        print("\n✅ Zapier MCP integration capabilities found!")
        return True
    else:
        print("\n❌ No Zapier MCP integration capabilities available")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
