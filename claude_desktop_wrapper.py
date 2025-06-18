#!/usr/bin/env python3
"""
RaiderBot Claude Desktop Wrapper - Fixed Version
Reliable wrapper to connect Claude Desktop to RaiderBot cloud server
"""

import requests
import json
import sys
import os

def main():
    try:
        # Test the cloud server connection
        response = requests.post(
            'https://raiderbot-production-production.up.railway.app/search_orders',
            json={'query': 'TMS vs TMS2 orders today'},
            timeout=10  # 10 second timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            # Simple text output for Claude Desktop
            output = json.dumps(result, indent=2)
            print(output)
        else:
            print(f"Error: HTTP {response.status_code} - {response.text}")
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out after 10 seconds")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to RaiderBot server")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
