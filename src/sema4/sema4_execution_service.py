"""
Sema4.ai Execution Support
Natural language to SQL execution with Snowflake integration
"""

import httpx
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

class Sema4ExecutionService:
    """Service for executing natural language queries via Sema4.ai"""
    
    def __init__(self, snowflake_client=None):
        self.sema4_api_key = os.getenv("SEMA4_API_KEY")
        self.sema4_endpoint = os.getenv("SEMA4_ENDPOINT", "https://api.sema4.ai/v1")
        self.snowflake_client = snowflake_client
        
    async def execute_natural_language_query(self, query: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute natural language query via Sema4.ai"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "query": query,
                    "context": {
                        "user_id": user_context.get("user_id"),
                        "role": user_context.get("role", "user"),
                        "database": "RAIDER_EXPRESS_DW",
                        "schema": "OPERATIONS"
                    },
                    "output_format": "sql_with_explanation"
                }
                
                response = await client.post(
                    f"{self.sema4_endpoint}/query/translate",
                    headers={
                        "Authorization": f"Bearer {self.sema4_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                if response.status_code == 200:
                    sema4_result = response.json()
                    
                    sql_result = await self._execute_sql(sema4_result["sql"])
                    
                    return {
                        "original_query": query,
                        "generated_sql": sema4_result["sql"],
                        "explanation": sema4_result.get("explanation", ""),
                        "results": sql_result,
                        "status": "success",
                        "execution_time": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"Sema4.ai API error: {response.text}"
                    }
                    
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    async def _execute_sql(self, sql: str) -> Dict[str, Any]:
        """Execute SQL query against Snowflake"""
        if not self.snowflake_client:
            return {"error": "Snowflake client not configured"}
            
        try:
            cursor = self.snowflake_client.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            return {
                "columns": columns,
                "rows": results,
                "row_count": len(results)
            }
        except Exception as e:
            return {"error": f"SQL execution failed: {str(e)}"}
            
    async def get_schema_context(self) -> Dict[str, Any]:
        """Get database schema context for Sema4.ai"""
        try:
            if not self.snowflake_client:
                return {
                    "schema": {
                        "columns": ["table_name", "column_name", "data_type"],
                        "rows": [
                            ["DELIVERIES", "delivery_id", "VARCHAR"],
                            ["DELIVERIES", "customer_id", "VARCHAR"],
                            ["DELIVERIES", "delivery_date", "DATE"],
                            ["TRUCKS", "truck_id", "VARCHAR"],
                            ["TRUCKS", "driver_id", "VARCHAR"]
                        ],
                        "row_count": 5,
                        "note": "Mock schema - Snowflake client not configured"
                    },
                    "status": "success"
                }
            
            schema_query = """
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'OPERATIONS'
            ORDER BY table_name, ordinal_position
            """
            
            schema_result = await self._execute_sql(schema_query)
            return {
                "schema": schema_result,
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    async def create_workflow_automation(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create automated workflow using Sema4.ai"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                workflow_payload = {
                    "name": workflow_config["name"],
                    "description": workflow_config["description"],
                    "trigger": workflow_config.get("trigger", "manual"),
                    "steps": workflow_config.get("steps", []),
                    "output_destination": workflow_config.get("output_destination", "snowflake")
                }
                
                response = await client.post(
                    f"{self.sema4_endpoint}/workflows",
                    headers={
                        "Authorization": f"Bearer {self.sema4_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=workflow_payload
                )
                
                if response.status_code in [200, 201]:
                    workflow_result = response.json()
                    return {
                        "workflow_id": workflow_result.get("id"),
                        "status": "created",
                        "workflow_url": workflow_result.get("url"),
                        "creation_time": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"Workflow creation failed: {response.text}"
                    }
                    
        except Exception as e:
            return {"status": "error", "error": str(e)}
