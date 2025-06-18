#!/usr/bin/env python3
"""
Pre-deployment test for RaiderBot MCP Server
Verifies everything works before cloud deployment
"""

import os
import sys
import json
from datetime import datetime

# Set environment variables for testing
os.environ['SNOWFLAKE_ACCOUNT'] = 'LI21842-WW07444'
os.environ['SNOWFLAKE_USER'] = 'ASH073108'
os.environ['SNOWFLAKE_PASSWORD'] = 'Phi1848gam!'
os.environ['SNOWFLAKE_WAREHOUSE'] = 'TABLEAU_CONNECT'
os.environ['SNOWFLAKE_DATABASE'] = 'RAIDER_DB'
os.environ['SNOWFLAKE_SCHEMA'] = 'SQL_SERVER_DBO'

def test_server_import():
    """Test that server.py imports correctly"""
    print("🔍 Testing server import...")
    try:
        from server import sf_client, search_orders, revenue_summary, health_check
        print("✅ Server imports successful")
        return True
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

def test_snowflake_connection():
    """Test Snowflake connection"""
    print("🔍 Testing Snowflake connection...")
    try:
        from server import sf_client
        health = sf_client.health_check()
        if health['status'] == 'healthy':
            print("✅ Snowflake connection healthy")
            print(f"   User: {health['user']}")
            print(f"   Database: {health['database']}")
            return True
        else:
            print(f"❌ Snowflake unhealthy: {health.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Snowflake test failed: {e}")
        return False

def test_business_logic():
    """Test TMS vs TMS2 business logic"""
    print("🔍 Testing TMS vs TMS2 business logic...")
    try:
        from server import search_orders
        result = search_orders("TMS vs TMS2 orders today")
        
        if 'error' in result:
            print(f"❌ Business logic failed: {result['error']}")
            return False
        
        if 'results' in result and len(result['results']) > 0:
            print("✅ Business logic working")
            for company in result['results']:
                print(f"   {company['company_name']}: {company['total_orders']:,} orders")
            return True
        else:
            print("⚠️ Business logic returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Business logic test failed: {e}")
        return False

def test_all_tools():
    """Test all MCP tools"""
    print("🔍 Testing all MCP tools...")
    try:
        from server import search_orders, revenue_summary, analyze_customer, sql_query, health_check
        
        # Test each tool
        tools_results = {
            "search_orders": search_orders("recent orders"),
            "revenue_summary": revenue_summary("week"),
            "analyze_customer": analyze_customer("top_customers", 5),
            "sql_query": sql_query("SELECT COMPANY_ID, COUNT(*) as cnt FROM ORDERS GROUP BY COMPANY_ID LIMIT 5"),
            "health_check": health_check()
        }
        
        success_count = 0
        for tool_name, result in tools_results.items():
            if 'error' not in result:
                print(f"   ✅ {tool_name}: Working")
                success_count += 1
            else:
                print(f"   ❌ {tool_name}: {result['error']}")
        
        if success_count == len(tools_results):
            print("✅ All MCP tools working")
            return True
        else:
            print(f"⚠️ {success_count}/{len(tools_results)} tools working")
            return False
            
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def main():
    """Run all pre-deployment tests"""
    print("🚀 RaiderBot Pre-Deployment Test Suite")
    print("=" * 60)
    
    tests = [
        ("Server Import", test_server_import),
        ("Snowflake Connection", test_snowflake_connection),
        ("Business Logic", test_business_logic),
        ("All MCP Tools", test_all_tools)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED! Ready for cloud deployment! 🚀")
        print("\nNext steps:")
        print("1. Open Cursor Cloud")
        print("2. Create new project from this directory")
        print("3. Set environment variables")
        print("4. Deploy!")
        return True
    else:
        print("❌ Some tests failed. Fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
