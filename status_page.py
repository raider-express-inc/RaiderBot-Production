#!/usr/bin/env python3

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import httpx
import yaml


class StatusPage:
    def __init__(self, config_path: str = "env/apis.yaml"):
        self.config = self._load_config(config_path)
        self.endpoints = self._get_endpoints()

    def _load_config(self, path: str) -> Dict[str, str]:
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {
                "functions_gateway_base": "https://raiderexpress.palantirfoundry.com/functions",
                "langgraph_service_base": "https://raiderbot-brain.raiderexpress.palantirfoundry.com",
                "semantic_base": "https://raiderbot-semantic.raiderexpress.palantirfoundry.com",
                "mcp_base": "https://raiderbot-mcp.raiderexpress.palantirfoundry.com",
            }

    def _get_endpoints(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "Foundry Functions",
                "url": self.config.get(
                    "functions_health_url",
                    f"{self.config['functions_gateway_base']}/health",
                ),
                "type": "foundry_function",
            },
            {
                "name": "LangGraph Service",
                "url": f"{self.config['langgraph_service_base']}/healthz",
                "type": "langgraph",
            },
            {
                "name": "Semantic Server",
                "url": f"{self.config['semantic_base']}/_health",
                "type": "semantic",
            },
            {
                "name": "MCP Server",
                "url": f"{self.config['mcp_base']}/readyz",
                "type": "mcp",
            },
            {
                "name": "Pipedream API",
                "url": "http://localhost:8080/mcp/pipedream/get_me",
                "type": "pipedream",
            },
        ]

    async def check_endpoint(self, endpoint: Dict[str, str]) -> Dict[str, Any]:
        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(endpoint["url"], follow_redirects=False)

                latency_ms = int((time.time() - start_time) * 1000)

                return {
                    "name": endpoint["name"],
                    "url": endpoint["url"],
                    "status": (
                        "healthy" if 200 <= response.status_code < 300 else "unhealthy"
                    ),
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "redirect_detected": 300 <= response.status_code < 400,
                }

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "name": endpoint["name"],
                "url": endpoint["url"],
                "status": "error",
                "error": str(e),
                "latency_ms": latency_ms,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    async def check_all(self) -> Dict[str, Any]:
        tasks = [self.check_endpoint(ep) for ep in self.endpoints]
        results = await asyncio.gather(*tasks)

        healthy_count = sum(1 for r in results if r.get("status") == "healthy")
        total_count = len(results)

        return {
            "overall_status": "healthy" if healthy_count == total_count else "degraded",
            "healthy_services": healthy_count,
            "total_services": total_count,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "services": results,
        }

    def generate_html(self, status_data: Dict[str, Any]) -> str:
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RaiderBot Status</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .healthy {{ color: green; }}
        .unhealthy {{ color: red; }}
        .degraded {{ color: orange; }}
        .service {{ margin: 10px 0; padding: 10px; border: 1px solid #ccc; }}
    </style>
</head>
<body>
    <h1>RaiderBot System Status</h1>
    <p>Overall Status: <span class="{status_data['overall_status']}">{status_data['overall_status'].upper()}</span></p>
    <p>Services: {status_data['healthy_services']}/{status_data['total_services']} healthy</p>
    <p>Last Updated: {status_data['timestamp']}</p>
    
    <h2>Service Details</h2>
"""

        for service in status_data["services"]:
            status_class = service.get("status", "error")
            html += f"""
    <div class="service">
        <h3>{service['name']} - <span class="{status_class}">{service.get('status', 'unknown').upper()}</span></h3>
        <p>URL: {service['url']}</p>
        <p>Latency: {service.get('latency_ms', 'N/A')}ms</p>
        <p>Status Code: {service.get('status_code', 'N/A')}</p>
        {f"<p>Error: {service['error']}</p>" if 'error' in service else ""}
        {"<p><strong>⚠️ Redirect Detected</strong></p>" if service.get('redirect_detected') else ""}
    </div>
"""

        html += """
</body>
</html>
"""
        return html


async def main():
    status_page = StatusPage()
    status_data = await status_page.check_all()

    with open("status.json", "w") as f:
        json.dump(status_data, f, indent=2)

    html_content = status_page.generate_html(status_data)
    with open("status.html", "w") as f:
        f.write(html_content)

    print(f"Status: {status_data['overall_status']}")
    print(
        f"Services: {status_data['healthy_services']}/{status_data['total_services']} healthy"
    )

    for service in status_data["services"]:
        status_icon = "✅" if service.get("status") == "healthy" else "❌"
        print(f"{status_icon} {service['name']}: {service.get('status', 'unknown')}")


if __name__ == "__main__":
    asyncio.run(main())
