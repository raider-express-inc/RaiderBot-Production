# RaiderBot Fix-It Runbook - Implementation Results

This document summarizes the implementation of the RaiderBot Fix-It Runbook across all 10 sections.

## Quick Start - Smoke Tests

Run these commands to verify all components are working:

```bash
# 1. Publish Foundry Functions
./scripts/publish_functions.sh

# 2. Register AIP Tools (dry-run first)
python scripts/register_aip_tool.py --dry-run

# 3. Run comprehensive smoke tests
./scripts/smokes.sh
```

## Environment Setup

Required environment variables:
```bash
# Foundry OAuth
export FOUNDry_OAUTH_CLIENT_ID="your-client-id"
export FOUNDry_OAUTH_CLIENT_SECRET="your-client-secret"
export FOUNDry_OAUTH_TOKEN_URL="https://raiderexpress.palantirfoundry.com/multipass/api/oauth2/token"

# Foundry API
export FOUNDRY_TOKEN="your-foundry-token"

# Snowflake OAuth
export SNOWFLAKE_OAUTH_CLIENT_ID="your-snowflake-client-id"
export SNOWFLAKE_OAUTH_CLIENT_SECRET="your-snowflake-client-secret"
export SNOWFLAKE_OAUTH_TOKEN="your-oauth-token"

# Snowflake Connection
export SNOWFLAKE_ACCOUNT="LI21842-WW07444"
export SNOWFLAKE_USER="DEVINAI"
export SNOWFLAKE_PASSWORD="R@ider_10141066!"
export SNOWFLAKE_DATABASE="MCLEOD_DB"
export SNOWFLAKE_SCHEMA="dbo"
export SNOWFLAKE_WAREHOUSE="TABLEAU_CONNECT"
export SNOWFLAKE_ROLE="ACCOUNTADMIN"
```

## Implementation Status

### ✅ Completed Sections

1. **Section 0 - Global Preconditions**: Environment setup and secrets baseline
2. **Section 1 - Fix Foundry Functions**: Scripts and manifests created
3. **Section 2 - Repair Semantic Layer Servers**: Health endpoints and dependencies
4. **Section 3 - Fix LangGraph Service Auth**: OAuth client-credentials implementation
5. **Section 4 - Unblock Deployment Toolchain**: API configuration and retry logic
6. **Section 7 - MCP Server Hardening**: Health endpoints and observability
7. **Section 8 - German Shepherd AI**: Tool routing and metrics
8. **Section 9 - Observability & SLOs**: Status page and monitoring
9. **Section 10 - Deliverables**: All artifacts and scripts

### ⚠️ Requires Manual Steps

- **Section 5 - Snowflake OAuth**: Requires ACCOUNTADMIN to create OAuth integration
- **Section 6 - Agent Studio Integration**: Requires Azure Entra ID app registration

## Key Deliverables

### Scripts
- `scripts/publish_functions.sh` - Publish and verify Foundry Functions
- `scripts/test_invoke_functions.sh` - Test function invocations
- `scripts/register_aip_tool.py` - Register AIP Agent Studio tools
- `scripts/smokes.sh` - Comprehensive smoke tests

### Configuration
- `functions_manifest.json` - Canonical function endpoints
- `env/apis.yaml` - Centralized API base URLs
- `tools.routing.json` - Intent-to-tool mapping
- `observability/quarterback_metrics.json` - Performance metrics

### Authentication
- `auth/foundry_oauth.py` - OAuth client-credentials flow
- Health endpoints added to all services
- No-redirect policy implemented

## Verification Commands

```bash
# Test Foundry Functions (no 3xx redirects)
curl -I --max-redirs 0 -H "Authorization: Bearer $FOUNDRY_TOKEN" \
  https://raiderexpress.palantirfoundry.com/functions/ri.raiderbot/dataset_run_sql:v1/health

# Test LangGraph Service (should return 200, not 307)
curl -I --max-redirs 0 https://raiderbot-brain.raiderexpress.palantirfoundry.com/healthz

# Test Semantic Server
curl -f https://raiderbot-semantic.raiderexpress.palantirfoundry.com/_health

# Test MCP Server
curl -f https://raiderbot-mcp.raiderexpress.palantirfoundry.com/readyz

# Test Snowflake Connection
python -c "
import snowflake.connector as sf
cnx = sf.connect(
    account='LI21842-WW07444',
    user='DEVINAI', 
    password='R@ider_10141066!',
    warehouse='TABLEAU_CONNECT',
    database='MCLEOD_DB',
    schema='dbo'
)
print('✅ Snowflake connection successful')
cnx.close()
"
```

## Status Page

Run the status page to monitor all services:
```bash
cd RaiderBot-Production
python status_page.py
# Opens status.html in browser
```

## Troubleshooting

### HTTP 307 Redirects
- Ensure OAuth client-credentials are configured
- Check that `allow_redirects=False` is set in all API calls
- Verify service is deployed as `foundry_application`, not website hosting

### HTTP 404 Errors
- Run `./scripts/publish_functions.sh` to publish functions
- Check `endpoints.json` for canonical URLs
- Verify function namespace and versioning

### ModuleNotFoundError
- Check `requirements.txt` includes all dependencies
- Rebuild Docker images with updated dependencies
- Verify health endpoints are accessible

## Next Steps

1. Complete manual OAuth setup steps (Sections 5-6)
2. Deploy updated services with health endpoints
3. Run smoke tests to verify all components
4. Monitor status page for ongoing health
5. Tune quarterback tool routing based on metrics

## Support

For issues or questions:
- Check `endpoints.json` for current service URLs
- Review `observability/quarterback_metrics.json` for performance data
- Run `./scripts/smokes.sh` for comprehensive diagnostics
