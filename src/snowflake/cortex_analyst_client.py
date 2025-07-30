#!/usr/bin/env python3
"""
Official Snowflake Python connector implementation
Following Snowflake's recommended approach for Python integration
"""

import os
import logging
import subprocess
import json
import snowflake.connector
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class SnowflakeConnection:
    """Official Snowflake Python connector implementation"""
    
    def __init__(self):
        """Initialize with official Snowflake CLI and Python connector"""
        self.connection = None
        self.cli_available = self._check_cli_availability()
        
        self.config = {
            'account': 'LI21842-WW07444',
            'user': 'ASH073108',
            'password': 'Phi1848gam!',
            'database': 'MCLEOD_DB',
            'schema': 'dbo',
            'warehouse': 'TABLEAU_CONNECT',
            'role': 'ACCOUNTADMIN',
            'client_session_keep_alive': True,
            'network_timeout': 60,
            'login_timeout': 60,
            'autocommit': True
        }
        
        logger.info("Initialized official Snowflake CLI and Python connector")
        logger.info(f"CLI available: {self.cli_available}")
    
    def _check_cli_availability(self) -> bool:
        """Check if Snowflake CLI is available"""
        try:
            result = subprocess.run(['snow', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False
    
    def execute_via_cli(self, query: str) -> Optional[Dict[str, Any]]:
        """Execute query using Snowflake CLI (recommended for terminal operations)"""
        if not self.cli_available:
            logger.warning("Snowflake CLI not available, falling back to Python connector")
            return None
            
        try:
            result = subprocess.run([
                'snow', 'sql', 
                '--query', query,
                '--format', 'json',
                '--connection', 'default'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return {
                        'success': True,
                        'data': data,
                        'method': 'snowflake_cli'
                    }
                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'data': result.stdout,
                        'method': 'snowflake_cli'
                    }
            else:
                logger.error(f"CLI query failed: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'method': 'snowflake_cli'
                }
                
        except Exception as e:
            logger.error(f"CLI execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'method': 'snowflake_cli'
            }
    
    def connect(self) -> bool:
        """Establish connection using official Snowflake Python connector"""
        try:
            logger.info("Connecting using official Snowflake Python connector...")
            self.connection = snowflake.connector.connect(**self.config)
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            
            logger.info("✅ Official Snowflake Python connector established")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False
    
    def execute_query(self, query: str) -> Optional[List[Any]]:
        """Execute query using hybrid approach: CLI first, then Python connector"""
        if self.cli_available:
            cli_result = self.execute_via_cli(query)
            if cli_result and cli_result.get('success'):
                data = cli_result.get('data', [])
                if isinstance(data, list):
                    return data
                else:
                    return [data] if data else []
        
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                cursor.close()
                return []
                
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check using official tools"""
        if self.cli_available:
            cli_result = self.execute_via_cli("SELECT CURRENT_TIMESTAMP() as test_time")
            if cli_result and cli_result.get('success'):
                return {
                    "success": True,
                    "method": "snowflake_cli",
                    "database": "MCLEOD_DB",
                    "schema": "dbo",
                    "data": cli_result.get('data')
                }
        
        try:
            if not self.connection:
                if not self.connect():
                    return {"success": False, "error": "Connection failed"}
            
            result = self.execute_query("SELECT CURRENT_TIMESTAMP() as test_time")
            if result:
                return {
                    "success": True,
                    "timestamp": result[0][0],
                    "method": "python_connector",
                    "database": self.config['database'],
                    "schema": self.config['schema']
                }
            else:
                return {"success": False, "error": "Query execution failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query using Cortex capabilities"""
        try:
            cortex_query = f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'llama3-8b',
                'Convert this natural language query to SQL for MCLEOD_DB.dbo schema: {query}'
            ) as sql_suggestion
            """
            
            result = self.execute_query(cortex_query)
            if result:
                sql_suggestion = result[0][0]
                
                data_result = self.execute_query(sql_suggestion)
                
                return {
                    "success": True,
                    "original_query": query,
                    "sql_suggestion": sql_suggestion,
                    "data": data_result
                }
            else:
                return {"success": False, "error": "Cortex query failed"}
                
        except Exception as e:
            logger.error(f"❌ Natural language query failed: {e}")
            return {"success": False, "error": str(e)}
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Connection closed")

snowflake_client = SnowflakeConnection()

CortexAnalystClient = SnowflakeConnection
