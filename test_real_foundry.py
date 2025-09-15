"""
Test script for real Foundry SDK integration with actual credentials
"""

import asyncio
from dotenv import load_dotenv
from src.foundry_sdk import FoundryClient


async def test_real_foundry_integration():
    """Test real Foundry API calls with production credentials"""
    load_dotenv()

    print("🔧 Testing real Foundry SDK integration...")

    client = FoundryClient()

    print(f"📡 Foundry URL: {client.foundry_url}")
    print(f"🔑 Auth configured: {'Yes' if client.auth_token else 'No'}")

    print("\n📚 Testing workbook listing...")
    try:
        workbooks = await client.get_user_workbooks("test_user")
        print(f"✅ Retrieved {len(workbooks)} workbooks")
        for wb in workbooks:
            print(f"  - {wb['name']} ({wb['workbook_id']})")
    except Exception as e:
        print(f"❌ Workbook listing failed: {e}")

    print("\n📊 Testing dashboard creation...")
    try:
        dashboard_config = {
            "user_id": "test_user",
            "name": "RaiderBot Test Dashboard",
            "widgets": ["delivery_performance", "safety_metrics"],
            "theme": "german_shepherd",
        }
        result = await client.create_user_dashboard(dashboard_config)
        print(f"✅ Dashboard created: {result['dashboard_id']}")
        print(f"🔗 URL: {result['url']}")
    except Exception as e:
        print(f"❌ Dashboard creation failed: {e}")

    print("\n🎨 Testing workbook visualization update...")
    try:
        viz_config = {
            "type": "chart",
            "chart_type": "bar",
            "data_source": "delivery_performance",
            "x_axis": "date",
            "y_axis": "deliveries",
            "title": "Daily Delivery Performance",
        }
        result = await client.update_workbook_visualization(
            "workbook_test_user_main", viz_config
        )
        print(f"📊 Visualization result: {result}")
        if result.get("status") == "updated":
            print(f"✅ Visualization updated: {result['visualization_id']}")
        elif result.get("status") == "error":
            print(
                f"❌ Visualization update failed: {result.get('error', 'Unknown error')}"
            )
            raise Exception(
                f"Visualization update failed: {result.get('error', 'Unknown error')}"
            )
        else:
            print(
                f"❌ Visualization update failed: {result.get('error', 'Unknown error')}"
            )
            if "attempted_endpoints" in result:
                print(f"🔍 Attempted endpoints: {result['attempted_endpoints']}")
    except Exception as e:
        print(f"❌ Visualization update failed: {e}")

    print("\n🏗️ Testing Workshop app creation...")
    try:
        app_config = {
            "name": "RaiderBot Test App",
            "type": "dashboard",
            "user_id": "test_user",
            "widgets": ["chart", "table", "metrics"],
        }
        result = await client.create_workshop_app(app_config)
        print(f"✅ Workshop app created: {result['app_id']}")
    except Exception as e:
        print(f"❌ Workshop app creation failed: {e}")

    print("\n🦸‍♂️ Real Foundry SDK integration test complete! Woof!")


if __name__ == "__main__":
    asyncio.run(test_real_foundry_integration())
