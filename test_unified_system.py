#!/usr/bin/env python3
"""
Test unified system functionality
"""

import sys
import os
import asyncio

sys.path.append(os.path.dirname(__file__))

from src.consolidation.unified_system_service import UnifiedRaiderBotSystem


async def test_unified_system():
    """Test unified system"""
    print("🤖 Testing unified system...")

    try:
        system = UnifiedRaiderBotSystem()
        print("✅ UnifiedRaiderBotSystem created")

        initialized = await system.initialize_system()
        print(f"✅ System initialized: {initialized}")

        if initialized:
            status = await system.get_system_status()
            print(f"📊 System status: {status['overall_status']}")

            test_query = "optimize delivery routes for today"
            result = await system.process_unified_query(test_query)
            print(f"🎯 Test query result: {result['success']}")
            print(f"   Query: {test_query}")
            print(
                f"   Intent: {result.get('quarterback_analysis', {}).get('intent', 'N/A')}"
            )

        return initialized

    except Exception as e:
        print(f"❌ Unified system test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_unified_system())
    print(
        f"\n{'✅' if success else '❌'} Unified system test {'passed' if success else 'failed'}"
    )
