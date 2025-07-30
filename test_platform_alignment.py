#!/usr/bin/env python3
"""
Test Platform Specification Alignment
Verify 5 agent types and Sema4.ai integration
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.foundry.quarterback_functions import operations_agent, customer_service_agent, financial_agent, compliance_agent, knowledge_agent
from src.sema4.sema4_integration_service import sema4_integration
from src.snowflake.unified_connection import snowflake_client

def test_platform_alignment():
    """Test Platform Specification Alignment"""
    print('🧪 Testing Platform Specification Alignment...')
    
    agents = [
        ('operations', operations_agent, 'Find optimal routes for California runs'),
        ('customer_service', customer_service_agent, 'Where is load #12345?'),
        ('financial', financial_agent, 'What is our profit margin on Texas to Florida lanes?'),
        ('compliance', compliance_agent, 'Which trucks need inspection this month?'),
        ('knowledge', knowledge_agent, 'What is our policy for temperature deviations?')
    ]
    
    agent_results = {}
    for agent_type, agent_func, test_query in agents:
        try:
            result = agent_func(test_query)
            success = result.get('agent_type') == agent_type
            agent_results[agent_type] = success
            print(f'  {agent_type}: {'✅' if success else '❌'} {result.get('agent_type', 'ERROR')}')
        except Exception as e:
            agent_results[agent_type] = False
            print(f'  {agent_type}: ❌ ERROR - {e}')
    
    print('🔌 Testing Sema4.ai Integration...')
    try:
        sema4_available = sema4_integration._check_sema4_availability()
        print(f'  Sema4.ai Available: {'✅' if sema4_available else '⚠️'} {sema4_available}')
    except Exception as e:
        sema4_available = False
        print(f'  Sema4.ai: ❌ ERROR - {e}')
    
    print('🏔️ Testing Snowflake Connectivity...')
    try:
        result = snowflake_client.execute_query('SELECT CURRENT_TIMESTAMP() as test_time')
        snowflake_success = result.get('success', False)
        print(f'  Snowflake: {'✅' if snowflake_success else '❌'} {snowflake_success}')
    except Exception as e:
        snowflake_success = False
        print(f'  Snowflake: ❌ ERROR - {e}')
    
    print('📊 Platform Alignment Summary:')
    total_agents = len(agent_results)
    successful_agents = sum(agent_results.values())
    success_rate = (successful_agents / total_agents) * 100
    
    print(f'  Agent Success Rate: {successful_agents}/{total_agents} ({success_rate:.1f}%)')
    print(f'  Sema4.ai Integration: {'✅' if sema4_available else '⚠️'}')
    print(f'  Snowflake Connectivity: {'✅' if snowflake_success else '❌'}')
    
    overall_success = successful_agents == total_agents and snowflake_success
    print(f'  Overall Platform Status: {'✅ READY' if overall_success else '⚠️ NEEDS ATTENTION'}')
    
    return {
        "agent_results": agent_results,
        "sema4_available": sema4_available,
        "snowflake_success": snowflake_success,
        "overall_success": overall_success,
        "success_rate": success_rate
    }

if __name__ == "__main__":
    result = test_platform_alignment()
    print('✅ Platform alignment testing complete!')
    
    if result["overall_success"]:
        print('🎉 Platform is ready for deployment!')
    else:
        print('⚠️ Platform needs attention before deployment.')
