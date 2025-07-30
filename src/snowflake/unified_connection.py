"""
Unified Snowflake Connection Utility
Consolidates all Snowflake connection patterns across the codebase
"""

import os
import snowflake.connector
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class UnifiedSnowflakeConnection:
    """Centralized Snowflake connection management"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self, database: str = "MCLEOD_DB", schema: str = "dbo"):
        """Get Snowflake connection with unified configuration"""
        if self._connection is None or self._connection.is_closed():
            password = os.getenv('SNOWFLAKE_PASSWORD')
            access_token = os.getenv('SNOWFLAKE_ACCESS_TOKEN')
            
            if password:
                self._connection = snowflake.connector.connect(
                    user=os.getenv('SNOWFLAKE_USER', 'ASH073108'),
                    password=password,
                    account=os.getenv('SNOWFLAKE_ACCOUNT', 'LI21842-WW0744'),
                    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'TABLEAU_CONNECT'),
                    database=database,
                    schema=schema,
                    client_session_keep_alive=True
                )
            elif access_token:
                self._connection = snowflake.connector.connect(
                    user=os.getenv('SNOWFLAKE_USER', 'ASH073108'),
                    authenticator='oauth',
                    token=access_token,
                    account=os.getenv('SNOWFLAKE_ACCOUNT', 'LI21842-WW0744'),
                    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'TABLEAU_CONNECT'),
                    database=database,
                    schema=schema,
                    client_session_keep_alive=True
                )
            else:
                raise ValueError("Either SNOWFLAKE_PASSWORD or SNOWFLAKE_ACCESS_TOKEN must be provided")
        return self._connection
    
    def execute_query(self, sql: str, database: str = "MCLEOD_DB", schema: str = "dbo"):
        """Execute query with unified connection"""
        conn = self.get_connection(database, schema)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return {"columns": columns, "rows": results, "success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            cursor.close()
    
    def execute_sema4_query(self, natural_language_query: str, agent_type: str = "operations"):
        """Execute natural language query using Sema4.ai native processing"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            sema4_query = f"""
            SELECT * FROM TABLE(
                SEMA4_AI.QUERY('{natural_language_query}', 
                              'agent_type={agent_type}',
                              'context=raider_express_logistics')
            )
            """
            
            cursor.execute(sema4_query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            return {
                "success": True,
                "natural_language_query": natural_language_query,
                "agent_type": agent_type,
                "columns": columns,
                "rows": results,
                "processing_method": "sema4_ai_native"
            }
            
        except Exception as e:
            return self._fallback_sql_query(natural_language_query, agent_type, str(e))
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def _fallback_sql_query(self, query: str, agent_type: str, sema4_error: str):
        """Fallback SQL query when Sema4.ai is not available"""
        try:
            if agent_type == "operations":
                sql = self._generate_operations_sql(query)
            elif agent_type == "customer_service":
                sql = self._generate_customer_service_sql(query)
            elif agent_type == "financial":
                sql = self._generate_financial_sql(query)
            elif agent_type == "compliance":
                sql = self._generate_compliance_sql(query)
            elif agent_type == "knowledge":
                sql = self._generate_knowledge_sql(query)
            else:
                sql = "SELECT 'Agent type not supported' as message"
            
            result = self.execute_query(sql)
            result["sema4_fallback"] = True
            result["sema4_error"] = sema4_error
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e), "sema4_error": sema4_error}
    
    def _generate_operations_sql(self, query: str) -> str:
        """Generate operations-specific SQL queries"""
        query_lower = query.lower()
        if 'california' in query_lower and 'route' in query_lower:
            return """
            SELECT route_name, COUNT(*) as load_count, AVG(miles) as avg_miles
            FROM orders WHERE destination_state = 'CA' 
            AND order_date >= CURRENT_DATE() - 7
            GROUP BY route_name ORDER BY load_count DESC
            """
        return "SELECT COUNT(*) as total_operations FROM orders WHERE order_date >= CURRENT_DATE() - 7"
    
    def _generate_customer_service_sql(self, query: str) -> str:
        """Generate customer service-specific SQL queries"""
        query_lower = query.lower()
        if 'track' in query_lower or 'shipment' in query_lower:
            return """
            SELECT order_id, customer_name, status, delivery_date, tracking_number
            FROM orders WHERE status IN ('IN_TRANSIT', 'DELIVERED')
            ORDER BY order_date DESC LIMIT 20
            """
        return "SELECT COUNT(*) as active_shipments FROM orders WHERE status = 'IN_TRANSIT'"
    
    def _generate_financial_sql(self, query: str) -> str:
        """Generate financial-specific SQL queries"""
        query_lower = query.lower()
        if 'profit' in query_lower or 'margin' in query_lower:
            return """
            SELECT route_name, SUM(revenue) as total_revenue, SUM(cost) as total_cost,
                   (SUM(revenue) - SUM(cost)) / SUM(revenue) * 100 as profit_margin
            FROM financial_data WHERE date >= CURRENT_DATE() - 30
            GROUP BY route_name ORDER BY profit_margin DESC
            """
        return "SELECT SUM(revenue) as total_revenue, SUM(cost) as total_cost FROM financial_data WHERE date >= CURRENT_DATE() - 30"
    
    def _generate_compliance_sql(self, query: str) -> str:
        """Generate compliance-specific SQL queries"""
        query_lower = query.lower()
        if 'inspection' in query_lower:
            return """
            SELECT unit_number, last_inspection_date, next_inspection_due
            FROM vehicle_maintenance WHERE next_inspection_due <= CURRENT_DATE() + 30
            ORDER BY next_inspection_due
            """
        return "SELECT COUNT(*) as compliance_items FROM vehicle_maintenance WHERE next_inspection_due <= CURRENT_DATE() + 30"
    
    def _generate_knowledge_sql(self, query: str) -> str:
        """Generate knowledge-specific SQL queries"""
        return """
        SELECT policy_name, policy_description, last_updated
        FROM company_policies WHERE policy_name ILIKE '%temperature%'
        ORDER BY last_updated DESC
        """
    
    def close(self):
        """Close connection"""
        if self._connection and not self._connection.is_closed():
            self._connection.close()

snowflake_client = UnifiedSnowflakeConnection()
