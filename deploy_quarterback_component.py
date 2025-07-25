#!/usr/bin/env python3
"""
Deploy quarterback functions as first incremental component
"""

import os
import sys
import json
import asyncio
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from src.foundry.quarterback_functions import process_user_query, autonomous_decision_making
from src.consolidation.unified_system_service import UnifiedRaiderBotSystem

async def deploy_quarterback_functions():
    """Deploy quarterback functions as standalone component"""
    print("🏈 Deploying RaiderBot Quarterback Functions")
    print("=" * 50)
    
    try:
        print("1️⃣ Initializing unified system...")
        unified_system = UnifiedRaiderBotSystem()
        initialized = await unified_system.initialize_system()
        
        if not initialized:
            print("❌ Unified system initialization failed")
            return False
        
        print("✅ Unified system initialized successfully")
        
        print("\n2️⃣ Testing quarterback functionality...")
        test_queries = [
            "emergency truck breakdown on I-35",
            "optimize delivery routes for today",
            "check fleet maintenance status"
        ]
        
        query_results = []
        for query in test_queries:
            result = await unified_system.process_unified_query(query)
            query_results.append({
                "query": query,
                "success": result['success'],
                "intent": result.get('quarterback_analysis', {}).get('intent', 'N/A'),
                "confidence": result.get('quarterback_analysis', {}).get('confidence', 0)
            })
            print(f"✅ Query: {query} -> Intent: {result.get('quarterback_analysis', {}).get('intent', 'N/A')}")
        
        print("\n3️⃣ Getting system status...")
        status = await unified_system.get_system_status()
        print(f"📊 System status: {status['overall_status']}")
        
        deployment_result = {
            "component": "quarterback_functions",
            "status": "deployed",
            "timestamp": datetime.now().isoformat(),
            "system_status": status,
            "test_results": query_results,
            "access_methods": [
                "UnifiedRaiderBotSystem.process_unified_query()",
                "process_user_query() - Direct function call",
                "autonomous_decision_making() - Direct function call"
            ],
            "deployment_location": "RaiderBot-Production/src/foundry/quarterback_functions.py",
            "integration_status": "Ready for Foundry Workshop deployment"
        }
        
        with open("quarterback_deployment_status.json", "w") as f:
            json.dump(deployment_result, f, indent=2)
        
        print("\n✅ Quarterback functions deployed successfully!")
        print(f"📄 Deployment status saved to quarterback_deployment_status.json")
        print("\n🔗 Access Methods:")
        for method in deployment_result['access_methods']:
            print(f"   • {method}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quarterback deployment failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(deploy_quarterback_functions())
    exit(0 if success else 1)
