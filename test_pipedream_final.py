#!/usr/bin/env python3
"""Final Pipedream API verification"""
import requests
import os

def test_pipedream_api():
    api_key = "7672368099fc1d5e2c3360fc95265da4"
    
    try:
        response = requests.get(
            'https://api.pipedream.com/v1/users/me', 
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=10
        )
        
        print(f'Pipedream API Status: {response.status_code}')
        if response.status_code == 200:
            print('✅ Pipedream integration fully functional')
            return True
        else:
            print(f'❌ Pipedream API error: {response.text[:100]}')
            return False
            
    except Exception as e:
        print(f'❌ Pipedream API connection error: {e}')
        return False

if __name__ == "__main__":
    success = test_pipedream_api()
    exit(0 if success else 1)
