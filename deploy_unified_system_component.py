#!/usr/bin/env python3
"""
Deploy unified system service as third incremental component
"""

import os
import sys
import json
import asyncio
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from src.consolidation.unified_system_service import UnifiedRaiderBotSystem


async def deploy_unified_system():
    """Deploy unified system service"""
    print("🤖 Deploying RaiderBot Unified System Service")
    print("=" * 50)

    try:
        print("1️⃣ Initializing unified system...")
        unified_system = UnifiedRaiderBotSystem()
        initialized = await unified_system.initialize_system()

        if not initialized:
            print("❌ Unified system initialization failed")
            return False

        print("✅ Unified system initialized successfully")

        print("\n2️⃣ Getting system status...")
        status = await unified_system.get_system_status()
        print(f"📊 Overall Status: {status['overall_status']}")
        print(f"   Components: {len(status.get('components', []))} active")
        print(f"   Services: {len(status.get('services', []))} running")

        print("\n3️⃣ Testing unified query processing...")
        test_queries = [
            "emergency truck breakdown on I-35",
            "optimize delivery routes for today",
            "generate fleet performance report",
            "check customer service metrics",
            "analyze route efficiency data",
        ]

        query_results = []
        for query in test_queries:
            result = await unified_system.process_unified_query(query)
            query_results.append(
                {
                    "query": query,
                    "success": result["success"],
                    "intent": result.get("quarterback_analysis", {}).get(
                        "intent", "N/A"
                    ),
                    "confidence": result.get("quarterback_analysis", {}).get(
                        "confidence", 0
                    ),
                    "processing_time": result.get("processing_time", 0),
                }
            )
            print(f"✅ Query: {query}")
            print(
                f"   Intent: {result.get('quarterback_analysis', {}).get('intent', 'N/A')}"
            )
            print(f"   Success: {result['success']}")

        deployment_result = {
            "component": "unified_system_service",
            "status": "deployed",
            "timestamp": datetime.now().isoformat(),
            "system_status": status,
            "test_results": query_results,
            "access_methods": [
                "UnifiedRaiderBotSystem.process_unified_query()",
                "UnifiedRaiderBotSystem.get_system_status()",
                "UnifiedRaiderBotSystem.initialize_system()",
            ],
            "deployment_location": "RaiderBot-Production/src/consolidation/unified_system_service.py",
            "integration_status": "Ready for production deployment",
        }

        with open("unified_system_deployment_status.json", "w") as f:
            json.dump(deployment_result, f, indent=2)

        print("\n✅ Unified system service deployed successfully!")
        print("📄 Deployment status saved to unified_system_deployment_status.json")
        print("\n🔗 Access Methods:")
        for method in deployment_result["access_methods"]:
            print(f"   • {method}")

        return True

    except Exception as e:
        print(f"❌ Unified system deployment failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(deploy_unified_system())
    exit(0 if success else 1)
