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
            self._connection = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER', 'ASH073108'),
                authenticator='oauth',
                token=os.getenv('SNOWFLAKE_ACCESS_TOKEN'),
                account=os.getenv('SNOWFLAKE_ACCOUNT', 'LI21842-WW07444'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'TABLEAU_CONNECT'),
                database=database,
                schema=schema,
                client_session_keep_alive=True
            )
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
    
    def close(self):
        """Close connection"""
        if self._connection and not self._connection.is_closed():
            self._connection.close()

snowflake_client = UnifiedSnowflakeConnection()
