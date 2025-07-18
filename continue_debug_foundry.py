"""
Continue.dev debugging script for Foundry API patterns
Using @continue.ask and @continue.debug patterns to find correct API structure
"""
import asyncio
import os
import json
from dotenv import load_dotenv
import httpx

async def continue_debug_foundry_apis():
    """
    Use Continue.dev patterns to debug Foundry API structure
    @continue.debug: Find correct Foundry Workshop API endpoints
    @continue.ask: Scaffold proper authentication patterns
    """
    load_dotenv()
    
    print("🤖 Continue.dev Foundry API Debug Session")
    print("=" * 50)
    
    token = os.getenv("FOUNDRY_TOKEN")
    base_url = os.getenv("FOUNDRY_BASE_URL", "https://raiderexpress.palantirfoundry.com")
    
    print(f"🔑 Token present: {'Yes' if token else 'No'}")
    print(f"🌐 Base URL: {base_url}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("\n🔍 Testing authentication with known endpoints...")
    
    auth_test_endpoints = [
        "/api/v1/me",
        "/api/v2/me", 
        "/api/user/me",
        "/compass/api/user",
        "/workshop/api/user"
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for endpoint in auth_test_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                response = await client.get(url, headers=headers)
                
                status_emoji = "✅" if response.status_code < 400 else "❌"
                print(f"{status_emoji} Auth test {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   📄 User info: {data.get('username', data.get('id', 'Unknown'))}")
                    except:
                        print(f"   📄 Response length: {len(response.text)} chars")
                        
            except Exception as e:
                print(f"❌ {endpoint}: Error - {str(e)[:50]}...")
    
    print(f"\n🏗️ Testing Workshop-specific patterns...")
    
    workshop_patterns = [
        "/compass/api/applications",
        "/compass/api/workspaces", 
        "/workspace/api/applications",
        "/third-party-applications/api/v1/applications",
        "/api/v2/third-party-applications"
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for pattern in workshop_patterns:
            try:
                url = f"{base_url}{pattern}"
                response = await client.get(url, headers=headers)
                
                status_emoji = "✅" if response.status_code < 400 else "❌"
                print(f"{status_emoji} Workshop {pattern}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   📄 Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                    except:
                        print(f"   📄 Response length: {len(response.text)} chars")
                elif response.status_code == 403:
                    print(f"   🔒 Forbidden - may need different permissions")
                elif response.status_code == 401:
                    print(f"   🔑 Unauthorized - authentication issue")
                        
            except Exception as e:
                print(f"❌ {pattern}: Error - {str(e)[:50]}...")
    
    print(f"\n💡 Continue.dev Recommendations:")
    print(f"   @continue.ask: Generate correct Foundry Workshop API client")
    print(f"   @continue.debug: Investigate authentication token scope")
    print(f"   @continue.docsearch: Find latest Foundry API documentation")
    print(f"   @continue.refactor: Update SDK with correct endpoint patterns")

if __name__ == "__main__":
    asyncio.run(continue_debug_foundry_apis())
