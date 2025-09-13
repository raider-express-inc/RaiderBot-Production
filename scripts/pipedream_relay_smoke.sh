#!/usr/bin/env bash
set -euo pipefail
if [ -z "${PIPEDREAM_RELAY_URL:-}" ]; then echo "PIPEDREAM_RELAY_URL not set"; exit 1; fi
curl -sS -X POST http://localhost:8080/mcp/pipedream/http_relay \
  -H "Content-Type: application/json" \
  -d '{"url":"https://httpbin.org/get","method":"GET","headers":{"Accept":"application/json"}}' | jq .
echo "✅ Relay smoke passed"
