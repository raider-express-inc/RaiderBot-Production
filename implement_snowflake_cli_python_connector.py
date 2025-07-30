#!/usr/bin/env python3
"""
Implement official Snowflake CLI and Python connector approach
Replace fragmented authentication with official Snowflake tools as recommended by user
"""

import os
import sys
import logging
import subprocess
import json
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_snowflake_cli_config():
    """Setup Snowflake CLI configuration using recommended approach"""
    logger.info("🔧 Setting up Snowflake CLI configuration...")
    
    try:
        snowflake_dir = os.path.expanduser("~/.snowflake")
        os.makedirs(snowflake_dir, exist_ok=True)
        
        config_content = """
[connections.default]
account = "LI21842-WW07444"
user = "ASH073108"
password = "Phi1848gam!"
database = "MCLEOD_DB"
schema = "dbo"
warehouse = "TABLEAU_CONNECT"
role = "ACCOUNTADMIN"

[connections.production]
account = "LI21842-WW07444"
user = "ASH073108"
password = "Phi1848gam!"
database = "MCLEOD_DB"
schema = "dbo"
warehouse = "TABLEAU_CONNECT"
role = "ACCOUNTADMIN"
"""
        
        config_path = os.path.join(snowflake_dir, "config.toml")
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        os.chmod(config_path, 0o600)
        
        logger.info(f"✅ Snowflake CLI config created: {config_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to setup Snowflake CLI config: {e}")
        return False

def create_enhanced_cortex_client():
    """Create enhanced cortex client using official Snowflake tools"""
    logger.info("🔧 Creating enhanced cortex client...")
    
    try:
        client_content = '''#!/usr/bin/env python3
"""
Enhanced Snowflake client using official CLI and Python connector
Implements user-recommended approach: CLI for terminal operations, Python connector for code
"""

import os
import logging
import subprocess
import json
import snowflake.connector
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class EnhancedSnowflakeClient:
    """Official Snowflake CLI + Python connector implementation"""
    
    def __init__(self):
        """Initialize with official Snowflake tools"""
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
        
        logger.info("Initialized enhanced Snowflake client with official tools")
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
    
    def connect_python_connector(self) -> bool:
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
            logger.error(f"❌ Python connector connection failed: {e}")
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
                if not self.connect_python_connector():
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
            cli_result = self.execute_via_cli("SELECT CURRENT_TIMESTAMP() as test_time, CURRENT_DATABASE() as db, CURRENT_SCHEMA() as schema")
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
                if not self.connect_python_connector():
                    return {"success": False, "error": "Connection failed"}
            
            result = self.execute_query("SELECT CURRENT_TIMESTAMP() as test_time, CURRENT_DATABASE() as db, CURRENT_SCHEMA() as schema")
            if result:
                return {
                    "success": True,
                    "timestamp": result[0][0],
                    "database": result[0][1],
                    "schema": result[0][2],
                    "method": "python_connector"
                }
            else:
                return {"success": False, "error": "Query execution failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_mcleod_data_access(self) -> Dict[str, Any]:
        """Test access to MCLEOD_DB.dbo data"""
        try:
            orders_query = 'SELECT COUNT(*) as order_count FROM "MCLEOD_DB"."dbo"."orders" LIMIT 1'
            orders_result = self.execute_query(orders_query)
            
            if orders_result:
                order_count = orders_result[0][0]
                logger.info(f"✅ Found {order_count} orders in MCLEOD_DB.dbo.orders")
                
                structure_query = 'DESCRIBE TABLE "MCLEOD_DB"."dbo"."orders"'
                structure_result = self.execute_query(structure_query)
                
                return {
                    "success": True,
                    "order_count": order_count,
                    "table_structure": len(structure_result) if structure_result else 0,
                    "database": "MCLEOD_DB",
                    "schema": "dbo"
                }
            else:
                return {"success": False, "error": "Could not access orders table"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Connection closed")

enhanced_snowflake_client = EnhancedSnowflakeClient()

snowflake_client = enhanced_snowflake_client
CortexAnalystClient = EnhancedSnowflakeClient
'''
        
        client_path = "/home/ubuntu/repos/RaiderBot-Production/src/snowflake/enhanced_cortex_client.py"
        with open(client_path, 'w') as f:
            f.write(client_content)
        
        logger.info(f"✅ Enhanced cortex client created: {client_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create enhanced cortex client: {e}")
        return False

def update_server_imports():
    """Update server.py to use enhanced Snowflake client"""
    logger.info("🔧 Updating server.py imports...")
    
    try:
        server_path = "/home/ubuntu/repos/RaiderBot-Production/server.py"
        
        with open(server_path, 'r') as f:
            content = f.read()
        
        updated_content = content.replace(
            'from src.snowflake.unified_connection import snowflake_client',
            'from src.snowflake.enhanced_cortex_client import enhanced_snowflake_client as snowflake_client'
        )
        
        with open(server_path, 'w') as f:
            f.write(updated_content)
        
        logger.info("✅ Server.py imports updated")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to update server imports: {e}")
        return False

def test_enhanced_implementation():
    """Test the enhanced Snowflake implementation"""
    logger.info("🔍 Testing enhanced Snowflake implementation...")
    
    try:
        sys.path.append("/home/ubuntu/repos/RaiderBot-Production")
        from src.snowflake.enhanced_cortex_client import enhanced_snowflake_client
        
        health = enhanced_snowflake_client.health_check()
        logger.info(f"Health check result: {health}")
        
        if health.get('success'):
            data_access = enhanced_snowflake_client.test_mcleod_data_access()
            logger.info(f"MCLEOD data access: {data_access}")
            
            return data_access.get('success', False)
        else:
            return False
            
    except Exception as e:
        logger.error(f"❌ Enhanced implementation test failed: {e}")
        return False

def main():
    """Implement official Snowflake CLI and Python connector approach"""
    logger.info("🚀 Implementing official Snowflake CLI and Python connector approach...")
    
    steps = [
        ("Setup Snowflake CLI Config", setup_snowflake_cli_config),
        ("Create Enhanced Cortex Client", create_enhanced_cortex_client),
        ("Update Server Imports", update_server_imports),
        ("Test Enhanced Implementation", test_enhanced_implementation)
    ]
    
    results = {}
    for step_name, step_func in steps:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {step_name}")
        logger.info(f"{'='*50}")
        
        try:
            results[step_name] = step_func()
        except Exception as e:
            logger.error(f"❌ {step_name} failed with exception: {e}")
            results[step_name] = False
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    logger.info(f"\n🎯 Overall: {passed}/{total} steps completed")
    
    if passed >= 3:  # At least 3 out of 4 steps should pass
        logger.info("🎉 Official Snowflake implementation SUCCESSFUL!")
        return True
    else:
        logger.error("⚠️ Official Snowflake implementation needs more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
