#!/usr/bin/env python3
"""
Enhanced Snowflake client with Cortex Analyst integration
Based on Cursor directory MCP standardized connectivity approach
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.connector.errors import DatabaseError, ProgrammingError

load_dotenv()

logger = logging.getLogger(__name__)

class SnowflakeConnection:
    """Standardized Snowflake connection following Cursor directory pattern"""
    
    def __init__(self):
        """Initialize following Cursor directory MCP pattern"""
        access_token = os.getenv("SNOWFLAKE_ACCESS_TOKEN")
        password = os.getenv("SNOWFLAKE_PASSWORD")
        
        if access_token:
            self.config = {
                "user": os.getenv("SNOWFLAKE_USER"),
                "password": access_token,
                "account": os.getenv("SNOWFLAKE_ACCOUNT"),
                "database": os.getenv("SNOWFLAKE_DATABASE"),
                "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
                "schema": os.getenv("SNOWFLAKE_SCHEMA")
            }
            logger.info("Using JWT token as password authentication")
        else:
            self.config = {
                "user": os.getenv("SNOWFLAKE_USER"),
                "password": password,
                "account": os.getenv("SNOWFLAKE_ACCOUNT"),
                "database": os.getenv("SNOWFLAKE_DATABASE"),
                "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
                "schema": os.getenv("SNOWFLAKE_SCHEMA")
            }
            logger.info("Using password authentication")
            
        self.connection = None
        self.cortex_enabled = True
        safe_config = {k:v for k,v in self.config.items() if k not in ['password', 'token']}
        logger.info(f"Initialized with config: {json.dumps(safe_config)}")
        
    def ensure_connection(self):
        """Ensure connection following Cursor directory MCP pattern"""
        try:
            if self.connection is None:
                logger.info("Creating new Snowflake connection...")
                clean_config = {k: v for k, v in self.config.items() if v is not None}
                self.connection = snowflake.connector.connect(
                    **clean_config,
                    client_session_keep_alive=True,
                    network_timeout=15,
                    login_timeout=15
                )
                self.connection.cursor().execute("ALTER SESSION SET TIMEZONE = 'UTC'")
                logger.info("✅ New connection established and configured")
                self._test_cortex_availability()
            
            try:
                self.connection.cursor().execute("SELECT 1")
            except:
                logger.info("Connection lost, reconnecting...")
                self.connection = None
                return self.ensure_connection()
                
            return self.connection
        except Exception as e:
            logger.error(f"❌ Snowflake connection failed: {e}")
            raise
    
    def connect(self) -> bool:
        """Establish connection with enhanced error handling"""
        try:
            self.ensure_connection()
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False
    
    def _test_cortex_availability(self):
        """Test if Cortex Analyst is available in this account"""
        try:
            test_query = "SELECT SYSTEM$GET_CORTEX_ANALYST_STATUS() as cortex_status"
            cursor = self.connection.cursor()
            cursor.execute(test_query)
            result = cursor.fetchone()
            cursor.close()
            
            if result and result[0]:
                logger.info("✅ Cortex Analyst is available")
                self.cortex_enabled = True
            else:
                logger.warning("⚠️ Cortex Analyst not available, using standard SQL")
                self.cortex_enabled = False
                
        except Exception as e:
            logger.warning(f"⚠️ Could not verify Cortex status: {e}")
            self.cortex_enabled = False
    
    def natural_language_query(self, question: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Enhanced natural language to SQL using Cortex Analyst"""
        try:
            conn = self.ensure_connection()
            
            if self.cortex_enabled:
                cortex_query = f"""
                SELECT CORTEX_ANALYST(
                    '{question}',
                    OBJECT_CONSTRUCT(
                        'database', '{self.config.get("database", "RAIDER_DB")}',
                        'context', '{json.dumps(context or {})}'
                    )
                ) as analysis_result
                """
                
                cursor = conn.cursor(DictCursor)
                cursor.execute(cortex_query)
                result = cursor.fetchone()
                cursor.close()
                
                if result and result['ANALYSIS_RESULT']:
                    analysis = json.loads(result['ANALYSIS_RESULT'])
                    
                    if 'sql' in analysis:
                        sql_result = self.execute_query(analysis['sql'])
                        analysis['data'] = sql_result
                    
                    return {
                        'success': True,
                        'method': 'cortex_analyst',
                        'question': question,
                        'analysis': analysis,
                        'cortex_enabled': True
                    }
            
            return self._fallback_semantic_query(question, context)
            
        except Exception as e:
            logger.error(f"❌ Natural language query failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'method': 'cortex_analyst' if self.cortex_enabled else 'fallback',
                'cortex_enabled': self.cortex_enabled
            }
    
    def _fallback_semantic_query(self, question: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Fallback semantic layer for when Cortex is not available"""
        question_lower = question.lower()
        schema = self.config.get("schema", "SQL_SERVER_DBO")
        
        if 'order' in question_lower or 'delivery' in question_lower:
            sql = f"""
            SELECT TOP 10 
                ID as order_id, CUSTOMER_ID, STATUS, ORDERED_DATE
            FROM {schema}.ORDERS 
            ORDER BY ORDERED_DATE DESC
            """
        elif 'revenue' in question_lower or 'sales' in question_lower:
            sql = f"""
            SELECT 
                DATE_TRUNC('month', ORDERED_DATE) as month,
                SUM(TOTAL_CHARGE) as revenue
            FROM {schema}.ORDERS 
            WHERE ORDERED_DATE >= DATEADD('month', -6, CURRENT_DATE())
            GROUP BY month
            ORDER BY month
            """
        elif 'customer' in question_lower:
            sql = f"""
            SELECT TOP 10
                CUSTOMER_ID, COUNT(*) as order_count, SUM(TOTAL_CHARGE) as total_spent
            FROM {schema}.ORDERS
            GROUP BY CUSTOMER_ID
            ORDER BY total_spent DESC
            """
        else:
            sql = "SELECT 'Query not recognized' as message"
        
        try:
            data = self.execute_query(sql)
            return {
                'success': True,
                'method': 'fallback_semantic',
                'question': question,
                'sql': sql,
                'data': data,
                'cortex_enabled': False
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'fallback_semantic',
                'cortex_enabled': False
            }
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query with enhanced error handling"""
        try:
            conn = self.ensure_connection()
            cursor = conn.cursor(DictCursor)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            logger.info(f"✅ Query executed successfully: {len(results)} rows")
            return results
            
        except DatabaseError as e:
            logger.error(f"❌ Database error: {e}")
            raise
        except ProgrammingError as e:
            logger.error(f"❌ SQL programming error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            if "connection" in str(e).lower() or "session" in str(e).lower():
                logger.info("🔄 Attempting to reconnect...")
                self.connection = None
                return self.execute_query(query)
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Enhanced health check with Cortex status"""
        try:
            conn = self.ensure_connection()
            test_result = self.execute_query("SELECT CURRENT_TIMESTAMP() as current_time")
            
            cortex_status = "unknown"
            if self.cortex_enabled:
                try:
                    cortex_test = self.natural_language_query("What is the current time?")
                    cortex_status = "available" if cortex_test['success'] else "error"
                except:
                    cortex_status = "unavailable"
            
            return {
                'status': 'healthy',
                'connection': True,
                'cortex_enabled': self.cortex_enabled,
                'cortex_status': cortex_status,
                'timestamp': test_result[0]['CURRENT_TIME'] if test_result else None,
                'account': self.config.get('account'),
                'database': self.config.get('database'),
                'warehouse': self.config.get('warehouse'),
                'schema': self.config.get('schema')
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'connection': False,
                'cortex_enabled': False,
                'error': str(e)
            }
    
    def close(self):
        """Close connection properly"""
        if self.connection:
            try:
                self.connection.close()
                logger.info("✅ Snowflake connection closed")
            except Exception as e:
                logger.error(f"❌ Error closing connection: {e}")
            finally:
                self.connection = None

class CortexAnalystClient(SnowflakeConnection):
    """Enhanced Snowflake client with Cortex Analyst capabilities"""
    pass

cortex_client = CortexAnalystClient()
