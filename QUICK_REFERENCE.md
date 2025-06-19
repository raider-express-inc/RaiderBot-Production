# 🚀 RaiderBot Quick Reference Card

## 🎯 For End Users

### In Claude Desktop:
```
"Build me a fuel cost dashboard"
"Create TMS performance tracker"  
"Set up daily revenue reports"
"Show me today's orders"
```

### In Foundry Workshop:
1. Go to: https://raiderexpress.palantirfoundry.com/workshop/raiderbot-build-console
2. Type what you want
3. Click "Build It!"

## 🔧 For Developers

### Quick Commands:
```bash
# Start local environment
source venv/bin/activate

# Test automation
python3 src/foundry/automation_engine.py

# Deploy updates
python3 deployment/deploy.py

# Run server
python3 server.py
```

### Key Files:
- `server.py` - Main MCP server
- `src/foundry/automation_engine.py` - Build automation
- `.env` - Configuration (don't commit!)
- `deployment/deploy.py` - Deployment script

## 📊 Common Queries

### TMS Comparison:
```
"Compare TMS vs TMS2 performance"
"Show order volumes by division"
```

### Revenue Analysis:
```
"Revenue summary for last week"
"Top 10 customers by revenue"
```

### Operational:
```
"Today's order count"
"Delayed shipments alert"
```

## 🌐 URLs

- **Foundry**: https://raiderexpress.palantirfoundry.com
- **Workshop**: /workshop/raiderbot-build-console  
- **API**: https://raiderbot-production.up.railway.app
- **Snowflake**: RAIDER_DB.SQL_SERVER_DBO

## 🚨 Troubleshooting

### "Can't connect to Snowflake"
Check VPN connection and credentials in .env

### "Build failed"
Check Foundry permissions and data access

### "Command not found"
Activate virtual environment: `source venv/bin/activate`

## 📞 Get Help

- Slack: #raiderbot-support
- Lead: Dan Eggleton
- Docs: See USER_GUIDE.md