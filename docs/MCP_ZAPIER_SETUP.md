# MCP Zapier Integration Setup Guide

## Overview
This guide explains how to set up Zapier MCP integration with the enhanced Snowflake client to enable automated workflows triggered by database queries.

## Prerequisites
- Enhanced Snowflake client with 100% connectivity (already configured)
- MCP integration layer (implemented in `src/mcp/mcp_snowflake_integration.py`)
- Zapier account with webhook capabilities

## Setup Steps

### 1. Configure Zapier MCP Server
Add Zapier MCP server to your MCP configuration:

```json
{
  "mcpServers": {
    "foundry-integration": {
      "command": "python",
      "args": ["./foundry-mcp-server/server.py"],
      "env": {
        "FOUNDRY_TOKEN": "${FOUNDRY_TOKEN}",
        "FOUNDRY_BASE_URL": "${FOUNDRY_BASE_URL}",
        "FOUNDRY_CLIENT_ID": "${FOUNDRY_CLIENT_ID}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    },
    "zapier-integration": {
      "command": "python",
      "args": ["-m", "mcp_zapier"],
      "env": {
        "ZAPIER_API_KEY": "${ZAPIER_API_KEY}",
        "ZAPIER_WEBHOOK_URL": "${ZAPIER_WEBHOOK_URL}"
      }
    }
  }
}
```

### 2. Environment Variables
Add to your `.env` file:

```bash
# Zapier MCP Configuration
MCP_ZAPIER_ENABLED=true
ZAPIER_API_KEY=your_zapier_api_key_here
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/your_webhook_id/
```

### 3. Test Integration
Run the MCP integration test:

```bash
python test_mcp_integration.py
```

## Usage Examples

### Trigger Zapier on Query Results
```python
from src.mcp.mcp_snowflake_integration import mcp_integration

# Execute query with Zapier automation
result = mcp_integration.natural_language_query_with_automation(
    "Show me orders with high priority",
    automation_config={
        'zapier_webhook': {
            'url': 'https://hooks.zapier.com/hooks/catch/your_id/',
            'trigger_condition': 'result_count > 10'
        }
    }
)
```

### Automated Notifications
```python
# Search orders and trigger notifications
result = mcp_integration.execute_with_mcp_integration(
    'SELECT * FROM "dbo"."orders" WHERE status = "urgent"',
    mcp_context={
        'trigger_zapier': True,
        'notification_type': 'urgent_orders'
    }
)
```

## Available Automation Triggers

1. **Query Result Thresholds**: Trigger when result count exceeds limits
2. **Data Value Conditions**: Trigger on specific field values
3. **Schedule-based**: Combine with cron for periodic automation
4. **Real-time Webhooks**: Immediate triggers on data changes

## Zapier Workflow Examples

1. **Order Alerts**: Snowflake query → Zapier → Slack notification
2. **Customer Updates**: Database change → Zapier → CRM update
3. **Report Generation**: Query results → Zapier → Email report
4. **Dashboard Sync**: Snowflake data → Zapier → Foundry dashboard update

## Troubleshooting

### Common Issues
- **Zapier not available**: Check MCP server configuration
- **Webhook failures**: Verify Zapier webhook URL and API key
- **Connectivity issues**: Ensure Snowflake client maintains 100% success rate

### Debug Commands
```bash
# Test MCP server discovery
python -c "from src.mcp.mcp_snowflake_integration import mcp_integration; print(mcp_integration.health_check_with_mcp())"

# Test Snowflake connectivity
python test_cortex_connectivity.py

# Full integration test
python test_mcp_integration.py
```

## Security Considerations
- Store API keys in environment variables, never in code
- Use webhook authentication when possible
- Limit Zapier webhook access to specific IP ranges
- Monitor automation triggers for unexpected behavior

## Next Steps
1. Configure your Zapier workflows
2. Test automation triggers with sample data
3. Monitor integration performance
4. Scale to additional MCP tools as needed
