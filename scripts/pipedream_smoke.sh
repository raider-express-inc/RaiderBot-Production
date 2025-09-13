#!/usr/bin/env bash
set -euo pipefail

if [ -z "${PIPEDREAM_API_KEY:-}" ]; then
  echo "❌ PIPEDREAM_API_KEY not set"; exit 1
fi

BASE="${PIPEDREAM_API_BASE:-https://api.pipedream.com/v1}"
echo "== GET /users/me =="
curl -sS -H "Authorization: Bearer ${PIPEDREAM_API_KEY}" \
     -H "Accept: application/json" \
     --max-redirs 0 \
     "${BASE}/users/me" | jq . >/tmp/pipedream_me.json

echo "User info saved to /tmp/pipedream_me.json"
echo "✅ Pipedream smoke passed"
