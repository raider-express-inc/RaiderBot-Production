#!/usr/bin/env python3
"""
Comprehensive AIP Agent Instruction Deployment Verification
Verify that German Shepherd logistics expert instructions are actually deployed
"""

import asyncio
import os
from src.aip.instruction_deployment_service import InstructionDeploymentService
from src.aip.browser_instruction_deployment import BrowserInstructionDeployment
from src.foundry_sdk import FoundryClient
from src.aip.agent_config import AIP_AGENT_CONFIG

async def verify_deployment_status():
    """Verify current deployment status of AIP agent instructions"""
    print("🔍 Verifying AIP Agent Instruction Deployment Status")
    print("=" * 60)
    
    agent_rid = "ri.aip-agents..agent.e6e9ff2f-0952-4774-98b5-4388a96ddbf1"
    
    foundry_client = FoundryClient(
        auth_token=os.getenv("FOUNDRY_AUTH_TOKEN"),
        foundry_url="https://raiderexpress.palantirfoundry.com"
    )
    
    print(f"🎯 Agent RID: {agent_rid}")
    print(f"🌐 Agent URL: https://raiderexpress.palantirfoundry.com/workspace/agent-studio-app/view/latest/{agent_rid}")
    
    instruction_service = InstructionDeploymentService(foundry_client)
    
    print(f"\n📋 Configuration Status:")
    instructions = AIP_AGENT_CONFIG["instructions"]
    print(f"   ✅ System Prompt: {len(instructions['system_prompt'])} characters")
    print(f"   ✅ Behavioral Guidelines: {len(instructions['behavioral_guidelines'])} configured")
    print(f"   ✅ Example Interactions: {len(instructions['example_interactions'])} configured")
    print(f"   ✅ Tools: {len(AIP_AGENT_CONFIG['tools'])} configured")
    
    print(f"\n🔄 Testing API Deployment...")
    deployment_result = await instruction_service.deploy_instructions()
    
    if deployment_result.get("success"):
        print(f"✅ API Deployment: SUCCESS")
        print(f"   Endpoint: {deployment_result.get('successful_endpoint')}")
        print(f"   Guidelines: {deployment_result['instruction_count']}")
        print(f"   Tools: {deployment_result['tool_count']}")
    else:
        print(f"❌ API Deployment: FAILED")
        print(f"   Error: {deployment_result.get('error')}")
        print(f"   Attempted: {len(deployment_result.get('attempted_endpoints', []))} endpoints")
    
    print(f"\n🔍 Testing Verification...")
    verification_result = await instruction_service.verify_instructions()
    
    if verification_result.get("success"):
        print(f"✅ Verification: SUCCESS")
        print(f"   Agent Configured: {verification_result.get('agent_configured')}")
        print(f"   Has Instructions: {verification_result.get('has_instructions')}")
        print(f"   Has System Prompt: {verification_result.get('has_system_prompt')}")
        print(f"   Tool Count: {verification_result.get('tool_count')}")
    else:
        print(f"❌ Verification: FAILED")
        print(f"   Error: {verification_result.get('error')}")
    
    print(f"\n🌐 Browser Deployment Preparation...")
    browser_service = BrowserInstructionDeployment(agent_rid)
    browser_result = await browser_service.deploy_through_browser()
    
    if browser_result.get("success"):
        print(f"✅ Browser Deployment: PREPARED")
        print(f"   Method: {browser_result.get('method')}")
        print(f"   Guidelines: {browser_result['guidelines_count']}")
        print(f"   Examples: {browser_result['examples_count']}")
    else:
        print(f"❌ Browser Deployment: FAILED")
        print(f"   Error: {browser_result.get('error')}")
    
    deployment_instructions = browser_service.get_deployment_instructions()
    print(f"\n📝 Manual Deployment Required:")
    print(f"   🌐 Navigate to: {browser_service.agent_url}")
    print(f"   📋 Steps:")
    for step in deployment_instructions["manual_steps"]:
        print(f"     {step}")
    
    print(f"\n🐕 German Shepherd System Prompt Preview:")
    system_prompt = instructions["system_prompt"]
    print(f"   {system_prompt[:300]}...")
    
    print(f"\n🛠️ Behavioral Guidelines Preview:")
    for i, guideline in enumerate(instructions["behavioral_guidelines"][:3], 1):
        print(f"   {i}. {guideline}")
    
    print(f"\n💡 Example Interactions Preview:")
    for i, example in enumerate(instructions["example_interactions"], 1):
        print(f"   {i}. User: {example['user_input']}")
        print(f"      Response: {example['response_pattern'][:150]}...")
    
    overall_status = "DEPLOYED" if deployment_result.get("success") and verification_result.get("success") else "NEEDS_MANUAL_DEPLOYMENT"
    
    print(f"\n📊 Overall Status: {overall_status}")
    
    if overall_status == "NEEDS_MANUAL_DEPLOYMENT":
        print(f"\n⚠️ CRITICAL: Instructions are configured but NOT deployed to live agent")
        print(f"   🔧 Solution: Manual deployment through browser interface required")
        print(f"   🌐 Agent URL: {browser_service.agent_url}")
        print(f"   📋 Follow manual deployment steps above")
    else:
        print(f"\n🎉 SUCCESS: German Shepherd logistics expert instructions are deployed!")
    
    return {
        "overall_status": overall_status,
        "api_deployment": deployment_result.get("success", False),
        "verification": verification_result.get("success", False),
        "browser_prepared": browser_result.get("success", False),
        "agent_url": browser_service.agent_url,
        "manual_deployment_required": overall_status == "NEEDS_MANUAL_DEPLOYMENT"
    }

if __name__ == "__main__":
    asyncio.run(verify_deployment_status())
