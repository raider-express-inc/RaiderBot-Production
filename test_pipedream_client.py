#!/usr/bin/env python3

import asyncio
import sys

sys.path.append("/home/ubuntu/repos/RaiderBot-Production")

from mcp.pipedream_client import PipedreamClient


async def test_pipedream_client():
    """Test Pipedream client connectivity"""
    try:
        client = PipedreamClient()
        result = await client.get_me()
        print("✅ Pipedream client test passed")
        print(f"User: {result.get('username', 'N/A')}")
        print(f"ID: {result.get('id', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Pipedream client test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_pipedream_client())
    sys.exit(0 if success else 1)
