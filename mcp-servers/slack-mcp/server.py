#!/usr/bin/env python3
"""
Slack MCP Server - Provides Slack integration through MCP protocol
Implements messaging, channel management, and notification workflows
"""

import os
import json
import asyncio
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import mcp.server.stdio
from mcp import types
from mcp.server import Server
from mcp.server.models import InitializationOptions

class SlackMCPServer:
    def __init__(self):
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.app_token = os.getenv('SLACK_APP_TOKEN')
        self.base_url = "https://slack.com/api"
        self.headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }

    async def send_message(self, channel: str, text: str, blocks: List[Dict] = None) -> Dict[str, Any]:
        """Send message to Slack channel"""
        try:
            url = f"{self.base_url}/chat.postMessage"
            data = {"channel": channel, "text": text}
            if blocks:
                data["blocks"] = blocks
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return {"success": True, "message": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_channels(self) -> Dict[str, Any]:
        """List Slack channels"""
        try:
            url = f"{self.base_url}/conversations.list"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "channels": response.json()['channels']}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_channel(self, name: str, is_private: bool = False) -> Dict[str, Any]:
        """Create Slack channel"""
        try:
            url = f"{self.base_url}/conversations.create"
            data = {"name": name, "is_private": is_private}
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return {"success": True, "channel": response.json()['channel']}
        except Exception as e:
            return {"success": False, "error": str(e)}

app = Server("slack-mcp-server")
slack_server = SlackMCPServer()

@app.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="send_message",
            description="Send message to Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Channel ID or name"},
                    "text": {"type": "string", "description": "Message text"},
                    "blocks": {"type": "array", "description": "Slack blocks (optional)"}
                },
                "required": ["channel", "text"]
            }
        ),
        types.Tool(
            name="list_channels",
            description="List Slack channels",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="create_channel",
            description="Create Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Channel name"},
                    "is_private": {"type": "boolean", "description": "Private channel"}
                },
                "required": ["name"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    if name == "send_message":
        result = await slack_server.send_message(**arguments)
    elif name == "list_channels":
        result = await slack_server.list_channels()
    elif name == "create_channel":
        result = await slack_server.create_channel(**arguments)
    else:
        result = {"success": False, "error": f"Unknown tool: {name}"}
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="slack-mcp-server", server_version="1.0.0",
            capabilities=app.get_capabilities(notification_options=None, experimental_capabilities=None)
        ))

if __name__ == "__main__":
    asyncio.run(main())
