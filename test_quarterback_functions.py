#!/usr/bin/env python3
"""
Test quarterback functions before deployment
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.foundry.quarterback_functions import process_user_query, autonomous_decision_making

def test_quarterback_functions():
    """Test quarterback functions"""
    print("🧪 Testing quarterback functions...")
    
    test_queries = [
        "emergency truck breakdown on I-35",
        "optimize delivery routes for today", 
        "check fleet maintenance status",
        "customer complaint about late delivery",
        "generate performance report"
    ]
    
    print("\n=== Testing process_user_query ===")
    for query in test_queries:
        try:
            result = process_user_query(query)
            print(f"✅ Query: {query}")
            print(f"   Intent: {result.get('intent', 'N/A')}")
            print(f"   Decision: {result.get('quarterback_decision', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print()
        except Exception as e:
            print(f"❌ Query failed: {query} - {str(e)}")
    
    print("\n=== Testing autonomous_decision_making ===")
    test_scenarios = [
        {"type": "emergency_response", "severity": "high"},
        {"type": "route_optimization", "vehicles": 5},
        {"type": "fleet_deployment", "demand": "high"},
        {"type": "customer_service_escalation", "priority": "urgent"}
    ]
    
    for scenario in test_scenarios:
        try:
            result = autonomous_decision_making(scenario)
            print(f"✅ Scenario: {scenario['type']}")
            print(f"   Decision: {result.get('decision', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print(f"   Autonomous: {result.get('autonomous', 'N/A')}")
            print()
        except Exception as e:
            print(f"❌ Scenario failed: {scenario['type']} - {str(e)}")

if __name__ == "__main__":
    test_quarterback_functions()
