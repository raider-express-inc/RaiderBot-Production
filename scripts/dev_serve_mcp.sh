#!/usr/bin/env bash
set -euo pipefail
export PIPEDREAM_API_BASE="${PIPEDREAM_API_BASE:-https://api.pipedream.com/v1}"
uvicorn mcp_server:app --host 0.0.0.0 --port 8080 --reload
