"""
Sema4.ai Integration Service for Native Snowflake Processing
Implements the platform specification requirement for all AI processing in Snowflake
"""

import os
import logging
from typing import Dict, List, Any, Optional
from ..snowflake.unified_connection import snowflake_client

class Sema4AIIntegrationService:
    """Service for native Sema4.ai processing in Snowflake"""
    
    def __init__(self):
        self.snowflake_client = snowflake_client
        self.sema4_enabled = self._check_sema4_availability()
        
    def _check_sema4_availability(self) -> bool:
        """Check if Sema4.ai is available in Snowflake"""
        try:
            result = self.snowflake_client.execute_query(
                "SHOW APPLICATIONS LIKE 'SEMA4_AI'"
            )
            return result["success"] and len(result["rows"]) > 0
        except Exception as e:
            logging.warning(f"Sema4.ai availability check failed: {e}")
            return False
    
    def process_multi_agent_query(self, query: str, agent_type: str = "auto") -> Dict[str, Any]:
        """Process query using multi-agent routing with Sema4.ai"""
        try:
            if agent_type == "auto":
                agent_type = self._detect_agent_type(query)
            
            if self.sema4_enabled:
                return self._process_with_sema4(query, agent_type)
            else:
                return self._process_with_fallback(query, agent_type)
                
        except Exception as e:
            logging.error(f"Multi-agent query processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_type": agent_type,
                "query": query
            }
    
    def _detect_agent_type(self, query: str) -> str:
        """Detect appropriate agent type based on query content"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['route', 'driver', 'load', 'delivery', 'optimize', 'dispatch']):
            return "operations"
        elif any(word in query_lower for word in ['track', 'shipment', 'customer', 'order', 'delivery status']):
            return "customer_service"
        elif any(word in query_lower for word in ['profit', 'cost', 'revenue', 'margin', 'pricing', 'financial']):
            return "financial"
        elif any(word in query_lower for word in ['dot', 'inspection', 'compliance', 'safety', 'maintenance', 'regulation']):
            return "compliance"
        elif any(word in query_lower for word in ['policy', 'procedure', 'guideline', 'training', 'how to']):
            return "knowledge"
        else:
            return "operations"
    
    def _process_with_sema4(self, query: str, agent_type: str) -> Dict[str, Any]:
        """Process query using native Sema4.ai in Snowflake"""
        try:
            sema4_query = f"""
            SELECT * FROM TABLE(
                SEMA4_AI.QUERY(
                    '{query}',
                    'agent_type={agent_type}',
                    'context=raider_express_logistics',
                    'data_sources={self._get_agent_data_sources(agent_type)}',
                    'business_context=long_haul_refrigerated_carrier'
                )
            )
            """
            
            result = self.snowflake_client.execute_query(sema4_query)
            
            if result["success"]:
                return {
                    "success": True,
                    "agent_type": agent_type,
                    "query": query,
                    "processing_method": "sema4_ai_native",
                    "results": result["rows"],
                    "columns": result["columns"],
                    "recommendations": self._generate_agent_recommendations(agent_type, result["rows"]),
                    "data_sources": self._get_agent_data_sources(agent_type)
                }
            else: 
                return self._process_with_fallback(query, agent_type, sema4_error=result.get("error"))
                
        except Exception as e:
            return self._process_with_fallback(query, agent_type, sema4_error=str(e))
    
    def _process_with_fallback(self, query: str, agent_type: str, sema4_error: str = None) -> Dict[str, Any]:
        """Fallback processing when Sema4.ai is not available"""
        try:
            result = self.snowflake_client.execute_sema4_query(query, agent_type)
            result["sema4_fallback"] = True
            if sema4_error:
                result["sema4_error"] = sema4_error
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "sema4_error": sema4_error,
                "agent_type": agent_type,
                "query": query
            }
    
    def _get_agent_data_sources(self, agent_type: str) -> str:
        """Get data sources for specific agent type"""
        data_sources_map = {
            "operations": "TMS,GPS_tracking,fuel_data",
            "customer_service": "order_management,tracking_systems,customer_history", 
            "financial": "accounting_systems,fuel_costs,labor_costs",
            "compliance": "DOT_records,vehicle_maintenance,driver_logs",
            "knowledge": "document_repository,past_decisions,training_materials"
        }
        return data_sources_map.get(agent_type, "TMS,order_management")
    
    def _generate_agent_recommendations(self, agent_type: str, results: List) -> List[str]:
        """Generate agent-specific recommendations based on results"""
        recommendations_map = {
            "operations": [
                "Optimize route efficiency",
                "Monitor driver availability", 
                "Track fuel consumption",
                "Update delivery schedules"
            ],
            "customer_service": [
                "Proactive customer communication",
                "Track delivery performance",
                "Monitor service quality",
                "Address customer concerns"
            ],
            "financial": [
                "Analyze profit margins",
                "Monitor cost trends",
                "Optimize pricing strategy",
                "Review financial performance"
            ],
            "compliance": [
                "Ensure DOT compliance",
                "Schedule maintenance",
                "Monitor safety metrics",
                "Update regulatory records"
            ],
            "knowledge": [
                "Update policy documentation",
                "Provide training guidance",
                "Share best practices",
                "Document decisions"
            ]
        }
        
        base_recommendations = recommendations_map.get(agent_type, ["Review results", "Take appropriate action"])
        
        if results and len(results) > 10:
            base_recommendations.append("High volume detected - consider automation")
        
        return base_recommendations

sema4_integration = Sema4AIIntegrationService()
