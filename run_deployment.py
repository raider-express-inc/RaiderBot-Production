#!/usr/bin/env python3
"""
Main deployment runner for consolidated RaiderBot system
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

from src.consolidation.unified_system_service import UnifiedRaiderBotSystem
from deployment.deploy import FoundryDeployer


async def main():
    """Main deployment function"""
    print("🚀 Starting consolidated RaiderBot deployment...")

    load_dotenv()

    print("1️⃣ Testing unified system...")
    unified_system = UnifiedRaiderBotSystem()

    try:
        initialized = await unified_system.initialize_system()
        if not initialized:
            print("❌ Unified system initialization failed")
            return 1

        print("✅ Unified system initialized successfully")

        print("2️⃣ Testing system status...")
        status = await unified_system.get_system_status()
        print(f"📊 System status: {status['overall_status']}")

        print("3️⃣ Running Foundry deployment...")
        deployer = FoundryDeployer()
        deployment_success = await deployer.deploy_automation()

        if deployment_success:
            print("4️⃣ Deploying unified system to Foundry...")
            unified_deployment = await unified_system.deploy_to_foundry()

            if unified_deployment["success"]:
                print("\n✅ Complete deployment successful!")
                print(f"🌐 Access RaiderBot at: {unified_deployment['foundry_url']}")
                return 0
            else:
                print(
                    f"❌ Unified system deployment failed: {unified_deployment.get('error')}"
                )
                return 1
        else:
            print("❌ Foundry deployment failed")
            return 1

    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
