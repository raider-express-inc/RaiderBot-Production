"""
AIP Agent Instruction Deployment Service
Handles deployment of comprehensive agent instructions to Foundry Agent Studio
"""

import httpx
import os
from typing import Dict, Any, Optional
from datetime import datetime
from .agent_config import AIP_AGENT_CONFIG

class InstructionDeploymentService:
    """Service for deploying agent instructions to AIP Studio"""
    
    def __init__(self, foundry_client):
        self.foundry_client = foundry_client
        self.studio_url = f"{foundry_client.foundry_url}/workspace/aip-studio"
        self.agent_rid = os.getenv('AIP_AGENT_RID', 'ri.aip-agents..agent.e6e9ff2f-0952-4774-98b5-4388a96ddbf1')
        
    async def deploy_instructions(self) -> Dict[str, Any]:
        """Deploy comprehensive instructions to AIP agent using multiple API endpoints"""
        try:
            instructions_payload = {
                "agent_rid": self.agent_rid,
                "instructions": AIP_AGENT_CONFIG["instructions"],
                "tools": AIP_AGENT_CONFIG["tools"],
                "capabilities": AIP_AGENT_CONFIG["capabilities"],
                "personality": "german_shepherd_logistics_expert",
                "deployment_timestamp": datetime.now().isoformat()
            }
            
            endpoints_to_try = [
                f"{self.studio_url}/api/agents/{self.agent_rid}/instructions",
                f"{self.studio_url}/api/agents/{self.agent_rid}/configuration",
                f"{self.foundry_client.foundry_url}/workspace/aip-studio/api/agents/{self.agent_rid}/instructions",
                f"{self.foundry_client.foundry_url}/api/aip-studio/agents/{self.agent_rid}/instructions",
                f"{self.foundry_client.foundry_url}/api/v1/agents/{self.agent_rid}/instructions",
                f"{self.foundry_client.foundry_url}/api/v2/agents/{self.agent_rid}/instructions"
            ]
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                for endpoint in endpoints_to_try:
                    try:
                        print(f"🔄 Attempting instruction deployment to: {endpoint}")
                        response = await client.put(endpoint, headers=self.foundry_client.headers, json=instructions_payload)
                        
                        if response.status_code in [200, 201]:
                            print(f"✅ Instructions deployed successfully via: {endpoint}")
                            return {
                                "success": True,
                                "agent_rid": self.agent_rid,
                                "instructions_deployed": True,
                                "deployment_time": datetime.now().isoformat(),
                                "instruction_count": len(AIP_AGENT_CONFIG["instructions"]["behavioral_guidelines"]),
                                "tool_count": len(AIP_AGENT_CONFIG["tools"]),
                                "successful_endpoint": endpoint
                            }
                        elif response.status_code == 404:
                            print(f"⚠️ Endpoint not found: {endpoint}")
                            continue
                        else:
                            print(f"⚠️ Endpoint {endpoint} failed with status {response.status_code}: {response.text}")
                            continue
                    except Exception as e:
                        print(f"⚠️ Endpoint {endpoint} failed with error: {e}")
                        continue
                
                return {
                    "success": False, 
                    "error": f"All AIP Studio API endpoints failed. Attempted: {endpoints_to_try}",
                    "status_code": "multiple_failures",
                    "attempted_endpoints": endpoints_to_try
                }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def verify_instructions(self) -> Dict[str, Any]:
        """Verify that instructions were properly deployed"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.studio_url}/api/agents/{self.agent_rid}",
                    headers=self.foundry_client.headers
                )
                
                if response.status_code == 200:
                    agent_data = response.json()
                    has_instructions = "instructions" in agent_data
                    has_system_prompt = has_instructions and "system_prompt" in agent_data.get("instructions", {})
                    
                    return {
                        "success": True,
                        "agent_configured": True,
                        "has_instructions": has_instructions,
                        "has_system_prompt": has_system_prompt,
                        "tool_count": len(agent_data.get("tools", [])),
                        "verification_time": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Verification failed: {response.text}"
                    }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
