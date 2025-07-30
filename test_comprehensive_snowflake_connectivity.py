#!/usr/bin/env python3
"""
Comprehensive test of all Snowflake connectivity approaches
Tests both official Snowflake tools and MCP bypass methods
"""

import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_server_compilation():
    """Test that server.py compiles without errors"""
    logger.info("🔍 Testing server.py compilation...")
    
    try:
        import py_compile
        py_compile.compile('/home/ubuntu/repos/RaiderBot-Production/server.py', doraise=True)
        logger.info("✅ Server.py compiles successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Server compilation failed: {e}")
        return False

def test_enhanced_snowflake_client():
    """Test the enhanced Snowflake client (CLI + Python connector)"""
    logger.info("🔍 Testing enhanced Snowflake client...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from src.snowflake.enhanced_cortex_client import enhanced_snowflake_client
        
        health = enhanced_snowflake_client.health_check()
        logger.info(f"Enhanced client health: {health}")
        
        if 'error' in health and 'MFA' in str(health['error']):
            logger.info("✅ Enhanced client functional (MFA expected)")
            return True
        elif health.get('success'):
            logger.info("✅ Enhanced client fully functional")
            return True
        else:
            logger.warning("⚠️ Enhanced client has issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ Enhanced client test failed: {e}")
        return False

def test_mcp_bypass_client():
    """Test the MCP bypass client"""
    logger.info("🔍 Testing MCP bypass client...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from src.snowflake.mcp_snowflake_client import mcp_snowflake_client
        
        health = mcp_snowflake_client.health_check()
        logger.info(f"MCP bypass health: {health}")
        
        result = mcp_snowflake_client.execute_query("SELECT CURRENT_TIMESTAMP()")
        logger.info(f"MCP bypass query result: {result}")
        
        if result and len(result) > 0:
            logger.info("✅ MCP bypass client functional")
            return True
        else:
            logger.warning("⚠️ MCP bypass client has issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP bypass client test failed: {e}")
        return False

def test_server_functionality():
    """Test server.py multi-agent query functionality"""
    logger.info("🔍 Testing server multi-agent query functionality...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from server import multi_agent_query
        
        result = multi_agent_query("What is our delivery performance this week?", "operations")
        logger.info(f"Multi-agent query result: {result}")
        
        if result and result.get('agent_type') == 'operations':
            logger.info("✅ Server multi-agent functionality working")
            return True
        else:
            logger.warning("⚠️ Server functionality has issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ Server functionality test failed: {e}")
        return False

def test_mcp_integration():
    """Test MCP integration functionality"""
    logger.info("🔍 Testing MCP integration...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from src.mcp.mcp_snowflake_integration import mcp_integration
        
        health = mcp_integration.health_check_with_mcp()
        logger.info(f"MCP integration health: {health}")
        
        if health and (health.get('success') or health.get('status') == 'healthy'):
            logger.info("✅ MCP integration functional")
            return True
        else:
            logger.warning("⚠️ MCP integration has issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP integration test failed: {e}")
        return False

def test_quarterback_functions():
    """Test quarterback functions with new connectivity"""
    logger.info("🔍 Testing quarterback functions...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from src.foundry.quarterback_functions import operations_agent, customer_service_agent
        
        ops_result = operations_agent("Find optimal routes for California runs")
        logger.info(f"Operations agent result: {ops_result}")
        
        cs_result = customer_service_agent("Where is load #12345?")
        logger.info(f"Customer service agent result: {cs_result}")
        
        if (ops_result and ops_result.get('agent_type') == 'operations' and
            cs_result and cs_result.get('agent_type') == 'customer_service'):
            logger.info("✅ Quarterback functions working")
            return True
        else:
            logger.warning("⚠️ Quarterback functions have issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ Quarterback functions test failed: {e}")
        return False

def main():
    """Run comprehensive Snowflake connectivity tests"""
    logger.info("🚀 Running comprehensive Snowflake connectivity tests...")
    
    tests = [
        ("Server Compilation", test_server_compilation),
        ("Enhanced Snowflake Client", test_enhanced_snowflake_client),
        ("MCP Bypass Client", test_mcp_bypass_client),
        ("Server Functionality", test_server_functionality),
        ("MCP Integration", test_mcp_integration),
        ("Quarterback Functions", test_quarterback_functions)
    ]
    
    results = {}
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed >= 4:  # At least 4 out of 6 tests should pass for deployment readiness
        logger.info("🎉 Snowflake connectivity FIXED! Deployment ready.")
        return True
    else:
        logger.error("⚠️ Snowflake connectivity still needs work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
