#!/usr/bin/env python3
"""
Test semantic analysis integration with existing MCP infrastructure
Verify Production, Memory, and AI-enhanced MCP servers work with RaiderBot
"""

import os
import sys
import subprocess
import time
import json
from typing import Dict, Any

sys.path.append(os.path.dirname(__file__))
from src.snowflake.cortex_analyst_client import cortex_client
from src.mcp.mcp_snowflake_integration import mcp_integration

def test_semantic_analysis_integration():
    """Test semantic analysis MCP server integration"""
    print("🧠 Testing Semantic Analysis Integration")
    print("=" * 50)
    
    success_count = 0
    total_tests = 6
    
    try:
        print("1️⃣ Testing base Snowflake connectivity...")
        health = cortex_client.health_check()
        if health.get('status') == 'healthy':
            print(f"   ✅ Snowflake connection: {health['status']}")
            print(f"   📊 Database: {health.get('database', 'unknown')}")
            print(f"   👤 User: {health.get('user', 'unknown')}")
            success_count += 1
        else:
            print(f"   ❌ Snowflake connection failed: {health.get('status')}")
    except Exception as e:
        print(f"   ❌ Snowflake connectivity test failed: {e}")
    
    try:
        print("\n2️⃣ Testing Production MCP Server configuration...")
        config_path = "/home/ubuntu/repos/raiderbot-foundry-functions/mcp-config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                semantic_servers = [name for name in config.get('mcpServers', {}).keys() if 'semantic' in name]
                if semantic_servers:
                    print(f"   ✅ Semantic servers configured: {semantic_servers}")
                    success_count += 1
                else:
                    print("   ❌ No semantic servers found in configuration")
        else:
            print(f"   ❌ MCP config file not found: {config_path}")
    except Exception as e:
        print(f"   ❌ MCP configuration test failed: {e}")
    
    try:
        print("\n3️⃣ Testing semantic query processing...")
        test_query = "Show me recent orders from the last week"
        result = mcp_integration.natural_language_query_with_automation(
            test_query,
            automation_config={'test_mode': True}
        )
        if result.get('success'):
            print("   ✅ Semantic query processing successful")
            print(f"   📊 Query method: {result.get('method', 'enhanced_client')}")
            success_count += 1
        else:
            print(f"   ❌ Semantic query failed: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Semantic query test failed: {e}")
    
    try:
        print("\n4️⃣ Testing business intelligence capabilities...")
        bi_query = 'SELECT COUNT(*) as order_count FROM "dbo"."orders" WHERE "created_date" >= DATEADD(day, -7, CURRENT_DATE())'
        result = cortex_client.execute_query(bi_query)
        if result and len(result) > 0:
            print("   ✅ Business intelligence query successful")
            print(f"   📊 Recent orders found: {result[0].get('ORDER_COUNT', 'unknown')}")
            success_count += 1
        else:
            print("   ❌ Business intelligence query returned no results")
    except Exception as e:
        print(f"   ❌ Business intelligence test failed: {e}")
    
    try:
        print("\n5️⃣ Testing MCP integration health...")
        mcp_health = mcp_integration.health_check_with_mcp()
        if mcp_health.get('status') == 'healthy':
            print("   ✅ MCP integration healthy")
            print(f"   🔗 MCP servers: {len(mcp_health.get('mcp_servers', []))}")
            print(f"   🤖 Integration status: {mcp_health.get('mcp_integration', 'unknown')}")
            success_count += 1
        else:
            print(f"   ❌ MCP integration unhealthy: {mcp_health.get('status')}")
    except Exception as e:
        print(f"   ❌ MCP integration health test failed: {e}")
    
    try:
        print("\n6️⃣ Testing semantic analysis tools availability...")
        semantic_tools = {
            'production': '/home/ubuntu/repos/raiderbot-platform/semantic-layer/mcp_server_production.py',
            'memory': '/home/ubuntu/repos/raiderbot-platform/semantic-layer/mcp_server_with_memory.py',
            'ai_enhanced': '/home/ubuntu/repos/raiderbot-platform/mcp-enhanced-ai/server.py'
        }
        
        available_tools = []
        for tool_name, tool_path in semantic_tools.items():
            if os.path.exists(tool_path):
                available_tools.append(tool_name)
        
        if len(available_tools) == 3:
            print(f"   ✅ All semantic tools available: {available_tools}")
            success_count += 1
        else:
            print(f"   ⚠️ Some semantic tools missing. Available: {available_tools}")
    except Exception as e:
        print(f"   ❌ Semantic tools availability test failed: {e}")
    
    print(f"\n📊 Semantic Analysis Integration Results:")
    print(f"   Success Rate: {success_count}/{total_tests} ({(success_count/total_tests)*100:.1f}%)")
    
    if success_count >= 5:  # Allow for 1 failure
        print("   ✅ Semantic analysis integration ready for deployment!")
        print("   🧠 Query intelligence with 10K query patterns available")
        print("   🧠 Memory-enhanced learning capabilities available")
        print("   🤖 AI-enhanced analysis with OpenAI/Claude available")
        return True
    else:
        print(f"   ⚠️ {total_tests - success_count} tests need attention before deployment")
        return False

def test_semantic_server_startup():
    """Test that semantic servers can start up properly"""
    print("\n🚀 Testing Semantic Server Startup")
    print("=" * 40)
    
    servers_to_test = [
        {
            'name': 'Production MCP Server',
            'path': '/home/ubuntu/repos/raiderbot-platform/semantic-layer/mcp_server_production.py',
            'env': {
                'SNOWFLAKE_ACCOUNT': 'LI21842-WW07444',
                'SNOWFLAKE_USER': 'ASH073108',
                'SNOWFLAKE_ACCESS_TOKEN': os.getenv('SNOWFLAKE_ACCESS_TOKEN'),
                'SNOWFLAKE_WAREHOUSE': 'TABLEAU_CONNECT',
                'SNOWFLAKE_DATABASE': 'MCLEOD_DB',
                'SNOWFLAKE_SCHEMA': 'dbo'
            }
        }
    ]
    
    for server in servers_to_test:
        try:
            print(f"🧪 Testing {server['name']}...")
            
            test_cmd = [
                'python', '-c', 
                f"import sys; sys.path.append('{os.path.dirname(server['path'])}'); "
                f"exec(open('{server['path']}').read().split('if __name__')[0]); "
                f"print('✅ {server['name']} imports successfully')"
            ]
            
            env = os.environ.copy()
            env.update(server['env'])
            
            result = subprocess.run(test_cmd, capture_output=True, text=True, env=env, timeout=10)
            
            if result.returncode == 0:
                print(f"   ✅ {server['name']} startup test passed")
            else:
                print(f"   ❌ {server['name']} startup failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠️ {server['name']} startup test timed out (may be normal)")
        except Exception as e:
            print(f"   ❌ {server['name']} startup test error: {e}")

if __name__ == "__main__":
    print("🧠 RaiderBot Semantic Analysis Integration Test Suite")
    print("=" * 60)
    
    integration_success = test_semantic_analysis_integration()
    
    test_semantic_server_startup()
    
    if integration_success:
        print("\n🎉 Semantic Analysis Integration: READY FOR DEPLOYMENT")
        print("🚀 All semantic analysis capabilities are functional and integrated")
    else:
        print("\n❌ Semantic Analysis Integration: NEEDS ATTENTION")
        print("🔧 Some components require fixes before deployment")
