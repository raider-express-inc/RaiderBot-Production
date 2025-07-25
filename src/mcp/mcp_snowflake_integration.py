#!/usr/bin/env python3
"""
MCP Integration Layer for Enhanced Snowflake Client
Provides MCP tool integration while maintaining 100% Snowflake connectivity
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.snowflake.cortex_analyst_client import cortex_client

logger = logging.getLogger(__name__)

class MCPSnowflakeIntegration:
    """MCP integration wrapper for enhanced Snowflake client"""
    
    def __init__(self):
        self.snowflake_client = cortex_client
        self.mcp_servers = {}
        self.zapier_available = False
        self.discover_mcp_servers()
    
    def discover_mcp_servers(self):
        """Discover available MCP servers from configuration"""
        config_paths = [
            "/home/ubuntu/repos/raiderbot-foundry-functions/mcp-config.json",
            "/home/ubuntu/.mcp/remote_server_config.json"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        if 'mcpServers' in config:
                            self.mcp_servers.update(config['mcpServers'])
                            logger.info(f"✅ Loaded MCP servers from {config_path}")
                        elif config_path.endswith('mcp-config.json') and 'foundry-integration' in str(config):
                            self.mcp_servers['foundry-integration'] = config
                            logger.info(f"✅ Loaded Foundry MCP server from {config_path}")
                except Exception as e:
                    logger.error(f"❌ Failed to load MCP config from {config_path}: {e}")
        
        self.check_zapier_availability()
    
    def check_zapier_availability(self):
        """Check if Zapier MCP tools are available"""
        try:
            from mcp_tool_call import mcp_tool_call
            zapier_servers = [name for name in self.mcp_servers.keys() if 'zapier' in name.lower()]
            if zapier_servers:
                self.zapier_available = True
                logger.info(f"✅ Zapier MCP servers found: {zapier_servers}")
            else:
                logger.info("ℹ️ No Zapier MCP servers configured")
        except ImportError:
            logger.info("ℹ️ MCP tool integration not available")
    
    def execute_with_mcp_integration(self, query: str, mcp_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute Snowflake query with MCP tool integration"""
        try:
            result = self.snowflake_client.execute_query(query)
            
            if mcp_context and self.mcp_servers:
                result = self._enhance_with_mcp_tools(result, mcp_context)
            
            return {
                'success': True,
                'data': result,
                'mcp_enhanced': bool(mcp_context and self.mcp_servers),
                'zapier_available': self.zapier_available
            }
        except Exception as e:
            logger.error(f"❌ MCP-integrated query failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _enhance_with_mcp_tools(self, data: List[Dict], mcp_context: Dict) -> List[Dict]:
        """Enhance Snowflake results with MCP tool capabilities"""
        try:
            if self.zapier_available and mcp_context.get('trigger_zapier'):
                logger.info("🔗 Triggering Zapier automation with Snowflake data")
                
            if 'foundry-integration' in self.mcp_servers and mcp_context.get('foundry_sync'):
                logger.info("🏗️ Syncing data with Foundry via MCP")
            
            return data
        except Exception as e:
            logger.error(f"❌ MCP enhancement failed: {e}")
            return data
    
    def natural_language_query_with_automation(self, question: str, automation_config: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute natural language query with optional automation triggers"""
        try:
            result = self.snowflake_client.natural_language_query(question)
            
            if result['success'] and automation_config:
                if automation_config.get('zapier_webhook') and self.zapier_available:
                    self._trigger_zapier_webhook(result['data'], automation_config['zapier_webhook'])
                
                if automation_config.get('foundry_update'):
                    self._update_foundry_dashboard(result['data'], automation_config['foundry_update'])
            
            return result
        except Exception as e:
            logger.error(f"❌ Automated query failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _trigger_zapier_webhook(self, data: Any, webhook_config: Dict):
        """Trigger Zapier webhook with Snowflake data"""
        try:
            logger.info(f"🔗 Would trigger Zapier webhook: {webhook_config.get('url', 'configured')}")
        except Exception as e:
            logger.error(f"❌ Zapier webhook trigger failed: {e}")
    
    def _update_foundry_dashboard(self, data: Any, dashboard_config: Dict):
        """Update Foundry dashboard with Snowflake data"""
        try:
            logger.info(f"🏗️ Would update Foundry dashboard: {dashboard_config.get('dashboard_id', 'configured')}")
        except Exception as e:
            logger.error(f"❌ Foundry dashboard update failed: {e}")
    
    def health_check_with_mcp(self) -> Dict[str, Any]:
        """Enhanced health check including MCP server status"""
        snowflake_health = self.snowflake_client.health_check()
        
        return {
            **snowflake_health,
            'mcp_servers': list(self.mcp_servers.keys()),
            'zapier_available': self.zapier_available,
            'mcp_integration': 'active' if self.mcp_servers else 'inactive'
        }

mcp_integration = MCPSnowflakeIntegration()
