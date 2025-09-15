#!/usr/bin/env python3
"""
Test Consolidated RaiderBot Functionality
Verify all consolidated components work correctly
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))


def test_quarterback_functions():
    """Test consolidated quarterback functions"""
    print("🐕 Testing Consolidated Quarterback Functions...")

    try:
        from src.foundry.quarterback_functions import (
            process_user_query,
            autonomous_decision_making,
        )

        test_query = "Emergency route optimization needed"
        result = process_user_query(test_query)

        if result.get("quarterback_decision"):
            print(
                f"✅ process_user_query working: {result['intent']} with confidence {result['confidence']}"
            )
        else:
            print(f"❌ process_user_query failed: {result}")
            return False

        test_scenario = {"type": "route_optimization", "priority": "high"}
        decision_result = autonomous_decision_making(test_scenario)

        if decision_result.get("autonomous"):
            print(
                f"✅ autonomous_decision_making working: {decision_result['decision']}"
            )
        else:
            print(f"❌ autonomous_decision_making failed: {decision_result}")
            return False

        return True

    except Exception as e:
        print(f"❌ Quarterback functions test error: {e}")
        return False


def test_unified_snowflake_connection():
    """Test unified Snowflake connection"""
    print("🔌 Testing Unified Snowflake Connection...")

    try:
        from src.snowflake.unified_connection import snowflake_client

        result = snowflake_client.execute_query(
            "SELECT CURRENT_TIMESTAMP() as test_time"
        )

        if result["success"]:
            print(f"✅ Snowflake connection working: {result['rows'][0]}")
            return True
        else:
            print(f"❌ Snowflake connection failed: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Snowflake connection test error: {e}")
        return False


def test_unified_mcp_server():
    """Test unified MCP server components"""
    print("🚀 Testing Unified MCP Server...")

    try:
        from src.mcp.unified_mcp_server import UnifiedRaiderBotMCP

        server = UnifiedRaiderBotMCP()

        if server.server:
            print(f"✅ Unified MCP server initialized: {server.server.name}")
            return True
        else:
            print("❌ Unified MCP server initialization failed")
            return False

    except Exception as e:
        print(f"❌ Unified MCP server test error: {e}")
        return False


def test_simplified_deployment():
    """Test simplified deployment script"""
    print("🎯 Testing Simplified Deployment...")

    try:
        from deploy_simplified import deploy_to_foundry

        result = deploy_to_foundry()

        if result["success"]:
            print(f"✅ Simplified deployment working: {result['message']}")
            return True
        else:
            print(f"❌ Simplified deployment failed: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ Simplified deployment test error: {e}")
        return False


def main():
    """Run all consolidation tests"""
    print("🧪 Running Consolidated RaiderBot Functionality Tests...")
    print("=" * 60)

    tests = [
        ("Quarterback Functions", test_quarterback_functions),
        ("Unified Snowflake Connection", test_unified_snowflake_connection),
        ("Unified MCP Server", test_unified_mcp_server),
        ("Simplified Deployment", test_simplified_deployment),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        print("-" * 40)

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All consolidated components working correctly!")
        print("✅ Ready for deployment and PR creation")
        return True
    else:
        print(f"❌ {total - passed} tests failed - consolidation needs fixes")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
