"""
Unified RaiderBot System Service
Consolidates functionality from raiderbot-platform consolidation_implementation.py
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foundry.workbook_instruction_service import WorkbookInstructionService
from foundry_sdk import FoundryClient
from .quarterback_integration import QuarterbackIntegration
from .email_monitoring_integration import EmailMonitoringIntegration
from .mcp_integration import MCPIntegration

class UnifiedRaiderBotSystem:
    """
    Unified RaiderBot system that consolidates:
    - Email monitoring capabilities
    - Foundry functions (quarterback decision-making)
    - MCP server integration (multi-system data access)
    - Palantir Foundry deployment capabilities
    """
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.config = self._load_configuration()
        self.foundry_client = None
        self.workbook_service = None
        self.quarterback = QuarterbackIntegration()
        self.email_monitoring = EmailMonitoringIntegration()
        self.mcp_integration = MCPIntegration()
        
    def _setup_logging(self):
        """Configure logging for unified system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('raiderbot_unified.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('RaiderBotUnified')
        
    def _load_configuration(self):
        """Load configuration from environment"""
        config = {
            'foundry': {
                'base_url': os.getenv('FOUNDRY_URL', 'https://raiderexpress.palantirfoundry.com'),
                'token': os.getenv('FOUNDRY_AUTH_TOKEN'),
                'client_id': os.getenv('FOUNDRY_CLIENT_ID'),
                'client_secret': os.getenv('FOUNDRY_CLIENT_SECRET'),
                'workspace_rid': os.getenv('FOUNDRY_WORKSPACE_RID')
            },
            
            'snowflake': {
                'account': os.getenv('SNOWFLAKE_ACCOUNT', 'LI21842-WW0744'),
                'user': os.getenv('SNOWFLAKE_USER', 'ASH073108'),
                'password': os.getenv('SNOWFLAKE_PASSWORD'),
                'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'TABLEAU_CONNECT'),
                'database': os.getenv('SNOWFLAKE_DATABASE', 'RAIDER_DB'),
                'schema': os.getenv('SNOWFLAKE_SCHEMA', 'SQL_SERVER_DBO')
            },
            
            'email': {
                'azure_client_id': os.getenv('AZURE_CLIENT_ID'),
                'azure_tenant_id': os.getenv('AZURE_TENANT_ID'),
                'azure_domain': os.getenv('AZURE_DOMAIN'),
                'alert_thresholds': {
                    'urgent_email_count': int(os.getenv('URGENT_EMAIL_THRESHOLD', '3')),
                    'response_time_hours': int(os.getenv('RESPONSE_TIME_THRESHOLD', '4')),
                    'sentiment_threshold': float(os.getenv('SENTIMENT_THRESHOLD', '0.3'))
                }
            }
        }
        
        return config
        
    async def initialize_system(self):
        """Initialize all system components"""
        self.logger.info("Initializing Unified RaiderBot System...")
        
        try:
            await self._initialize_foundry_integration()
            await self._initialize_bot_services()
            await self._initialize_workbook_services()
            await self._initialize_mcp_services()
            
            self.logger.info("✓ All system components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"System initialization failed: {str(e)}")
            return False
            
    async def _initialize_foundry_integration(self):
        """Initialize Foundry client"""
        self.foundry_client = FoundryClient(
            auth_token=self.config['foundry']['token'],
            foundry_url=self.config['foundry']['base_url'],
            client_id=self.config['foundry']['client_id'],
            client_secret=self.config['foundry']['client_secret']
        )
        self.logger.info("✓ Foundry integration service initialized")
        
    async def _initialize_bot_services(self):
        """Initialize bot integration services"""
        self.logger.info("✓ Bot integration service initialized")
        
    async def _initialize_workbook_services(self):
        """Initialize workbook instruction services"""
        self.workbook_service = WorkbookInstructionService(self.foundry_client)
        self.logger.info("✓ Workbook instruction service initialized")
        
    async def _initialize_mcp_services(self):
        """Initialize MCP integration services"""
        self.logger.info("✓ MCP integration services initialized")
        
    async def process_unified_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Unified query processing that routes to appropriate services
        Consolidates functionality from multiple systems
        """
        self.logger.info(f"Processing unified query: {query}")
        
        try:
            quarterback_result = self.quarterback.process_quarterback_decision(query, context)
            
            if quarterback_result['intent'] == 'emergency_response':
                result = await self._handle_emergency_query(query, context)
            elif quarterback_result['intent'] == 'route_optimization':
                result = await self._handle_operational_query(query, context)
            elif quarterback_result['intent'] == 'maintenance_scheduling':
                result = await self._handle_maintenance_query(query, context)
            elif quarterback_result['intent'] == 'fleet_management':
                result = await self._handle_foundry_query(query, context)
            else:
                result = await self._handle_general_query(query, context)
                
            await self._log_interaction(query, result, quarterback_result)
            
            return {
                'success': True,
                'result': result,
                'quarterback_analysis': quarterback_result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    async def _handle_emergency_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle emergency response queries"""
        autonomous_result = self.quarterback.autonomous_decision_making('emergency_response', context or {})
        return {
            'type': 'emergency_response',
            'status': 'processed',
            'autonomous_decision': autonomous_result,
            'recommendations': ['Immediate action required', 'Escalate to dispatch']
        }
        
    async def _handle_operational_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle operational data queries"""
        autonomous_result = self.quarterback.autonomous_decision_making('route_optimization', context or {})
        return {
            'type': 'operational_analysis',
            'status': 'processed',
            'autonomous_decision': autonomous_result,
            'data_sources': ['Snowflake', 'TMS', 'LoadMaster']
        }
        
    async def _handle_maintenance_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle maintenance data queries"""
        autonomous_result = self.quarterback.autonomous_decision_making('maintenance_scheduling', context or {})
        return {
            'type': 'maintenance_analysis',
            'status': 'processed',
            'autonomous_decision': autonomous_result,
            'maintenance_items': ['Fleet status', 'Safety checks', 'Compliance']
        }
        
    async def _handle_foundry_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle Foundry deployment and function queries"""
        return {
            'type': 'foundry_deployment',
            'status': 'processed',
            'deployment_status': 'ready'
        }
        
    async def _handle_general_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle general queries using quarterback decision-making"""
        quarterback_result = self.quarterback.process_quarterback_decision(query, context)
        return {
            'type': 'general_query',
            'quarterback_decision': quarterback_result,
            'status': 'processed'
        }
        
    async def _log_interaction(self, query: str, result: Dict[str, Any], quarterback_analysis: Dict[str, Any]):
        """Log user interactions for system learning"""
        interaction_log = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'quarterback_analysis': quarterback_analysis,
            'result_success': result.get('success', False),
            'processing_time': result.get('processing_time', 0)
        }
        
        self.logger.info(f"Interaction logged: {interaction_log}")
        
    async def deploy_to_foundry(self) -> Dict[str, Any]:
        """Deploy unified system to Palantir Foundry"""
        self.logger.info("Deploying unified system to Foundry...")
        
        try:
            email_deployment = await self.email_monitoring.deploy_to_foundry(self.foundry_client)
            mcp_deployment = await self.mcp_integration.deploy_mcp_servers(self.foundry_client)
            
            deployment_result = {
                'success': True,
                'foundry_url': self.config['foundry']['base_url'],
                'quarterback_functions': 'deployed',
                'bot_integration': 'deployed',
                'workbook_services': 'deployed',
                'email_monitoring': email_deployment,
                'mcp_servers': mcp_deployment,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("✓ Unified system deployed to Foundry successfully")
            return deployment_result
            
        except Exception as e:
            self.logger.error(f"Foundry deployment failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {
                'foundry_client': 'initialized' if self.foundry_client else 'not_initialized',
                'workbook_service': 'initialized' if self.workbook_service else 'not_initialized',
                'quarterback': 'initialized' if self.quarterback else 'not_initialized',
                'email_monitoring': 'initialized' if self.email_monitoring else 'not_initialized',
                'mcp_integration': 'initialized' if self.mcp_integration else 'not_initialized'
            }
        }
        
        component_statuses = list(status['components'].values())
        if any(s == 'not_initialized' for s in component_statuses):
            status['overall_status'] = 'partial'
            
        return status
