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
        """Deploy comprehensive instructions to AIP agent"""
        try:
            instructions_payload = {
                "agent_rid": self.agent_rid,
                "instructions": AIP_AGENT_CONFIG["instructions"],
                "tools": AIP_AGENT_CONFIG["tools"],
                "capabilities": AIP_AGENT_CONFIG["capabilities"],
                "personality": "german_shepherd_logistics_expert",
                "deployment_timestamp": datetime.now().isoformat()
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.put(
                    f"{self.studio_url}/api/agents/{self.agent_rid}/instructions",
                    headers=self.foundry_client.headers,
                    json=instructions_payload
                )
                
                if response.status_code in [200, 201]:
                    return {
                        "success": True,
                        "agent_rid": self.agent_rid,
                        "instructions_deployed": True,
                        "deployment_time": datetime.now().isoformat(),
                        "instruction_count": len(AIP_AGENT_CONFIG["instructions"]["behavioral_guidelines"]),
                        "tool_count": len(AIP_AGENT_CONFIG["tools"])
                    }
                else:
                    return {
                        "success": False, 
                        "error": f"Deployment failed: {response.text}",
                        "status_code": response.status_code
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
