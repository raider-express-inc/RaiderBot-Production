#!/usr/bin/env python3
"""
Test script to verify authentication token loading
"""

import os
from dotenv import load_dotenv

def test_auth_loading():
    """Test that authentication tokens are properly loaded"""
    print("🔐 Testing Authentication Token Loading...")
    print("=" * 50)
    
    load_dotenv()
    
    foundry_token = os.getenv('FOUNDRY_AUTH_TOKEN')
    foundry_url = os.getenv('FOUNDRY_URL', 'https://raiderexpress.palantirfoundry.com')
    client_id = os.getenv('FOUNDRY_CLIENT_ID')
    agent_rid = os.getenv('AIP_AGENT_RID', 'ri.aip-agents..agent.e6e9ff2f-0952-4774-98b5-4388a96ddbf1')
    
    print(f"🌐 Foundry URL: {foundry_url}")
    print(f"🎯 Agent RID: {agent_rid}")
    print(f"🔑 Client ID: {'Configured' if client_id else 'Missing'}")
    print(f"🔐 Auth Token: {'Configured' if foundry_token else 'Missing'}")
    
    if foundry_token:
        print(f"   Token Length: {len(foundry_token)} characters")
        print(f"   Token Format: {'JWT' if foundry_token.startswith('eyJ') else 'Invalid'}")
        print(f"   Token Preview: {foundry_token[:50]}...")
    else:
        print("   ❌ No auth token found in environment")
    
    return {
        "foundry_url": foundry_url,
        "agent_rid": agent_rid,
        "client_id": client_id,
        "foundry_token": foundry_token,
        "token_configured": bool(foundry_token),
        "token_valid_format": foundry_token and foundry_token.startswith('eyJ')
    }

if __name__ == "__main__":
    result = test_auth_loading()
    
    if result["token_configured"] and result["token_valid_format"]:
        print("\n✅ Authentication configuration is valid")
    else:
        print("\n❌ Authentication configuration has issues")
        if not result["token_configured"]:
            print("   - Missing FOUNDRY_AUTH_TOKEN")
        if not result["token_valid_format"]:
            print("   - Invalid token format (should be JWT)")
