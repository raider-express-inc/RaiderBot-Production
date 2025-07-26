#!/usr/bin/env python3
"""
Docker/Kubernetes MCP Server - Provides container orchestration through MCP protocol
Implements Docker container management and Kubernetes deployment capabilities
"""

import os
import json
import asyncio
import logging
import docker
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime
import mcp.server.stdio
from mcp import types
from mcp.server import Server
from mcp.server.models import InitializationOptions

class DockerMCPServer:
    def __init__(self):
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            logging.warning(f"Docker client initialization failed: {e}")
            self.docker_client = None

    async def list_containers(self, all_containers: bool = False) -> Dict[str, Any]:
        """List Docker containers"""
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker client not available"}
            
            containers = self.docker_client.containers.list(all=all_containers)
            container_info = []
            for container in containers:
                container_info.append({
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else "unknown"
                })
            
            return {"success": True, "containers": container_info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def start_container(self, container_name: str) -> Dict[str, Any]:
        """Start Docker container"""
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker client not available"}
            
            container = self.docker_client.containers.get(container_name)
            container.start()
            return {"success": True, "message": f"Container {container_name} started"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def deploy_compose_stack(self, compose_file: str, project_name: str = None) -> Dict[str, Any]:
        """Deploy Docker Compose stack"""
        try:
            cmd = ["docker-compose", "-f", compose_file]
            if project_name:
                cmd.extend(["-p", project_name])
            cmd.append("up")
            cmd.extend(["-d"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_container_logs(self, container_name: str, tail: int = 100) -> Dict[str, Any]:
        """Get Docker container logs"""
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker client not available"}
            
            container = self.docker_client.containers.get(container_name)
            logs = container.logs(tail=tail).decode('utf-8')
            return {"success": True, "logs": logs}
        except Exception as e:
            return {"success": False, "error": str(e)}

app = Server("docker-mcp-server")
docker_server = DockerMCPServer()

@app.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="list_containers",
            description="List Docker containers",
            inputSchema={
                "type": "object",
                "properties": {
                    "all_containers": {"type": "boolean", "description": "Include stopped containers"}
                }
            }
        ),
        types.Tool(
            name="start_container",
            description="Start Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {"type": "string", "description": "Container name or ID"}
                },
                "required": ["container_name"]
            }
        ),
        types.Tool(
            name="deploy_compose_stack",
            description="Deploy Docker Compose stack",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_file": {"type": "string", "description": "Path to docker-compose.yml"},
                    "project_name": {"type": "string", "description": "Project name (optional)"}
                },
                "required": ["compose_file"]
            }
        ),
        types.Tool(
            name="get_container_logs",
            description="Get Docker container logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {"type": "string", "description": "Container name or ID"},
                    "tail": {"type": "integer", "description": "Number of log lines"}
                },
                "required": ["container_name"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    if name == "list_containers":
        result = await docker_server.list_containers(arguments.get("all_containers", False))
    elif name == "start_container":
        result = await docker_server.start_container(arguments["container_name"])
    elif name == "deploy_compose_stack":
        result = await docker_server.deploy_compose_stack(**arguments)
    elif name == "get_container_logs":
        result = await docker_server.get_container_logs(**arguments)
    else:
        result = {"success": False, "error": f"Unknown tool: {name}"}
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="docker-mcp-server", server_version="1.0.0",
            capabilities=app.get_capabilities(notification_options=None, experimental_capabilities=None)
        ))

if __name__ == "__main__":
    asyncio.run(main())
