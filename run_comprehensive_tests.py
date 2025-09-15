#!/usr/bin/env python3
"""
Run all comprehensive tests for the 8 critical checklist items
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


async def run_all_tests():
    """Run all test suites"""
    print("🚀 Running All RaiderBot Test Suites")
    print("=" * 60)

    test_results = {}

    print("\n1️⃣ Running AIP Integration Tests...")
    try:
        from tests.test_aip_integration import test_aip_integration

        result = await test_aip_integration()
        test_results["aip_integration"] = {"success": True, "result": result}
        print("✅ AIP Integration Tests: PASSED")
    except Exception as e:
        test_results["aip_integration"] = {"success": False, "error": str(e)}
        print(f"❌ AIP Integration Tests: FAILED - {e}")

    print("\n2️⃣ Running Real Foundry Integration Tests...")
    try:
        from test_real_foundry import test_real_foundry_integration

        result = await test_real_foundry_integration()
        test_results["real_foundry"] = {"success": True, "result": result}
        print("✅ Real Foundry Tests: PASSED")
    except Exception as e:
        test_results["real_foundry"] = {"success": False, "error": str(e)}
        print(f"❌ Real Foundry Tests: FAILED - {e}")

    print("\n3️⃣ Running Server Integration Tests...")
    try:
        from test_server_integration import test_server_integration

        result = await test_server_integration()
        test_results["server_integration"] = {"success": True, "result": result}
        print("✅ Server Integration Tests: PASSED")
    except Exception as e:
        test_results["server_integration"] = {"success": False, "error": str(e)}
        print(f"❌ Server Integration Tests: FAILED - {e}")

    print("\n4️⃣ Running Comprehensive Integration Tests...")
    try:
        from tests.comprehensive_integration_test import ComprehensiveIntegrationTest

        test_suite = ComprehensiveIntegrationTest()
        result = await test_suite.run_all_tests()
        test_results["comprehensive"] = {
            "success": result["overall_success"],
            "result": result,
        }
        print(
            f"✅ Comprehensive Tests: {'PASSED' if result['overall_success'] else 'FAILED'}"
        )
    except Exception as e:
        test_results["comprehensive"] = {"success": False, "error": str(e)}
        print(f"❌ Comprehensive Tests: FAILED - {e}")

    print("\n5️⃣ Running Production Deployment Verification...")
    try:
        from verify_production_deployment import verify_production_deployment

        result = await verify_production_deployment()
        test_results["production_verification"] = {"success": result, "result": result}
        print(f"✅ Production Verification: {'PASSED' if result else 'FAILED'}")
    except Exception as e:
        test_results["production_verification"] = {"success": False, "error": str(e)}
        print(f"❌ Production Verification: FAILED - {e}")

    print("\n📊 FINAL TEST SUMMARY")
    print("=" * 60)

    passed_tests = sum(1 for result in test_results.values() if result["success"])
    total_tests = len(test_results)
    success_rate = passed_tests / total_tests if total_tests > 0 else 0

    for test_name, result in test_results.items():
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if not result["success"] and "error" in result:
            print(f"    Error: {result['error']}")

    print(
        f"\n🎯 Overall Results: {passed_tests}/{total_tests} tests passed ({success_rate:.1%})"
    )

    if success_rate == 1.0:
        print("🎉 ALL TESTS PASSED! All 8 critical checklist items verified! 🦸‍♂️🐕")
        return True
    else:
        print("⚠️ Some tests failed. Review and fix before claiming completion.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
