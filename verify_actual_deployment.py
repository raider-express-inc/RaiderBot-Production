#!/usr/bin/env python3
"""
Verify actual deployment status of RaiderBot components
This script tests real accessibility and functionality vs deployment script claims
"""

import os
import sys
import json
import asyncio
import requests
from datetime import datetime

sys.path.append(os.path.dirname(__file__))


async def verify_actual_deployment_status():
    """Verify what is actually deployed and accessible vs claimed"""
    print("🔍 Verifying Actual RaiderBot Deployment Status")
    print("=" * 60)

    verification_results = {
        "verification_timestamp": datetime.now().isoformat(),
        "components_tested": [],
        "actual_deployment_status": "UNKNOWN",
        "discrepancies_found": [],
        "working_components": [],
        "non_working_components": [],
    }

    try:
        print("1️⃣ Testing Foundry Workshop Dashboard accessibility...")
        foundry_url = "https://raiderexpress.palantirfoundry.com/workspace/workshop/raiderbot-dashboard"

        try:
            response = requests.get(foundry_url, timeout=10)
            if response.status_code == 200:
                dashboard_status = "ACCESSIBLE"
                print(f"✅ Foundry Workshop URL accessible: {response.status_code}")
            else:
                dashboard_status = "NOT_ACCESSIBLE"
                print(f"❌ Foundry Workshop URL failed: {response.status_code}")
                verification_results["discrepancies_found"].append(
                    f"Workshop dashboard URL returns {response.status_code}"
                )
        except Exception as e:
            dashboard_status = "CONNECTION_FAILED"
            print(f"❌ Foundry Workshop URL connection failed: {str(e)}")
            verification_results["discrepancies_found"].append(
                f"Workshop dashboard connection failed: {str(e)}"
            )

        verification_results["components_tested"].append(
            {
                "component": "foundry_workshop_dashboard",
                "claimed_status": "deployed",
                "actual_status": dashboard_status,
                "url": foundry_url,
            }
        )

        print("\n2️⃣ Testing quarterback functions locally...")
        try:
            from src.foundry.quarterback_functions import process_user_query

            test_query = "emergency truck breakdown on I-35"
            qb_result = process_user_query(test_query)

            if qb_result and "intent" in qb_result:
                qb_status = "WORKING_LOCALLY"
                print(
                    f"✅ Quarterback functions working locally: {qb_result['intent']}"
                )
            else:
                qb_status = "NOT_WORKING"
                print("❌ Quarterback functions failed locally")
                verification_results["discrepancies_found"].append(
                    "Quarterback functions not working locally"
                )

        except Exception as e:
            qb_status = "IMPORT_FAILED"
            print(f"❌ Quarterback functions import failed: {str(e)}")
            verification_results["discrepancies_found"].append(
                f"Quarterback functions import failed: {str(e)}"
            )

        verification_results["components_tested"].append(
            {
                "component": "quarterback_functions",
                "claimed_status": "deployed",
                "actual_status": qb_status,
                "location": "src/foundry/quarterback_functions.py",
            }
        )

        print("\n3️⃣ Testing unified system service...")
        try:
            from src.consolidation.unified_system_service import UnifiedRaiderBotSystem

            unified_system = UnifiedRaiderBotSystem()
            initialized = await unified_system.initialize_system()

            if initialized:
                unified_status = "WORKING_LOCALLY"
                print("✅ Unified system service working locally")
            else:
                unified_status = "INITIALIZATION_FAILED"
                print("❌ Unified system service initialization failed")
                verification_results["discrepancies_found"].append(
                    "Unified system service initialization failed"
                )

        except Exception as e:
            unified_status = "IMPORT_FAILED"
            print(f"❌ Unified system service import failed: {str(e)}")
            verification_results["discrepancies_found"].append(
                f"Unified system service import failed: {str(e)}"
            )

        verification_results["components_tested"].append(
            {
                "component": "unified_system_service",
                "claimed_status": "deployed",
                "actual_status": unified_status,
                "location": "src/consolidation/unified_system_service.py",
            }
        )

        print("\n4️⃣ Testing AIP Studio integration...")
        try:
            from src.aip.agent_config import AIP_AGENT_CONFIG

            if AIP_AGENT_CONFIG and "name" in AIP_AGENT_CONFIG:
                aip_status = "CONFIG_AVAILABLE"
                print(f"✅ AIP Studio config available: {AIP_AGENT_CONFIG['name']}")
            else:
                aip_status = "CONFIG_MISSING"
                print("❌ AIP Studio config missing or invalid")
                verification_results["discrepancies_found"].append(
                    "AIP Studio config missing or invalid"
                )

        except Exception as e:
            aip_status = "IMPORT_FAILED"
            print(f"❌ AIP Studio integration import failed: {str(e)}")
            verification_results["discrepancies_found"].append(
                f"AIP Studio integration import failed: {str(e)}"
            )

        verification_results["components_tested"].append(
            {
                "component": "aip_studio_integration",
                "claimed_status": "deployed",
                "actual_status": aip_status,
                "location": "src/aip/",
            }
        )

        print("\n5️⃣ Checking actual Foundry deployment vs local functionality...")

        foundry_deployed_count = 0
        locally_working_count = 0

        for component in verification_results["components_tested"]:
            if component["actual_status"] in ["ACCESSIBLE", "DEPLOYED_TO_FOUNDRY"]:
                foundry_deployed_count += 1
                verification_results["working_components"].append(
                    component["component"]
                )
            elif component["actual_status"] in ["WORKING_LOCALLY", "CONFIG_AVAILABLE"]:
                locally_working_count += 1
            else:
                verification_results["non_working_components"].append(
                    component["component"]
                )

        if foundry_deployed_count >= 3:
            verification_results["actual_deployment_status"] = "PRODUCTION_DEPLOYED"
        elif locally_working_count >= 3:
            verification_results["actual_deployment_status"] = "LOCAL_ONLY"
        else:
            verification_results["actual_deployment_status"] = "INCOMPLETE"

        print("\n📊 Verification Summary:")
        print(f"   Foundry Deployed: {foundry_deployed_count}/4 components")
        print(f"   Working Locally: {locally_working_count}/4 components")
        print(f"   Overall Status: {verification_results['actual_deployment_status']}")

        if verification_results["discrepancies_found"]:
            print("\n⚠️  Discrepancies Found:")
            for discrepancy in verification_results["discrepancies_found"]:
                print(f"   • {discrepancy}")

        with open("actual_deployment_verification.json", "w") as f:
            json.dump(verification_results, f, indent=2)

        print("\n📄 Verification results saved to actual_deployment_verification.json")

        return verification_results

    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        verification_results["actual_deployment_status"] = "VERIFICATION_FAILED"
        verification_results["discrepancies_found"].append(
            f"Verification script failed: {str(e)}"
        )
        return verification_results


if __name__ == "__main__":
    results = asyncio.run(verify_actual_deployment_status())

    print("\n" + "=" * 60)
    print("🎯 HONEST DEPLOYMENT ASSESSMENT")
    print("=" * 60)

    if results["actual_deployment_status"] == "LOCAL_ONLY":
        print(
            "❌ REALITY CHECK: Components work locally but are NOT deployed to Foundry"
        )
        print(
            "   Deployment scripts ran successfully, but this is NOT the same as production deployment"
        )
        print("   End users cannot access functionality through Foundry login")
    elif results["actual_deployment_status"] == "PRODUCTION_DEPLOYED":
        print("✅ Components are actually deployed and accessible through Foundry")
    else:
        print("⚠️  Deployment status is incomplete or unclear")

    exit(0 if results["actual_deployment_status"] == "PRODUCTION_DEPLOYED" else 1)
