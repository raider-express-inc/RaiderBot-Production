from typing import Dict, Union, Optional, List
import logging
from datetime import datetime

try:
    from foundry_functions import function
except ImportError:
    def function(func):
        return func

@function
def operations_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    Operations Agent: Load planning, driver assignments, route optimization
    Data Sources: TMS, GPS tracking, fuel data
    """
    logging.info(f"Operations Agent processing: {query}")
    
    try:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['route', 'optimize', 'path', 'delivery']):
            return {
                "agent_type": "operations",
                "query": query,
                "intent": "route_optimization",
                "confidence": 0.95,
                "recommendations": [
                    "Analyze current traffic patterns",
                    "Consider driver availability", 
                    "Optimize for fuel efficiency",
                    "Account for delivery time windows"
                ],
                "data_sources": ["TMS", "GPS_tracking", "fuel_data"],
                "example_queries": ["Find optimal routes for this week's California runs"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in query_lower for word in ['driver', 'assignment', 'fleet']):
            return {
                "agent_type": "operations",
                "query": query,
                "intent": "driver_assignment",
                "confidence": 0.92,
                "recommendations": [
                    "Check driver availability",
                    "Review hours of service",
                    "Match driver skills to load requirements",
                    "Optimize driver utilization"
                ],
                "data_sources": ["TMS", "driver_logs", "fleet_management"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return _general_operations_response(query)
            
    except Exception as e:
        return _error_response("operations", query, str(e))

@function
def customer_service_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    Customer Service Agent: Shipment tracking, delivery updates, customer inquiries
    Data Sources: Order management, tracking systems, customer history
    """
    logging.info(f"Customer Service Agent processing: {query}")
    
    try:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['track', 'shipment', 'delivery', 'order']):
            return {
                "agent_type": "customer_service",
                "query": query,
                "intent": "shipment_tracking",
                "confidence": 0.94,
                "recommendations": [
                    "Retrieve shipment status",
                    "Check delivery timeline",
                    "Identify any delays",
                    "Prepare customer communication"
                ],
                "data_sources": ["order_management", "tracking_systems", "customer_history"],
                "example_queries": ["Where is load #12345 and when will it deliver?"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in query_lower for word in ['customer', 'complaint', 'issue']):
            return {
                "agent_type": "customer_service",
                "query": query,
                "intent": "customer_inquiry",
                "confidence": 0.89,
                "recommendations": [
                    "Review customer history",
                    "Assess inquiry severity",
                    "Prepare response strategy",
                    "Schedule follow-up"
                ],
                "data_sources": ["customer_history", "service_records"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return _general_customer_service_response(query)
            
    except Exception as e:
        return _error_response("customer_service", query, str(e))

@function
def financial_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    Financial Agent: Revenue reporting, cost analysis, pricing decisions
    Data Sources: Accounting systems, fuel costs, labor costs
    """
    logging.info(f"Financial Agent processing: {query}")
    
    try:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['profit', 'margin', 'cost', 'revenue']):
            return {
                "agent_type": "financial",
                "query": query,
                "intent": "financial_analysis",
                "confidence": 0.93,
                "recommendations": [
                    "Analyze profit margins by lane",
                    "Review cost components",
                    "Compare against benchmarks",
                    "Identify optimization opportunities"
                ],
                "data_sources": ["accounting_systems", "fuel_costs", "labor_costs"],
                "example_queries": ["What's our profit margin on Texas to Florida lanes?"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in query_lower for word in ['pricing', 'rate', 'quote']):
            return {
                "agent_type": "financial",
                "query": query,
                "intent": "pricing_decision",
                "confidence": 0.91,
                "recommendations": [
                    "Calculate cost basis",
                    "Review market rates",
                    "Consider competitive factors",
                    "Optimize pricing strategy"
                ],
                "data_sources": ["market_data", "cost_analysis", "competitive_intelligence"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return _general_financial_response(query)
            
    except Exception as e:
        return _error_response("financial", query, str(e))

@function
def compliance_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    Compliance Agent: DOT regulations, safety compliance, maintenance schedules
    Data Sources: DOT records, vehicle maintenance, driver logs
    """
    logging.info(f"Compliance Agent processing: {query}")
    
    try:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['dot', 'inspection', 'maintenance', 'safety']):
            return {
                "agent_type": "compliance",
                "query": query,
                "intent": "compliance_check",
                "confidence": 0.96,
                "recommendations": [
                    "Review DOT compliance status",
                    "Check inspection schedules",
                    "Verify driver qualifications",
                    "Update maintenance records"
                ],
                "data_sources": ["DOT_records", "vehicle_maintenance", "driver_logs"],
                "example_queries": ["Which trucks need inspection this month?"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in query_lower for word in ['hours', 'service', 'log', 'violation']):
            return {
                "agent_type": "compliance",
                "query": query,
                "intent": "hours_of_service",
                "confidence": 0.94,
                "recommendations": [
                    "Check driver hours status",
                    "Identify potential violations",
                    "Plan rest periods",
                    "Ensure compliance"
                ],
                "data_sources": ["driver_logs", "ELD_data", "DOT_regulations"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return _general_compliance_response(query)
            
    except Exception as e:
        return _error_response("compliance", query, str(e))

@function
def knowledge_agent(query: str, context: Optional[Dict] = None) -> Dict[str, Union[str, bool, float, List[str]]]:
    """
    Knowledge Agent: Company policies, procedures, historical decisions
    Data Sources: Document repository, past decisions, training materials
    """
    logging.info(f"Knowledge Agent processing: {query}")
    
    try:
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['policy', 'procedure', 'guideline']):
            return {
                "agent_type": "knowledge",
                "query": query,
                "intent": "policy_lookup",
                "confidence": 0.92,
                "recommendations": [
                    "Search policy database",
                    "Retrieve relevant procedures",
                    "Check for recent updates",
                    "Provide implementation guidance"
                ],
                "data_sources": ["document_repository", "policy_database", "training_materials"],
                "example_queries": ["What's our policy for temperature deviations on produce loads?"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in query_lower for word in ['training', 'procedure', 'how to']):
            return {
                "agent_type": "knowledge",
                "query": query,
                "intent": "training_guidance",
                "confidence": 0.89,
                "recommendations": [
                    "Locate training materials",
                    "Provide step-by-step guidance",
                    "Reference best practices",
                    "Schedule additional training if needed"
                ],
                "data_sources": ["training_materials", "best_practices", "historical_decisions"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return _general_knowledge_response(query)
            
    except Exception as e:
        return _error_response("knowledge", query, str(e))

def _general_operations_response(query: str) -> Dict:
    return {
        "agent_type": "operations",
        "query": query,
        "intent": "general_operations",
        "confidence": 0.75,
        "recommendations": ["Clarify operational requirements", "Specify load or route details"],
        "data_sources": ["TMS", "GPS_tracking", "fuel_data"],
        "timestamp": datetime.now().isoformat()
    }

def _general_customer_service_response(query: str) -> Dict:
    return {
        "agent_type": "customer_service", 
        "query": query,
        "intent": "general_customer_service",
        "confidence": 0.75,
        "recommendations": ["Gather customer details", "Specify service request"],
        "data_sources": ["order_management", "customer_history"],
        "timestamp": datetime.now().isoformat()
    }

def _general_financial_response(query: str) -> Dict:
    return {
        "agent_type": "financial",
        "query": query,
        "intent": "general_financial",
        "confidence": 0.75,
        "recommendations": ["Specify financial metric", "Define analysis timeframe"],
        "data_sources": ["accounting_systems", "cost_data"],
        "timestamp": datetime.now().isoformat()
    }

def _general_compliance_response(query: str) -> Dict:
    return {
        "agent_type": "compliance",
        "query": query,
        "intent": "general_compliance",
        "confidence": 0.75,
        "recommendations": ["Specify compliance area", "Identify regulatory requirement"],
        "data_sources": ["DOT_records", "safety_data"],
        "timestamp": datetime.now().isoformat()
    }

def _general_knowledge_response(query: str) -> Dict:
    return {
        "agent_type": "knowledge",
        "query": query,
        "intent": "general_knowledge",
        "confidence": 0.75,
        "recommendations": ["Specify information needed", "Clarify policy area"],
        "data_sources": ["document_repository", "policy_database"],
        "timestamp": datetime.now().isoformat()
    }

def _error_response(agent_type: str, query: str, error: str) -> Dict:
    return {
        "agent_type": agent_type,
        "query": query,
        "intent": "error",
        "confidence": 0.0,
        "error": error,
        "recommendations": ["Review error logs", "Contact technical support"],
        "timestamp": datetime.now().isoformat()
    }
