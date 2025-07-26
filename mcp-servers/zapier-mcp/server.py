#!/usr/bin/env python3
"""
Zapier MCP Server - Provides Zapier automation capabilities through MCP protocol
Implements webhook triggers, data fetching, and automation workflows
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime
import mcp.server.stdio
from mcp import types
from mcp.server import Server
from mcp.server.models import InitializationOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZapierMCPServer:
    def __init__(self):
        self.api_key = os.getenv('ZAPIER_API_KEY')
        self.webhook_url = os.getenv('ZAPIER_WEBHOOK_URL')
        self.base_url = "https://hooks.zapier.com/hooks/catch"
        self.enabled = os.getenv('MCP_ZAPIER_ENABLED', 'false').lower() == 'true'
        
        if not self.api_key:
            logger.warning("ZAPIER_API_KEY not set - using demo mode")
        
        logger.info(f"Zapier MCP Server initialized - Enabled: {self.enabled}")

    async def trigger_webhook(self, webhook_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a Zapier webhook with provided data"""
        try:
            if not self.enabled:
                return {
                    "success": False,
                    "error": "Zapier MCP integration not enabled",
                    "demo_mode": True
                }
            
            url = f"{self.base_url}/{webhook_id}"
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': self.api_key if self.api_key else 'demo-key'
            }
            
            payload = {
                **data,
                "timestamp": datetime.now().isoformat(),
                "source": "RaiderBot-MCP-Server",
                "mcp_session_id": os.getenv('MCP_SESSION_ID', 'unknown')
            }
            
            if self.api_key:
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                
                return {
                    "success": True,
                    "webhook_id": webhook_id,
                    "status_code": response.status_code,
                    "response": response.text,
                    "data_sent": payload
                }
            else:
                return {
                    "success": True,
                    "webhook_id": webhook_id,
                    "status_code": 200,
                    "response": "Demo webhook triggered successfully",
                    "data_sent": payload,
                    "demo_mode": True
                }
                
        except Exception as e:
            logger.error(f"Webhook trigger failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "webhook_id": webhook_id
            }

    async def fetch_zap_data(self, zap_id: str, limit: int = 10) -> Dict[str, Any]:
        """Fetch data from a Zapier automation (Zap)"""
        try:
            if not self.enabled or not self.api_key:
                return {
                    "success": True,
                    "zap_id": zap_id,
                    "demo_mode": True,
                    "data": [
                        {
                            "id": f"demo_record_{i}",
                            "timestamp": datetime.now().isoformat(),
                            "type": "automation_trigger",
                            "status": "completed",
                            "data": {
                                "customer_id": f"CUST_{1000 + i}",
                                "order_value": 150.00 + (i * 25),
                                "region": ["North", "South", "East", "West"][i % 4],
                                "priority": ["High", "Medium", "Low"][i % 3]
                            }
                        }
                        for i in range(min(limit, 5))
                    ],
                    "total_records": min(limit, 5),
                    "message": "Demo data - configure ZAPIER_API_KEY for live data"
                }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"https://zapier.com/api/v1/zaps/{zap_id}/runs"
            params = {'limit': limit}
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "zap_id": zap_id,
                "data": data.get('runs', []),
                "total_records": len(data.get('runs', [])),
                "demo_mode": False
            }
            
        except Exception as e:
            logger.error(f"Zap data fetch failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "zap_id": zap_id
            }

    async def list_available_zaps(self) -> Dict[str, Any]:
        """List available Zapier automations"""
        try:
            if not self.enabled or not self.api_key:
                return {
                    "success": True,
                    "demo_mode": True,
                    "zaps": [
                        {
                            "id": "demo_zap_001",
                            "name": "Order Processing Automation",
                            "status": "active",
                            "trigger": "New Snowflake Record",
                            "actions": ["Send Email", "Update CRM", "Create Task"]
                        },
                        {
                            "id": "demo_zap_002", 
                            "name": "Customer Notification System",
                            "status": "active",
                            "trigger": "Delivery Status Change",
                            "actions": ["Send SMS", "Update Dashboard", "Log Event"]
                        },
                        {
                            "id": "demo_zap_003",
                            "name": "Revenue Reporting Pipeline",
                            "status": "active", 
                            "trigger": "Daily Schedule",
                            "actions": ["Query Database", "Generate Report", "Email Summary"]
                        }
                    ],
                    "total_zaps": 3,
                    "message": "Demo zaps - configure ZAPIER_API_KEY for live data"
                }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get('https://zapier.com/api/v1/zaps', headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "zaps": data.get('zaps', []),
                "total_zaps": len(data.get('zaps', [])),
                "demo_mode": False
            }
            
        except Exception as e:
            logger.error(f"Zap listing failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def create_automation_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Zapier automation workflow"""
        try:
            workflow_name = workflow_config.get('name', 'Unnamed Workflow')
            trigger_type = workflow_config.get('trigger', 'webhook')
            actions = workflow_config.get('actions', [])
            
            if not self.enabled or not self.api_key:
                return {
                    "success": True,
                    "demo_mode": True,
                    "workflow": {
                        "id": f"demo_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "name": workflow_name,
                        "status": "created",
                        "trigger": trigger_type,
                        "actions": actions,
                        "webhook_url": f"{self.base_url}/demo_webhook_123",
                        "created_at": datetime.now().isoformat()
                    },
                    "message": "Demo workflow created - configure ZAPIER_API_KEY for live creation"
                }
            
            return {
                "success": False,
                "error": "Live workflow creation not implemented - requires Zapier API integration"
            }
            
        except Exception as e:
            logger.error(f"Workflow creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

app = Server("zapier-mcp-server")
zapier_server = ZapierMCPServer()

@app.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Zapier MCP tools"""
    return [
        types.Tool(
            name="trigger_zapier_webhook",
            description="Trigger a Zapier webhook with custom data payload",
            inputSchema={
                "type": "object",
                "properties": {
                    "webhook_id": {
                        "type": "string",
                        "description": "Zapier webhook ID or endpoint identifier"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data payload to send to the webhook"
                    }
                },
                "required": ["webhook_id", "data"]
            }
        ),
        types.Tool(
            name="fetch_zap_data",
            description="Fetch execution data from a Zapier automation (Zap)",
            inputSchema={
                "type": "object",
                "properties": {
                    "zap_id": {
                        "type": "string",
                        "description": "Zapier automation ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records to fetch",
                        "default": 10
                    }
                },
                "required": ["zap_id"]
            }
        ),
        types.Tool(
            name="list_zapier_automations",
            description="List all available Zapier automations and their status",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="create_zapier_workflow",
            description="Create a new Zapier automation workflow",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the new workflow"
                    },
                    "trigger": {
                        "type": "string",
                        "description": "Trigger type (webhook, schedule, etc.)"
                    },
                    "actions": {
                        "type": "array",
                        "description": "List of actions to perform",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "trigger", "actions"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool calls for Zapier MCP operations"""
    try:
        if name == "trigger_zapier_webhook":
            result = await zapier_server.trigger_webhook(
                arguments["webhook_id"],
                arguments["data"]
            )
        elif name == "fetch_zap_data":
            result = await zapier_server.fetch_zap_data(
                arguments["zap_id"],
                arguments.get("limit", 10)
            )
        elif name == "list_zapier_automations":
            result = await zapier_server.list_available_zaps()
        elif name == "create_zapier_workflow":
            result = await zapier_server.create_automation_workflow(arguments)
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}
        
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        logger.error(f"Tool call failed: {e}")
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
                "tool": name
            }, indent=2)
        )]

async def main():
    """Run the Zapier MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="zapier-mcp-server",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                )
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
