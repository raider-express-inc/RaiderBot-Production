#!/usr/bin/env python3
"""
MCP Snowflake Integration using working authentication patterns
Based on successful MCP server configurations
"""

import os
import logging
import json
import subprocess
from typing import Dict, List, Any, Optional
from ..snowflake.mcp_snowflake_client import mcp_snowflake_client

logger = logging.getLogger(__name__)

class MCPSnowflakeIntegration:
    """MCP-based Snowflake integration using working authentication patterns"""
    
    def __init__(self):
        """Initialize with MCP server configuration"""
        self.config = {
            'account': 'LI21842-WW07444',
            'user': 'ASH073108',
            'database': 'MCLEOD_DB',
            'schema': 'dbo',
            'warehouse': 'TABLEAU_CONNECT',
            'access_token': os.getenv('SNOWFLAKE_ACCESS_TOKEN'),
            'password': os.getenv('SNOWFLAKE_PASSWORD', 'Phi1848gam!')
        }
        
        logger.info("Initialized MCP Snowflake integration")
    
    def health_check_with_mcp(self) -> Dict[str, Any]:
        """Perform health check using MCP server approach"""
        try:
            env_vars = {
                'SNOWFLAKE_ACCOUNT': self.config['account'],
                'SNOWFLAKE_USER': self.config['user'],
                'SNOWFLAKE_ACCESS_TOKEN': self.config['access_token'],
                'SNOWFLAKE_WAREHOUSE': self.config['warehouse'],
                'SNOWFLAKE_DATABASE': self.config['database'],
                'SNOWFLAKE_SCHEMA': self.config['schema']
            }
            
            for key, value in env_vars.items():
                if value:
                    os.environ[key] = str(value)
            
            result = self.execute_mcp_query("SELECT 1 as health_check")
            
            if result and result.get('success'):
                return {
                    'status': 'healthy',
                    'method': 'mcp_integration',
                    'database': self.config['database'],
                    'schema': self.config['schema'],
                    'timestamp': result.get('data', [{}])[0].get('HEALTH_CHECK', 'unknown')
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': result.get('error', 'Unknown error'),
                    'method': 'mcp_integration'
                }
                
        except Exception as e:
            logger.error(f"❌ MCP health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'method': 'mcp_integration'
            }
    
    def execute_mcp_query(self, query: str) -> Dict[str, Any]:
        """Execute query using MCP server approach"""
        try:
            
            if self.config['access_token']:
                result = self._try_token_query(query)
                if result.get('success'):
                    return result
            
            result = self._try_password_query(query)
            return result
            
        except Exception as e:
            logger.error(f"❌ MCP query execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _try_token_query(self, query: str) -> Dict[str, Any]:
        """Try query execution with access token"""
        try:
            import snowflake.connector
            
            config = {
                'account': self.config['account'],
                'user': self.config['user'],
                'authenticator': 'oauth',
                'token': self.config['access_token'],
                'database': self.config['database'],
                'schema': self.config['schema'],
                'warehouse': self.config['warehouse']
            }
            
            conn = snowflake.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                data = []
                for row in results:
                    data.append(dict(zip(columns, row)))
                
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'data': data,
                    'method': 'token_authentication'
                }
            else:
                cursor.close()
                conn.close()
                return {
                    'success': True,
                    'data': [],
                    'method': 'token_authentication'
                }
                
        except Exception as e:
            logger.warning(f"⚠️ Token authentication failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _try_password_query(self, query: str) -> Dict[str, Any]:
        """Try query execution with password"""
        try:
            import snowflake.connector
            
            config = {
                'account': self.config['account'],
                'user': self.config['user'],
                'password': self.config['password'],
                'database': self.config['database'],
                'schema': self.config['schema'],
                'warehouse': self.config['warehouse']
            }
            
            conn = snowflake.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                data = []
                for row in results:
                    data.append(dict(zip(columns, row)))
                
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'data': data,
                    'method': 'password_authentication'
                }
            else:
                cursor.close()
                conn.close()
                return {
                    'success': True,
                    'data': [],
                    'method': 'password_authentication'
                }
                
        except Exception as e:
            logger.error(f"❌ Password authentication failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def natural_language_to_sql(self, nl_query: str) -> Dict[str, Any]:
        """Convert natural language to SQL using Snowflake Cortex"""
        try:
            cortex_query = f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'llama3-8b',
                'Convert this natural language query to SQL for MCLEOD_DB.dbo schema: {nl_query}'
            ) as sql_suggestion
            """
            
            result = self.execute_mcp_query(cortex_query)
            if result.get('success'):
                sql_suggestion = result['data'][0]['SQL_SUGGESTION']
                
                data_result = self.execute_mcp_query(sql_suggestion)
                
                return {
                    'success': True,
                    'original_query': nl_query,
                    'sql_suggestion': sql_suggestion,
                    'data': data_result.get('data', [])
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Natural language to SQL failed: {e}")
            return {'success': False, 'error': str(e)}

mcp_integration = MCPSnowflakeIntegration()
