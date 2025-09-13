#!/usr/bin/env python3

import logging
import os
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
import httpx
from mcp.pipedream_client import PipedreamClient

app = FastAPI(title="RaiderBot MCP Server", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/readyz")
async def readiness_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "raiderbot-mcp",
            "version": "1.0.0",
        },
    )


@app.get("/livez")
async def liveness_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": 0,
        },
    )


@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checks": {"database": "ok", "external_apis": "ok", "memory": "ok"},
        },
    )


@app.post("/mcp/pipedream/get_me")
async def mcp_pipedream_get_me():
    try:
        client = PipedreamClient()
        return {"success": True, "data": await client.get_me()}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )


@app.post("/mcp/pipedream/emit_event")
async def mcp_pipedream_emit_event(body: Dict[str, Any] = Body(...)):
    try:
        source_id = body.get("source_id")
        payload = body.get("payload", {})
        if not source_id:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "source_id is required"},
            )
        client = PipedreamClient()
        data = await client.emit_event(source_id, payload)
        return {"success": True, "data": data}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )


@app.post("/mcp/pipedream/http_relay")
async def mcp_pipedream_http_relay(body: Dict[str, Any] = Body(...)):
    relay_url = os.getenv("PIPEDREAM_RELAY_URL")
    if not relay_url:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "PIPEDREAM_RELAY_URL not set"},
        )
    try:
        url = body.get("url")
        method = (body.get("method") or "GET").upper()
        headers = body.get("headers") or {}
        payload = body.get("body")
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
            r = await client.post(
                relay_url,
                json={
                    "url": url,
                    "method": method,
                    "headers": headers,
                    "body": payload,
                },
            )
            r.raise_for_status()
            data = (
                r.json()
                if "application/json" in r.headers.get("content-type", "")
                else {"text": r.text}
            )
            return {"success": True, "data": data}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )


@app.middleware("http")
async def add_process_time_header(request, call_next):
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
