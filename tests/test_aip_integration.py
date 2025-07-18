#!/usr/bin/env python3
"""
Test AIP Studio integration functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.foundry.automation_engine import RaiderBotAutomationEngine, BuildRequest
from src.aip.bot_integration_service import BotIntegrationService

async def test_aip_integration():
    """Test AIP Studio integration with workbook instructions"""
    
    print("🧪 Testing RaiderBot AIP Studio integration...")
    
    config = {"FOUNDRY_URL": "https://test.palantirfoundry.com"}
    engine = RaiderBotAutomationEngine(config)
    bot_integration = BotIntegrationService(engine)
    
    test_commands = [
        "delivery_performance",
        "driver_performance", 
        "safety_metrics"
    ]
    
    for command in test_commands:
        print(f"\n📊 Testing {command} command...")
        result = await bot_integration.process_bot_command(command, "test_user")
        
        if result["success"]:
            print(f"✅ {command}: {result['bot_response']}")
        else:
            print(f"❌ {command}: {result.get('error', 'Unknown error')}")
    
    print(f"\n🏗️ Testing general build request...")
    build_request = BuildRequest(
        id="test_build",
        user_id="test_user",
        natural_language_request="Build me a fuel cost dashboard with charts"
    )
    
    result = await engine.process_build_request(build_request)
    if result["success"]:
        print("✅ General build request successful")
    else:
        print(f"❌ General build request failed: {result.get('errors', [])}")
    
    print("\n🦸‍♂️ AIP Studio integration test complete! Woof!")

if __name__ == "__main__":
    asyncio.run(test_aip_integration())
