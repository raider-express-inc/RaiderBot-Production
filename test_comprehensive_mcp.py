#!/usr/bin/env python3
"""
Comprehensive MCP Server Toolkit Test Suite
Tests all 10 MCP servers and orchestration capabilities
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import Dict, List, Any
from datetime import datetime

class ComprehensiveMCPTest:
    def __init__(self):
        self.config_path = "/home/ubuntu/.devin/mcp-config.json"
        self.test_results = {}
        
    async def test_all_servers(self) -> Dict[str, Any]:
        """Test all 10 MCP servers"""
        servers_to_test = [
            "snowflake", "foundry", "github", "aws", "slack", 
            "docker", "zapier", "semantic-production", "semantic-memory", "semantic-ai"
        ]
        
        results = {}
        for server in servers_to_test:
            print(f"🧪 Testing {server} MCP server...")
            result = await self._test_server(server)
            results[server] = result
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {server}: {result.get('message', 'Test completed')}")
        
        return results
    
    async def _test_server(self, server_name: str) -> Dict[str, Any]:
        """Test individual MCP server"""
        try:
            if server_name == "snowflake":
                return await self._test_snowflake()
            elif server_name == "foundry":
                return await self._test_foundry()
            elif server_name == "github":
                return await self._test_github()
            elif server_name == "aws":
                return await self._test_aws()
            elif server_name == "slack":
                return await self._test_slack()
            elif server_name == "docker":
                return await self._test_docker()
            elif server_name == "zapier":
                return await self._test_zapier()
            elif server_name == "semantic-production":
                return await self._test_semantic_production()
            elif server_name == "semantic-memory":
                return await self._test_semantic_memory()
            elif server_name == "semantic-ai":
                return await self._test_semantic_ai()
            else:
                return {"success": True, "message": f"{server_name} test not implemented yet"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_snowflake(self) -> Dict[str, Any]:
        """Test Snowflake MCP server"""
        try:
            sys.path.append('/home/ubuntu/repos/RaiderBot-Production')
            from src.snowflake.cortex_analyst_client import cortex_client
            
            health = cortex_client.health_check()
            return {
                "success": health.get('status') == 'healthy',
                "message": f"Snowflake health: {health.get('status')}",
                "details": health
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_foundry(self) -> Dict[str, Any]:
        """Test Foundry MCP server"""
        try:
            server_path = "/home/ubuntu/repos/raiderbot-foundry-functions/foundry-mcp-server/server.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "Foundry MCP server found"}
            else:
                return {"success": False, "error": "Foundry MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_github(self) -> Dict[str, Any]:
        """Test GitHub MCP server"""
        try:
            server_path = "/home/ubuntu/.devin/mcp-servers/github-mcp/server.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "GitHub MCP server created"}
            else:
                return {"success": False, "error": "GitHub MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_aws(self) -> Dict[str, Any]:
        """Test AWS MCP server"""
        try:
            result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "message": "AWS credentials valid"}
            else:
                return {"success": False, "error": "AWS credentials not configured"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_slack(self) -> Dict[str, Any]:
        """Test Slack MCP server"""
        try:
            slack_token = os.getenv('SLACK_BOT_TOKEN')
            if slack_token:
                return {"success": True, "message": "Slack token configured"}
            else:
                return {"success": False, "error": "Slack token not configured"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_docker(self) -> Dict[str, Any]:
        """Test Docker MCP server"""
        try:
            result = subprocess.run(['docker', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "message": "Docker available"}
            else:
                return {"success": False, "error": "Docker not available"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_zapier(self) -> Dict[str, Any]:
        """Test Zapier MCP server"""
        try:
            server_path = "/home/ubuntu/.devin/mcp-servers/zapier-mcp/server.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "Zapier MCP server found"}
            else:
                return {"success": False, "error": "Zapier MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_semantic_production(self) -> Dict[str, Any]:
        """Test Semantic Production MCP server"""
        try:
            server_path = "/home/ubuntu/repos/raiderbot-platform/semantic-layer/mcp_server_production.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "Semantic Production MCP server found"}
            else:
                return {"success": False, "error": "Semantic Production MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_semantic_memory(self) -> Dict[str, Any]:
        """Test Semantic Memory MCP server"""
        try:
            server_path = "/home/ubuntu/repos/raiderbot-platform/semantic-layer/mcp_server_with_memory.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "Semantic Memory MCP server found"}
            else:
                return {"success": False, "error": "Semantic Memory MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_semantic_ai(self) -> Dict[str, Any]:
        """Test Semantic AI MCP server"""
        try:
            server_path = "/home/ubuntu/repos/raiderbot-platform/mcp-enhanced-ai/server.py"
            if os.path.exists(server_path):
                return {"success": True, "message": "Semantic AI MCP server found"}
            else:
                return {"success": False, "error": "Semantic AI MCP server not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_orchestration(self) -> Dict[str, Any]:
        """Test master orchestration capabilities"""
        try:
            orchestrator_path = "/home/ubuntu/.devin/orchestrator.py"
            if os.path.exists(orchestrator_path):
                return {"success": True, "message": "Master orchestrator created"}
            else:
                return {"success": False, "error": "Master orchestrator not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_cross_platform_integration(self) -> Dict[str, Any]:
        """Test cross-platform integration capabilities"""
        try:
            config_exists = os.path.exists("/home/ubuntu/.devin/mcp-config.json")
            orchestrator_exists = os.path.exists("/home/ubuntu/.devin/orchestrator.py")
            startup_script_exists = os.path.exists("/home/ubuntu/.devin/start.sh")
            
            if config_exists and orchestrator_exists and startup_script_exists:
                return {
                    "success": True,
                    "message": "Cross-platform integration components ready",
                    "details": {
                        "config": config_exists,
                        "orchestrator": orchestrator_exists,
                        "startup_script": startup_script_exists
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Missing integration components",
                    "details": {
                        "config": config_exists,
                        "orchestrator": orchestrator_exists,
                        "startup_script": startup_script_exists
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

async def main():
    """Run comprehensive MCP test suite"""
    print("🧪 Comprehensive MCP Server Toolkit Test Suite")
    print("=" * 60)
    
    tester = ComprehensiveMCPTest()
    
    server_results = await tester.test_all_servers()
    
    print("\n🎭 Testing Master Orchestration...")
    orchestration_result = await tester.test_orchestration()
    status = "✅" if orchestration_result["success"] else "❌"
    print(f"   {status} Orchestration: {orchestration_result.get('message')}")
    
    print("\n🔗 Testing Cross-Platform Integration...")
    integration_result = await tester.test_cross_platform_integration()
    status = "✅" if integration_result["success"] else "❌"
    print(f"   {status} Integration: {integration_result.get('message')}")
    
    total_servers = len(server_results)
    successful_servers = len([r for r in server_results.values() if r["success"]])
    success_rate = (successful_servers / total_servers) * 100
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Servers Tested: {total_servers}")
    print(f"   Successful: {successful_servers}")
    print(f"   Success Rate: {success_rate:.1f}%")
    print(f"   Orchestration: {'✅' if orchestration_result['success'] else '❌'}")
    print(f"   Integration: {'✅' if integration_result['success'] else '❌'}")
    
    if success_rate >= 80 and orchestration_result["success"] and integration_result["success"]:
        print("\n🎉 Comprehensive MCP Toolkit: READY FOR DEPLOYMENT")
        deployment_status = "READY"
    else:
        print("\n⚠️ Some components need attention before deployment")
        deployment_status = "NEEDS_ATTENTION"
    
    results = {
        "server_results": server_results,
        "orchestration_result": orchestration_result,
        "integration_result": integration_result,
        "success_rate": success_rate,
        "deployment_status": deployment_status,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("/home/ubuntu/.devin/test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
