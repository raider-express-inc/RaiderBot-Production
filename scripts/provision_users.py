#!/usr/bin/env python3
"""
User provisioning script for RaiderBot AIP Studio integration
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.foundry.automation_engine import RaiderBotAutomationEngine
from src.foundry.workbook_instruction_service import WorkbookInstructionService

async def provision_user_dashboards():
    """Provision connected dashboards for all users"""
    
    users = [
        {"user_id": "dispatch_001", "role": "dispatch", "name": "Maria Rodriguez"},
        {"user_id": "fleet_001", "role": "fleet", "name": "John Smith"},
        {"user_id": "cs_001", "role": "customer_service", "name": "Sarah Johnson"},
        {"user_id": "mgmt_001", "role": "management", "name": "Dan Eggleton"},
        {"user_id": "safety_001", "role": "safety", "name": "Mike Wilson"}
    ]
    
    config = {
        "FOUNDRY_URL": os.getenv('FOUNDRY_URL', 'https://raiderexpress.palantirfoundry.com'),
        "FOUNDRY_CLIENT_ID": os.getenv('FOUNDRY_CLIENT_ID'),
        "FOUNDRY_CLIENT_SECRET": os.getenv('FOUNDRY_CLIENT_SECRET'),
        "FOUNDRY_AUTH_TOKEN": os.getenv('FOUNDRY_AUTH_TOKEN')
    }
    
    engine = RaiderBotAutomationEngine(config)
    workbook_service = WorkbookInstructionService(engine.foundry_client)
    
    print("🦸‍♂️ Starting RaiderBot user dashboard provisioning...")
    
    for user in users:
        try:
            print(f"📊 Provisioning dashboard for {user['name']} ({user['role']})...")
            
            result = await workbook_service.provision_user_dashboard(
                user_id=user['user_id'],
                user_role=user['role'],
                template="raiderbot_integrated"
            )
            
            if result['success']:
                print(f"✅ Dashboard provisioned: {result['dashboard']['url']}")
            else:
                print(f"❌ Failed to provision dashboard: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error provisioning {user['name']}: {e}")
    
    print("🐕 User provisioning complete! Woof!")

if __name__ == "__main__":
    asyncio.run(provision_user_dashboards())
