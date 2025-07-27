#!/usr/bin/env python3
"""
Manual AIP Agent Instruction Deployment Script
Deploy comprehensive German Shepherd logistics expert instructions
"""

import asyncio
import os
from dotenv import load_dotenv
from src.aip.instruction_deployment_service import InstructionDeploymentService
from src.aip.browser_instruction_deployment import BrowserInstructionDeployment
from src.foundry_sdk import FoundryClient
from src.aip.agent_config import AIP_AGENT_CONFIG

load_dotenv()

async def main():
    """Deploy instructions manually"""
    print("🐕 Deploying German Shepherd Logistics Expert Instructions...")
    print("=" * 60)
    
    agent_rid = "ri.aip-agents..agent.e6e9ff2f-0952-4774-98b5-4388a96ddbf1"
    
    foundry_client = FoundryClient(
        auth_token=os.getenv("FOUNDRY_AUTH_TOKEN"),
        foundry_url="https://raiderexpress.palantirfoundry.com"
    )
    
    print(f"🎯 Target Agent RID: {agent_rid}")
    print(f"🌐 Foundry URL: {foundry_client.foundry_url}")
    print(f"🔐 Auth Token: {'Configured' if foundry_client.auth_token else 'Missing'}")
    
    instruction_service = InstructionDeploymentService(foundry_client)
    result = await instruction_service.deploy_instructions()
    
    if result.get("success"):
        print(f"\n✅ Instructions deployed successfully!")
        print(f"   Agent RID: {result['agent_rid']}")
        print(f"   Guidelines: {result['instruction_count']}")
        print(f"   Tools: {result['tool_count']}")
        print(f"   Endpoint: {result.get('successful_endpoint', 'Unknown')}")
        
        verification = await instruction_service.verify_instructions()
        if verification.get("success"):
            print(f"✅ Verification successful: Agent fully configured")
        else:
            print(f"⚠️ Verification failed: {verification.get('error')}")
    else:
        print(f"\n❌ API Deployment failed: {result.get('error')}")
        print(f"⚠️ Attempted endpoints: {result.get('attempted_endpoints', [])}")
        
        print(f"\n🔄 Preparing browser-based deployment...")
        browser_service = BrowserInstructionDeployment(agent_rid)
        browser_result = await browser_service.deploy_through_browser()
        
        if browser_result.get("success"):
            print(f"✅ Browser deployment prepared successfully!")
            
            deployment_instructions = browser_service.get_deployment_instructions()
            print(f"\n📋 Manual Deployment Instructions:")
            for step in deployment_instructions["manual_steps"]:
                print(f"   {step}")
            
            print(f"\n📝 System Prompt to Deploy ({len(deployment_instructions['system_prompt'])} chars):")
            print(f"   {deployment_instructions['system_prompt'][:200]}...")
            
            print(f"\n🛠️ Behavioral Guidelines ({len(deployment_instructions['behavioral_guidelines'])}):")
            for i, guideline in enumerate(deployment_instructions['behavioral_guidelines'][:3], 1):
                print(f"   {i}. {guideline}")
            if len(deployment_instructions['behavioral_guidelines']) > 3:
                print(f"   ... and {len(deployment_instructions['behavioral_guidelines']) - 3} more")
            
            print(f"\n💡 Example Interactions ({len(deployment_instructions['example_interactions'])}):")
            for i, example in enumerate(deployment_instructions['example_interactions'], 1):
                print(f"   {i}. User: {example['user_input']}")
                print(f"      Response: {example['response_pattern'][:100]}...")
        else:
            print(f"❌ Browser deployment preparation failed: {browser_result.get('error')}")
        
        print(f"\n📋 Instructions that should be deployed:")
        instructions = AIP_AGENT_CONFIG["instructions"]
        print(f"   System Prompt: {len(instructions['system_prompt'])} characters")
        print(f"   Guidelines: {len(instructions['behavioral_guidelines'])}")
        print(f"   Examples: {len(instructions['example_interactions'])}")
        print(f"   Tools: {len(AIP_AGENT_CONFIG['tools'])}")

if __name__ == "__main__":
    asyncio.run(main())
