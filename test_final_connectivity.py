#!/usr/bin/env python3
"""
Final connectivity test with corrected MCLEOD_DB.dbo configuration
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from src.snowflake.cortex_analyst_client import cortex_client

def test_final_connectivity():
    """Test final connectivity with corrected database/schema configuration"""
    print("🔍 Testing final Snowflake connectivity with MCLEOD_DB.dbo...")
    print("=" * 60)
    
    tests = [
        ("Connection Test", lambda: cortex_client.connect()),
        ("Health Check", lambda: cortex_client.health_check()['status'] == 'healthy'),
        ("Direct Orders Query", lambda: len(cortex_client.execute_query('SELECT TOP 1 * FROM "dbo"."orders"')) > 0),
        ("Business Query - Orders", lambda: len(cortex_client.natural_language_query("Show me recent orders")['data']) > 0 if cortex_client.natural_language_query("Show me recent orders")['success'] else False),
        ("Business Query - Revenue", lambda: cortex_client.natural_language_query("Show me revenue trends")['success']),
        ("Business Query - Customers", lambda: cortex_client.natural_language_query("Show me top customers")['success']),
        ("MCP Server Health", lambda: cortex_client.health_check()['connection']),
        ("Schema Verification", lambda: cortex_client.config.get('database') == 'MCLEOD_DB' and cortex_client.config.get('schema') == 'dbo')
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"   ✅ {test_name}")
                passed += 1
            else:
                print(f"   ❌ {test_name} - Failed")
        except Exception as e:
            print(f"   ❌ {test_name} - Error: {str(e)[:50]}")
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Final Results:")
    print(f"   Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    if success_rate >= 87.5:
        print(f"   🎯 SUCCESS: Connectivity improved!")
        return True
    else:
        print(f"   ⚠️  Needs improvement")
        return False

if __name__ == "__main__":
    success = test_final_connectivity()
    if success:
        print("\n✅ MCLEOD_DB.dbo connectivity fix successful!")
    else:
        print("\n❌ MCLEOD_DB.dbo connectivity still has issues")
