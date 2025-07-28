from typing import Dict, Union, Optional, List
import logging
from datetime import datetime

try:
    from foundry_functions import function
except ImportError:
    def function(func):
        return func

@function
def process_user_query(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    RaiderBot Quarterback: Consolidated query processing with intelligent routing
    """
    logging.info(f"Processing quarterback query: {query}")
    
    try:
        intent = _classify_intent(query)
        confidence_score = _calculate_confidence(query, intent, context)
        
        return {
            "query": query,
            "intent": intent,
            "confidence": confidence_score,
            "quarterback_decision": True,
            "recommendations": _get_recommended_actions(intent, confidence_score),
            "requires_escalation": confidence_score < 0.75,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error processing quarterback query: {str(e)}")
        return {
            "query": query,
            "intent": "error",
            "confidence": 0.0,
            "quarterback_decision": False,
            "error": str(e)
        }

@function
def autonomous_decision_making(scenario: Dict[str, Union[str, int, float]]) -> Dict[str, Union[str, bool, float]]:
    """
    RaiderBot Quarterback: Consolidated autonomous decision making
    """
    scenario_type = scenario.get("type", "general")
    
    decision_map = {
        "route_optimization": {
            "decision": "IMPLEMENT_DYNAMIC_ROUTING",
            "confidence": 0.92,
            "actions": ["Calculate optimal path", "Update GPS systems", "Notify drivers"]
        },
        "emergency_response": {
            "decision": "ACTIVATE_EMERGENCY_PROTOCOL", 
            "confidence": 0.96,
            "actions": ["Alert dispatch", "Contact emergency services", "Reroute vehicles"]
        },
        "fleet_management": {
            "decision": "OPTIMIZE_FLEET_ALLOCATION",
            "confidence": 0.87,
            "actions": ["Check availability", "Update assignments", "Monitor performance"]
        }
    }
    
    result = decision_map.get(scenario_type, {
        "decision": "Proceed with standard protocol",
        "confidence": 0.75,
        "actions": ["Standard processing"]
    })
    
    return {
        "scenario": scenario,
        "decision": result["decision"],
        "autonomous": True,
        "confidence": result["confidence"],
        "actions_taken": result["actions"],
        "timestamp": datetime.now().isoformat()
    }

def _classify_intent(query: str) -> str:
    """Classify query intent"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['emergency', 'urgent', 'critical']):
        return 'emergency_response'
    elif any(word in query_lower for word in ['route', 'optimize', 'path']):
        return 'route_optimization'
    elif any(word in query_lower for word in ['fleet', 'vehicle', 'truck']):
        return 'fleet_management'
    else:
        return 'general_inquiry'

def _calculate_confidence(query: str, intent: str, context: Optional[Dict] = None) -> float:
    """Calculate confidence score"""
    base_confidence = 0.7
    
    if context and 'historical_data' in context:
        base_confidence += 0.1
    if len(query.split()) > 10:
        base_confidence += 0.05
    if intent == 'emergency_response':
        base_confidence += 0.1
        
    return min(base_confidence, 1.0)

def _get_recommended_actions(intent: str, confidence: float) -> List[str]:
    """Get recommended actions based on intent"""
    actions_map = {
        'emergency_response': ['Notify dispatch', 'Contact emergency services', 'Update fleet status'],
        'route_optimization': ['Analyze traffic patterns', 'Calculate fuel efficiency', 'Update routes'],
        'fleet_management': ['Check vehicle status', 'Review assignments', 'Monitor metrics'],
        'general_inquiry': ['Clarify intent', 'Gather context', 'Route to specialist']
    }
    
    base_actions = actions_map.get(intent, actions_map['general_inquiry'])
    
    if confidence < 0.7:
        base_actions.append('Request human review')
        
    return base_actions
