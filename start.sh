#!/bin/bash

echo "🚀 Starting Comprehensive MCP Server Toolkit..."

mkdir -p ~/.devin/mcp-servers/{github-mcp,aws-mcp,slack-mcp,docker-mcp}
mkdir -p ~/.devin/logs

chmod +x ~/.devin/mcp-servers/*/server.py 2>/dev/null || true
chmod +x ~/.devin/orchestrator.py

echo "📡 Starting MCP servers..."

cd /home/ubuntu/repos/RaiderBot-Production
python server.py > ~/.devin/logs/snowflake-mcp.log 2>&1 &
echo "✅ Snowflake MCP server started"

cd /home/ubuntu/repos/raiderbot-foundry-functions/foundry-mcp-server
python server.py > ~/.devin/logs/foundry-mcp.log 2>&1 &
echo "✅ Foundry MCP server started"

python ~/.devin/mcp-servers/github-mcp/server.py > ~/.devin/logs/github-mcp.log 2>&1 &
echo "✅ GitHub MCP server started"

python ~/.devin/mcp-servers/aws-mcp/server.py > ~/.devin/logs/aws-mcp.log 2>&1 &
echo "✅ AWS MCP server started"

python ~/.devin/mcp-servers/slack-mcp/server.py > ~/.devin/logs/slack-mcp.log 2>&1 &
echo "✅ Slack MCP server started"

python ~/.devin/mcp-servers/docker-mcp/server.py > ~/.devin/logs/docker-mcp.log 2>&1 &
echo "✅ Docker MCP server started"

python ~/.devin/mcp-servers/zapier-mcp/server.py > ~/.devin/logs/zapier-mcp.log 2>&1 &
echo "✅ Zapier MCP server started"

cd /home/ubuntu/repos/raiderbot-platform/semantic-layer
python mcp_server_production.py > ~/.devin/logs/semantic-production.log 2>&1 &
echo "✅ Semantic Production MCP server started"

python mcp_server_with_memory.py > ~/.devin/logs/semantic-memory.log 2>&1 &
echo "✅ Semantic Memory MCP server started"

cd /home/ubuntu/repos/raiderbot-platform/mcp-enhanced-ai
python server.py > ~/.devin/logs/semantic-ai.log 2>&1 &
echo "✅ Semantic AI MCP server started"

echo "🎭 Starting master orchestrator..."
python ~/.devin/orchestrator.py --mode=autonomous > ~/.devin/logs/orchestrator.log 2>&1 &
echo "✅ Master orchestrator started"

echo "📊 Starting monitoring dashboard..."
cd /home/ubuntu/repos/raiderbot-foundry-functions
docker-compose up -d grafana prometheus > ~/.devin/logs/monitoring.log 2>&1
echo "✅ Monitoring dashboard available at http://localhost:3000"

echo ""
echo "🎉 Comprehensive MCP Toolkit is now running!"
echo "📊 Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "🎭 Orchestrator API: http://localhost:8080"
echo "📝 Logs: ~/.devin/logs/"
echo ""
echo "Use 'python ~/.devin/test_comprehensive_mcp.py' to run tests"
