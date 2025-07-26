#!/usr/bin/env python3
"""
GitHub MCP Server - Provides GitHub API access through MCP protocol
Implements repository management, PR automation, and CI/CD triggers
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

class GitHubMCPServer:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.api_url = os.getenv('GITHUB_API_URL', 'https://api.github.com')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    async def list_repositories(self, org: str = None) -> Dict[str, Any]:
        """List repositories for user or organization"""
        try:
            url = f"{self.api_url}/user/repos" if not org else f"{self.api_url}/orgs/{org}/repos"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "repositories": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_pull_request(self, owner: str, repo: str, title: str, head: str, base: str, body: str = "") -> Dict[str, Any]:
        """Create a pull request"""
        try:
            url = f"{self.api_url}/repos/{owner}/{repo}/pulls"
            data = {"title": title, "head": head, "base": base, "body": body}
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return {"success": True, "pull_request": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        try:
            url = f"{self.api_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "repository": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

app = Server("github-mcp-server")
github_server = GitHubMCPServer()

@app.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="list_repositories",
            description="List GitHub repositories",
            inputSchema={
                "type": "object",
                "properties": {
                    "org": {"type": "string", "description": "Organization name (optional)"}
                }
            }
        ),
        types.Tool(
            name="create_pull_request", 
            description="Create a GitHub pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                    "title": {"type": "string", "description": "PR title"},
                    "head": {"type": "string", "description": "Head branch"},
                    "base": {"type": "string", "description": "Base branch"},
                    "body": {"type": "string", "description": "PR body"}
                },
                "required": ["owner", "repo", "title", "head", "base"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    if name == "list_repositories":
        result = await github_server.list_repositories(arguments.get("org"))
    elif name == "create_pull_request":
        result = await github_server.create_pull_request(**arguments)
    else:
        result = {"success": False, "error": f"Unknown tool: {name}"}
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="github-mcp-server", server_version="1.0.0",
            capabilities=app.get_capabilities(notification_options=None, experimental_capabilities=None)
        ))

if __name__ == "__main__":
    asyncio.run(main())
