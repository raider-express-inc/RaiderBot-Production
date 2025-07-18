"""
Test server integration with real Foundry SDK
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import build_this_out

async def test_server_integration():
    """Test the build_this_out function with real Foundry credentials"""
    print("🚀 Testing server integration with real Foundry SDK...")
    
    try:
        result = build_this_out(
            "Build me a delivery performance dashboard with safety metrics", 
            "test_user_integration"
        )
        
        print(f"✅ Server integration successful!")
        print(f"📊 Result: {result}")
        
        if result.get("status") == "success":
            print(f"🎯 Dashboard URL: {result.get('dashboard_url', 'Not provided')}")
            print(f"📈 Workbook ID: {result.get('workbook_id', 'Not provided')}")
        
    except Exception as e:
        print(f"❌ Server integration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server_integration())
