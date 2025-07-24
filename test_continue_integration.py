#!/usr/bin/env python3
"""
Test Continue.dev integration for Foundry deployment
"""

import sys
import os
sys.path.append('src')

from dev_tools.continue_integration_service import ContinueIntegrationService
import asyncio

def test_continue():
    """Test Continue.dev integration"""
    service = ContinueIntegrationService()
    commands = service.get_foundry_scaffolding_commands()
    print('Continue.dev Foundry commands:')
    for cmd in commands:
        print(f'  - {cmd}')
    
    result = service.scaffold_foundry_component('Workshop application', 'RaiderBot dashboard with German Shepherd AI assistant')
    print(f'Scaffolding result: {result}')

if __name__ == "__main__":
    test_continue()
