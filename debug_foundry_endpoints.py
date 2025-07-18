"""
Debug script for Foundry API endpoints using Continue.dev patterns
This script will help identify correct API endpoints and request formats
"""
import asyncio
import os
import json
from dotenv import load_dotenv
from src.foundry_sdk import FoundryClient

async def debug_foundry_endpoints():
    """Debug Foundry API endpoints to identify correct patterns"""
    load_dotenv()
    
    print("🔍 Debugging Foundry API endpoints...")
    print("📋 Using Continue.dev @continue.debug patterns for Foundry APIs")
    
    client = FoundryClient()
    
    endpoints_to_test = [
        "/api/v1/workbooks",
        "/api/v2/workbooks", 
        "/workshop/api/workbooks",
        "/api/v1/applications",
        "/api/v2/applications",
        "/workshop/api/applications",
        "/api/v1/dashboards",
        "/api/v2/dashboards",
        "/workshop/api/dashboards"
    ]
    
    print(f"\n🌐 Testing endpoints against: {client.foundry_url}")
    
    import httpx
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        for endpoint in endpoints_to_test:
            try:
                url = f"{client.foundry_url}{endpoint}"
                response = await http_client.get(url, headers=client.headers)
                
                status_emoji = "✅" if response.status_code < 400 else "❌"
                print(f"{status_emoji} {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   📄 Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                    except:
                        print(f"   📄 Response length: {len(response.text)} chars")
                        
            except Exception as e:
                print(f"❌ {endpoint}: Error - {str(e)[:50]}...")
    
    print(f"\n🎨 Testing workbook-specific operations...")
    
    workbook_patterns = [
        "/api/v1/workbooks/test_workbook/visualizations",
        "/api/v1/workbooks/test_workbook/charts", 
        "/api/v1/workbooks/test_workbook/widgets",
        "/workshop/api/workbooks/test_workbook/visualizations",
        "/workshop/api/workbooks/test_workbook/update"
    ]
    
    test_viz_config = {
        "type": "chart",
        "chart_type": "bar",
        "title": "Test Chart"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        for pattern in workbook_patterns:
            try:
                url = f"{client.foundry_url}{pattern}"
                response = await http_client.post(url, headers=client.headers, json=test_viz_config)
                
                status_emoji = "✅" if response.status_code < 400 else "❌"
                print(f"{status_emoji} POST {pattern}: {response.status_code}")
                
                if response.status_code not in [404, 405]:
                    print(f"   📄 Response: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"❌ POST {pattern}: Error - {str(e)[:50]}...")
    
    print(f"\n🦸‍♂️ Foundry endpoint debugging complete!")
    print(f"💡 Use Continue.dev @continue.ask to scaffold correct API patterns")
    print(f"💡 Use Continue.dev @continue.docsearch for Foundry API documentation")

if __name__ == "__main__":
    asyncio.run(debug_foundry_endpoints())
