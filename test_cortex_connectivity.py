#!/usr/bin/env python3
"""
Test the enhanced Cortex Analyst connectivity fix
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from src.snowflake.cortex_analyst_client import cortex_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_cortex_connectivity():
    """Test the enhanced Snowflake connectivity with Cortex capabilities"""
    print("🧪 Testing Enhanced Snowflake Connectivity with Cortex Analyst")
    print("=" * 70)
    
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'tests': [],
        'overall_status': 'UNKNOWN'
    }
    
    try:
        print("1️⃣ Testing basic connectivity...")
        health = cortex_client.health_check()
        test_results['tests'].append({
            'test': 'basic_connectivity',
            'status': health['status'],
            'details': health
        })
        
        if health['status'] == 'healthy':
            print(f"✅ Connection successful")
            print(f"   Account: {health.get('account', 'N/A')}")
            print(f"   Database: {health.get('database', 'N/A')}")
            print(f"   Cortex Enabled: {health.get('cortex_enabled', False)}")
            print(f"   Cortex Status: {health.get('cortex_status', 'unknown')}")
        else:
            print(f"❌ Connection failed: {health.get('error', 'Unknown error')}")
        
        print("\n2️⃣ Testing natural language query capabilities...")
        nl_test_queries = [
            "What is the current time?",
            "Show me recent orders",
            "How many customers do we have?",
            "What is our revenue this month?"
        ]
        
        for query in nl_test_queries:
            try:
                result = cortex_client.natural_language_query(query)
                test_results['tests'].append({
                    'test': f'nl_query_{query[:20]}',
                    'status': 'success' if result['success'] else 'failed',
                    'method': result.get('method', 'unknown'),
                    'cortex_enabled': result.get('cortex_enabled', False)
                })
                
                if result['success']:
                    print(f"✅ Query: '{query}' -> Method: {result.get('method', 'unknown')}")
                    if 'data' in result and result['data']:
                        print(f"   Data rows: {len(result['data'])}")
                else:
                    print(f"❌ Query failed: '{query}' -> {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Query exception: '{query}' -> {str(e)}")
                test_results['tests'].append({
                    'test': f'nl_query_{query[:20]}',
                    'status': 'exception',
                    'error': str(e)
                })
        
        print("\n3️⃣ Testing direct SQL execution...")
        sql_tests = [
            "SELECT CURRENT_TIMESTAMP() as current_time",
            "SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'SQL_SERVER_DBO'",
            "SELECT 'Connectivity test successful' as message"
        ]
        
        for sql in sql_tests:
            try:
                result = cortex_client.execute_query(sql)
                test_results['tests'].append({
                    'test': f'sql_execution',
                    'status': 'success',
                    'rows': len(result) if result else 0
                })
                print(f"✅ SQL executed successfully: {len(result) if result else 0} rows")
                
            except Exception as e:
                print(f"❌ SQL execution failed: {str(e)}")
                test_results['tests'].append({
                    'test': f'sql_execution',
                    'status': 'failed',
                    'error': str(e)
                })
        
        print("\n4️⃣ Testing authentication method...")
        token = os.getenv('SNOWFLAKE_ACCESS_TOKEN')
        user = os.getenv('SNOWFLAKE_USER')
        password = os.getenv('SNOWFLAKE_PASSWORD')
        
        auth_method = "unknown"
        if token:
            auth_method = "programmatic_access_token"
        elif user and password:
            auth_method = "user_password"
        else:
            auth_method = "no_credentials"
        
        print(f"🔑 Authentication method: {auth_method}")
        test_results['authentication_method'] = auth_method
        
        successful_tests = sum(1 for test in test_results['tests'] if test['status'] == 'success')
        total_tests = len(test_results['tests'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        if success_rate >= 80:
            test_results['overall_status'] = 'CONNECTIVITY_FIXED'
        elif success_rate >= 50:
            test_results['overall_status'] = 'PARTIAL_CONNECTIVITY'
        else:
            test_results['overall_status'] = 'CONNECTIVITY_ISSUES'
        
        print(f"\n📊 Test Summary:")
        print(f"   Successful tests: {successful_tests}/{total_tests}")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Overall status: {test_results['overall_status']}")
        
        import json
        with open("cortex_connectivity_test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n📄 Test results saved to cortex_connectivity_test_results.json")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        test_results['overall_status'] = 'TEST_SUITE_FAILED'
        test_results['error'] = str(e)
        return test_results
    
    finally:
        cortex_client.close()

if __name__ == "__main__":
    results = asyncio.run(test_cortex_connectivity())
    
    print("\n" + "="*70)
    print("🎯 CONNECTIVITY FIX ASSESSMENT")
    print("="*70)
    
    if results['overall_status'] == 'CONNECTIVITY_FIXED':
        print("✅ SUCCESS: Snowflake connectivity issues have been resolved!")
        print("   Enhanced Cortex Analyst client is working properly")
        print("   Standardized authentication is functional")
        print("   Natural language query capabilities are available")
    elif results['overall_status'] == 'PARTIAL_CONNECTIVITY':
        print("⚠️ PARTIAL: Some connectivity improvements achieved")
        print("   Basic connection working but some features may be limited")
        print("   Consider checking Cortex availability in your Snowflake account")
    else:
        print("❌ ISSUES REMAIN: Connectivity problems persist")
        print("   Check authentication credentials and account permissions")
        print("   Verify Snowflake account supports Cortex features")
    
    exit(0 if results['overall_status'] == 'CONNECTIVITY_FIXED' else 1)
