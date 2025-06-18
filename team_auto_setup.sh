#!/bin/bash

# RaiderBot Team Auto-Setup Script
# Automatically configures Claude Desktop for RaiderBot access

echo "🚀 RaiderBot Team Setup - Raider Express"
echo "======================================="

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS="Mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/claude"
    OS="Linux"
else
    echo "❌ Unsupported operating system"
    exit 1
fi

echo "📍 Detected OS: $OS"
echo "📁 Config directory: $CONFIG_DIR"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Download wrapper script
echo "📥 Downloading RaiderBot wrapper..."
curl -s -o "$HOME/raiderbot_wrapper.py" https://raw.githubusercontent.com/raider-express-inc/RaiderBot-Production/main/claude_desktop_wrapper.py

if [ $? -eq 0 ]; then
    chmod +x "$HOME/raiderbot_wrapper.py"
    echo "✅ Wrapper script downloaded and made executable"
else
    echo "❌ Failed to download wrapper script"
    exit 1
fi

# Create or update Claude Desktop config
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

if [ -f "$CONFIG_FILE" ]; then
    echo "📝 Backing up existing config..."
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create new config with RaiderBot
cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "raiderbot-cloud": {
      "command": "python3",
      "args": ["~/raiderbot_wrapper.py"]
    }
  }
}
EOF

echo "✅ Claude Desktop configuration updated"

# Test the wrapper script
echo "🧪 Testing RaiderBot connection..."
python3 "$HOME/raiderbot_wrapper.py" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ RaiderBot connection test successful"
else
    echo "⚠️ RaiderBot connection test failed (may still work in Claude Desktop)"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. 🔄 Restart Claude Desktop completely"
echo "2. 💬 Start a new conversation"
echo "3. 🧪 Test with: 'Show me TMS vs TMS2 orders today'"
echo ""
echo "Expected result: Real business data from Raider Express operations"
echo ""
echo "📞 Support: Contact Dan Eggleton for issues"
echo ""
echo "🏢 RaiderBot: Business Intelligence for Raider Express"
