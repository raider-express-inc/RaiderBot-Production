#!/usr/bin/env python3
"""
AWS MCP Server - Provides AWS resource management through MCP protocol
Implements S3, CloudFront, Lambda, and infrastructure management
"""

import os
import json
import asyncio
import logging
import boto3
from typing import Dict, List, Any, Optional
from datetime import datetime
import mcp.server.stdio
from mcp import types
from mcp.server import Server
from mcp.server.models import InitializationOptions

class AWSMCPServer:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        self.s3 = self.session.client('s3')
        self.cloudformation = self.session.client('cloudformation')
        self.lambda_client = self.session.client('lambda')

    async def list_s3_buckets(self) -> Dict[str, Any]:
        """List S3 buckets"""
        try:
            response = self.s3.list_buckets()
            return {"success": True, "buckets": response['Buckets']}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def deploy_cloudformation_stack(self, stack_name: str, template_body: str, parameters: List[Dict] = None) -> Dict[str, Any]:
        """Deploy CloudFormation stack"""
        try:
            kwargs = {
                'StackName': stack_name,
                'TemplateBody': template_body,
                'Capabilities': ['CAPABILITY_IAM']
            }
            if parameters:
                kwargs['Parameters'] = parameters
            
            response = self.cloudformation.create_stack(**kwargs)
            return {"success": True, "stack_id": response['StackId']}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_lambda_functions(self) -> Dict[str, Any]:
        """List Lambda functions"""
        try:
            response = self.lambda_client.list_functions()
            return {"success": True, "functions": response['Functions']}
        except Exception as e:
            return {"success": False, "error": str(e)}

app = Server("aws-mcp-server")
aws_server = AWSMCPServer()

@app.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="list_s3_buckets",
            description="List AWS S3 buckets",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="deploy_cloudformation_stack",
            description="Deploy CloudFormation stack",
            inputSchema={
                "type": "object",
                "properties": {
                    "stack_name": {"type": "string"},
                    "template_body": {"type": "string"},
                    "parameters": {"type": "array"}
                },
                "required": ["stack_name", "template_body"]
            }
        ),
        types.Tool(
            name="list_lambda_functions",
            description="List AWS Lambda functions",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    if name == "list_s3_buckets":
        result = await aws_server.list_s3_buckets()
    elif name == "deploy_cloudformation_stack":
        result = await aws_server.deploy_cloudformation_stack(**arguments)
    elif name == "list_lambda_functions":
        result = await aws_server.list_lambda_functions()
    else:
        result = {"success": False, "error": f"Unknown tool: {name}"}
    
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="aws-mcp-server", server_version="1.0.0",
            capabilities=app.get_capabilities(notification_options=None, experimental_capabilities=None)
        ))

if __name__ == "__main__":
    asyncio.run(main())
