#!/usr/bin/env python3
"""
Deploy RaiderBot using Continue.dev integration instead of direct API calls
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

from src.dev_tools.continue_integration_service import ContinueIntegrationService
from src.consolidation.unified_system_service import UnifiedRaiderBotSystem

async def deploy_via_continue():
    """Deploy using Continue.dev integration"""
    print("🚀 Deploying RaiderBot via Continue.dev integration...")
    
    load_dotenv()
    
    try:
        print("1️⃣ Initializing Continue.dev integration...")
        continue_service = ContinueIntegrationService()
        
        print("2️⃣ Getting Foundry scaffolding commands...")
        commands = continue_service.get_foundry_scaffolding_commands()
        print(f"Available commands: {len(commands)}")
        
        print("3️⃣ Scaffolding Workshop application...")
        workshop_result = continue_service.scaffold_foundry_component(
            "Workshop application", 
            "RaiderBot Enterprise Dashboard with German Shepherd AI assistant for logistics automation"
        )
        print(f"Workshop scaffolding: {workshop_result}")
        
        print("4️⃣ Scaffolding AIP Studio agent...")
        aip_result = continue_service.scaffold_foundry_component(
            "AIP Studio agent",
            "RaiderBot with quarterback decision-making and workbook visualization tools"
        )
        print(f"AIP scaffolding: {aip_result}")
        
        print("5️⃣ Updating Continue.dev configuration...")
        config_result = continue_service.update_continue_config([{
            "name": "raiderbot_deployment",
            "description": "Deploy consolidated RaiderBot system",
            "prompt": "Deploy RaiderBot with Workshop app, AIP agent, and quarterback functions to Foundry"
        }])
        print(f"Config update: {config_result}")
        
        print("6️⃣ Initializing unified system...")
        unified_system = UnifiedRaiderBotSystem()
        initialized = await unified_system.initialize_system()
        
        if initialized:
            print("✅ Continue.dev deployment successful!")
            print("🌐 Access RaiderBot through VS Studio Continue.dev extensions")
            print("🎯 Use custom commands: foundry_scaffold, aip_tool, orchestrator_agent")
            return 0
        else:
            print("❌ Unified system initialization failed")
            return 1
            
    except Exception as e:
        print(f"❌ Continue.dev deployment failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(deploy_via_continue())
    exit(exit_code)
