"""
Test suite for quarterback functions
Validates merged functionality from both versions
"""

import asyncio
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.foundry.quarterback_functions import process_user_query, autonomous_decision_making

class TestQuarterbackFunctions(unittest.TestCase):
    
    def test_process_user_query_route_optimization(self):
        """Test route optimization intent detection"""
        query = "optimize delivery routes for truck 4025"
        result = process_user_query(query)
        
        self.assertEqual(result["intent"], "route_optimization")
        self.assertEqual(result["quarterback_decision"], "OPTIMIZE_ROUTES")
        self.assertGreater(result["confidence"], 0.9)
        self.assertIn("recommendations", result)
        self.assertIn("next_actions", result)
        
    def test_process_user_query_emergency(self):
        """Test emergency response detection"""
        query = "urgent problem with truck breakdown"
        result = process_user_query(query)
        
        self.assertEqual(result["intent"], "emergency_response")
        self.assertEqual(result["quarterback_decision"], "ACTIVATE_EMERGENCY_PROTOCOL")
        self.assertEqual(result["risk_assessment"], "HIGH")
        self.assertFalse(result["requires_human_approval"])
        
    def test_process_user_query_general(self):
        """Test general query handling"""
        query = "what is the weather today"
        result = process_user_query(query)
        
        self.assertEqual(result["intent"], "general_inquiry")
        self.assertTrue(result["quarterback_decision"])
        self.assertIn("query", result)
        self.assertIn("analysis", result)
        
    def test_autonomous_decision_making_route_optimization(self):
        """Test autonomous decision for route optimization"""
        scenario = {"type": "route_optimization", "priority": "high"}
        result = autonomous_decision_making(scenario)
        
        self.assertEqual(result["decision"], "IMPLEMENT_DYNAMIC_ROUTING")
        self.assertTrue(result["autonomous"])
        self.assertGreater(result["confidence"], 0.9)
        self.assertIn("reasoning", result)
        self.assertIn("decision_timestamp", result)
        
    def test_autonomous_decision_making_emergency(self):
        """Test autonomous decision for emergency response"""
        scenario = {"type": "emergency_response", "severity": "critical"}
        result = autonomous_decision_making(scenario)
        
        self.assertEqual(result["decision"], "ACTIVATE_EMERGENCY_PROTOCOL")
        self.assertTrue(result["autonomous"])
        self.assertFalse(result["requires_approval"])
        self.assertIn("mitigation_strategies", result)
        
    def test_autonomous_decision_making_general(self):
        """Test autonomous decision for general scenarios"""
        scenario = {"type": "general", "data": "test"}
        result = autonomous_decision_making(scenario)
        
        self.assertEqual(result["decision"], "Proceed with standard protocol")
        self.assertTrue(result["autonomous"])
        self.assertIn("decision_timestamp", result)

if __name__ == "__main__":
    unittest.main()
