#!/usr/bin/env python3
"""
Test deployment script to verify Foundry connectivity and deployment functionality
"""

import asyncio
import os
from dotenv import load_dotenv
from src.foundry_sdk import FoundryClient
from src.consolidation.unified_system_service import UnifiedRaiderBotSystem

async def test_foundry_connectivity():
    """Test Foundry API connectivity"""
    load_dotenv()
    
    print("🔍 Testing Foundry API connectivity...")
    
    client = FoundryClient(
        auth_token=os.getenv("FOUNDRY_AUTH_TOKEN"),
        foundry_url=os.getenv("FOUNDRY_URL"),
        client_id=os.getenv("FOUNDRY_CLIENT_ID"),
        client_secret=os.getenv("FOUNDRY_CLIENT_SECRET")
    )
    
    print(f"🌐 Foundry URL: {client.foundry_url}")
    print(f"🔑 Auth Token: {'✓ Set' if client.auth_token else '✗ Missing'}")
    
    try:
        result = await client.test_connection()
        print(f"✅ Foundry connectivity test: {'PASSED' if result else 'FAILED'}")
        return result
    except Exception as e:
        print(f"❌ Foundry connectivity test failed: {e}")
        return False

async def test_unified_system():
    """Test unified system initialization"""
    print("\n🤖 Testing Unified RaiderBot System...")
    
    system = UnifiedRaiderBotSystem()
    
    try:
        initialized = await system.initialize_system()
        print(f"✅ System initialization: {'PASSED' if initialized else 'FAILED'}")
        
        if initialized:
            status = await system.get_system_status()
            print(f"📊 System status: {status['overall_status']}")
            
            test_query = "Show me fleet management dashboard"
            result = await system.process_unified_query(test_query)
            print(f"✅ Query processing test: {'PASSED' if result['success'] else 'FAILED'}")
            
        return initialized
    except Exception as e:
        print(f"❌ Unified system test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting RaiderBot deployment tests...")
    
    connectivity_ok = await test_foundry_connectivity()
    system_ok = await test_unified_system()
    
    if connectivity_ok and system_ok:
        print("\n✅ All tests passed! Ready for deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Check configuration and connectivity.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
