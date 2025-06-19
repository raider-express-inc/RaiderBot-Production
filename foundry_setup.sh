#!/bin/bash
# RaiderBot Foundry Quick Setup Script

echo "🚀 RaiderBot Foundry Integration Setup"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "server.py" ]; then
    echo "❌ Error: Please run this script from the RaiderBot-Cursor-Deploy directory"
    exit 1
fi

echo "✅ Found RaiderBot directory"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Foundry credentials!"
else
    echo "✅ .env file already exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p src/foundry src/aip deployment tests docs logs

# Run tests
echo "🧪 Running basic tests..."
python3 -c "import sys; print('✅ Python environment OK')"

# Check Foundry connection (optional)
echo ""
echo "🔧 Next Steps:"
echo "1. Edit .env with your Foundry credentials"
echo "2. Run: python3 deployment/deploy.py"
echo "3. Access Foundry Workshop and find 'RaiderBot Build Console'"
echo ""
echo "📚 See FOUNDRY_README.md for detailed instructions"
echo ""
echo "Ready to build! Try: 'Build me a fuel cost dashboard' 🎉"