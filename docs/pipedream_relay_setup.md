# Pipedream HTTP Relay Setup Guide

## Overview
The Pipedream HTTP relay allows bypassing 307/401/SSL connectivity issues by proxying requests through Pipedream's infrastructure.

## Setup Steps

### 1. Create Pipedream Workflow
1. Go to [Pipedream](https://pipedream.com) and create a new workflow
2. Add HTTP Request trigger (accepts JSON body)
3. Add Code step with this Node.js code:

```javascript
// Expects JSON body: { url, method, headers, body }
export default defineComponent({
  async run({ steps, $ }) {
    const { url, method = "GET", headers = {}, body } = $.steps.trigger.event.body || {};
    if (!url) throw new Error("url required");
    const res = await $.http(url, {
      method,
      headers,
      data: body,
      // Do not follow redirects (surface 3xx upstream)
      maxRedirects: 0,
      validateStatus: () => true
    });
    return {
      status: res.status,
      statusText: res.statusText,
      headers: res.headers,
      data: res.data
    };
  },
});
```

4. Deploy the workflow
5. Copy the public HTTP endpoint URL (e.g., `https://xxxxxx.m.pipedream.net`)

### 2. Configure Environment
Set the relay URL in your environment:
```bash
export PIPEDREAM_RELAY_URL="https://xxxxxx.m.pipedream.net"
```

### 3. Usage
The relay is automatically used by the MCP server endpoint `/mcp/pipedream/http_relay` and can be called programmatically to bypass connectivity issues.

## Testing
Run the relay smoke test:
```bash
./scripts/pipedream_relay_smoke.sh
```
