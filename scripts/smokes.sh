#!/usr/bin/env bash
set -euo pipefail

echo "== RaiderBot Fix-It Runbook - Comprehensive Smoke Tests =="

export PIPEDREAM_API_KEY="${PIPEDREAM_API_KEY:-7672368099fc1d5e2c3360fc95265da4}"
export PIPEDREAM_API_BASE="${PIPEDREAM_API_BASE:-https://api.pipedream.com/v1}"
export MCP_BASE="${MCP_BASE:-http://localhost:8080}"
export FOUNDRY_TOKEN="${FOUNDRY_TOKEN:-}"
export FUNCTIONS_GATEWAY_BASE="${FUNCTIONS_GATEWAY_BASE:-https://raiderexpress.palantirfoundry.com/functions}"
export SEMANTIC_BASE="${SEMANTIC_BASE:-https://raiderbot-semantic.raiderexpress.palantirfoundry.com}"
export SNOWFLAKE_ACCOUNT="${SNOWFLAKE_ACCOUNT:-LI21842-WW07444}"
export SNOWFLAKE_USER="${SNOWFLAKE_USER:-DEVINAI}"
export SNOWFLAKE_PASSWORD="${SNOWFLAKE_PASSWORD:-R@ider_10141066!}"
export SNOWFLAKE_WAREHOUSE="${SNOWFLAKE_WAREHOUSE:-TABLEAU_CONNECT}"
export SNOWFLAKE_ROLE="${SNOWFLAKE_ROLE:-ACCOUNTADMIN}"
export SNOWFLAKE_DATABASE="${SNOWFLAKE_DATABASE:-MCLEOD_DB}"
export SNOWFLAKE_SCHEMA="${SNOWFLAKE_SCHEMA:-dbo}"

echo "== 1. Pipedream API Health =="
if curl -sSf -H "Authorization: Bearer $PIPEDREAM_API_KEY" \
  "$PIPEDREAM_API_BASE/me" > /tmp/pipedream_me.json; then
  echo "✅ Pipedream API accessible"
  cat /tmp/pipedream_me.json | jq .
else
  echo "❌ Pipedream API failed"
fi

echo "== 2. MCP Server Health =="
if curl -sSf "$MCP_BASE/readyz" > /tmp/mcp_ready.json; then
  echo "✅ MCP Server ready"
  cat /tmp/mcp_ready.json | jq .
else
  echo "❌ MCP Server not ready"
fi

echo "== 3. Pipedream MCP Integration =="
if curl -sSf -X POST "$MCP_BASE/mcp/pipedream/get_me" > /tmp/mcp_pipedream.json; then
  echo "✅ Pipedream MCP integration working"
  cat /tmp/mcp_pipedream.json | jq .
else
  echo "❌ Pipedream MCP integration failed"
fi

echo "== 4. HTTP Relay Test (if PIPEDREAM_RELAY_URL set) =="
if [ -n "${PIPEDREAM_RELAY_URL:-}" ]; then
  if curl -sSf -X POST "$MCP_BASE/mcp/pipedream/http_relay" \
    -H "Content-Type: application/json" \
    -d '{"url":"https://httpbin.org/get","method":"GET","headers":{"Accept":"application/json"}}' \
    > /tmp/relay_test.json; then
    echo "✅ HTTP Relay working"
    cat /tmp/relay_test.json | jq .
  else
    echo "❌ HTTP Relay failed"
  fi
else
  echo "⚠️  PIPEDREAM_RELAY_URL not set, skipping relay test"
fi

echo "== 5. Foundry Functions Health (if token available) =="
if [ -n "$FOUNDRY_TOKEN" ]; then
  if curl -sSf -I --max-redirs 0 \
    -H "Authorization: Bearer $FOUNDRY_TOKEN" \
    "$FUNCTIONS_GATEWAY_BASE/health" 2>/dev/null; then
    echo "✅ Foundry Functions accessible (no redirects)"
  else
    echo "❌ Foundry Functions failed or redirected"
  fi
else
  echo "⚠️  FOUNDRY_TOKEN not set, skipping Foundry test"
fi

echo "== 6. Semantic Server Health =="
if curl -sSf "$SEMANTIC_BASE/_health" > /tmp/semantic_health.json; then
  echo "✅ Semantic Server healthy"
  cat /tmp/semantic_health.json | jq .
else
  echo "❌ Semantic Server failed"
fi

echo "== 7. Snowflake Connection Test =="
python3 - <<'PY'
import os
import json
try:
    import snowflake.connector as sf
    cnx = sf.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ["SNOWFLAKE_ROLE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )
    cs = cnx.cursor()
    cs.execute("SELECT COUNT(*) FROM information_schema.tables LIMIT 1")
    count = cs.fetchone()[0]
    print(f"✅ Snowflake connection successful, found {count} tables")
    cs.close()
    cnx.close()
except Exception as e:
    print(f"❌ Snowflake connection failed: {e}")
PY

echo "== 8. Status Page Generation =="
if python3 status_page.py > /tmp/status_output.txt 2>&1; then
  echo "✅ Status page generated successfully"
  cat /tmp/status_output.txt
else
  echo "❌ Status page generation failed"
  cat /tmp/status_output.txt
fi

echo "== Smoke Tests Complete =="
echo "Check individual test results above for detailed status."
echo "Generated artifacts:"
echo "  - /tmp/pipedream_me.json"
echo "  - /tmp/mcp_ready.json"
echo "  - /tmp/mcp_pipedream.json"
echo "  - /tmp/relay_test.json (if relay configured)"
echo "  - /tmp/semantic_health.json"
echo "  - /tmp/status_output.txt"
echo "  - status.html (status page)"
echo "  - status.json (status data)"
