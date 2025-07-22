# RaiderBot - Enterprise AI Platform with Palantir Foundry Integration

## 🚀 What's New: "Build This Out" Natural Language Automation
Transform ideas into production Foundry applications with simple commands:
- **"Build me a fuel cost dashboard"** → Complete Workshop app in 5 minutes
- **"Create TMS performance tracker"** → Automated pipelines + visualizations  
- **"Set up daily revenue reports"** → Scheduled workflows with alerts

## 📚 Documentation

- 🎯 **[User Guide](./USER_GUIDE.md)** - How to use RaiderBot (start here!)
- 🏗️ **[Foundry Integration](./FOUNDRY_README.md)** - Technical details about Foundry automation
- 🚀 **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - How to deploy to cloud
- 👥 **[Team Setup](./TEAM_SETUP_GUIDE.md)** - Onboarding new team members
- 📝 **[Devin Handoff](./DEVIN_HANDOFF.md)** - Final deployment checklist for Devin

## 🎯 Quick Start

### For Users:
1. Open Claude Desktop
2. Say: "Build me a dashboard showing today's orders"
3. Watch RaiderBot create it automatically!

### For Developers:
```bash
# Clone the repository
git clone [your-repo-url]
cd RaiderBot-Cursor-Deploy

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
nano .env  # Add your credentials
# Important: keep this file out of Git. Credentials must never be committed.

# Run tests before deploying
python run_comprehensive_tests.py

# Deploy
python3 deployment/deploy.py
```

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Desktop │────▶│   RaiderBot API  │────▶│ Palantir Foundry│
│  (Natural Lang) │     │   (Python/MCP)   │     │  (AIP/Workshop) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                        │                         │
         │                        ▼                         ▼
         │              ┌──────────────────┐      ┌─────────────────┐
         └─────────────▶│    Snowflake     │      │   Tableau/BI    │
                        │   (Data Source)  │      │ (Visualizations)│
                        └──────────────────┘      └─────────────────┘
```

## 🔧 Core Components

### 1. **MCP Server** (`server.py`)
- Snowflake data access
- Natural language processing
- Foundry automation integration

### 2. **Foundry Automation** (`src/foundry/`)
- AIP Agent configuration
- Machinery workflow automation
- Workshop app generation

### 3. **Web Interface** (`web_dashboard.html`)
- Visual query builder
- Real-time results
- Export capabilities

### 4. **Deployment** (`deployment/`)
- Cloud deployment scripts
- Docker configuration
- Health monitoring

## 💡 Key Features

### Natural Language to Applications
- ✅ Understand business intent
- ✅ Generate complete applications
- ✅ Deploy automatically
- ✅ No coding required

### Data Integration
- ✅ Direct Snowflake queries
- ✅ 499K+ orders accessible
- ✅ Real-time data sync
- ✅ Multi-source support

### Enterprise Ready
- ✅ Role-based access control
- ✅ Audit logging
- ✅ Error handling
- ✅ Scalable architecture

## 🎨 Usage Examples

### Through Claude Desktop:
```
You: Build a dashboard for fuel costs by month
Claude: I'll create that dashboard for you using RaiderBot...
[Creates complete application]
Claude: Your dashboard is ready at: [link]
```

### Through Foundry Workshop:
1. Open RaiderBot Build Console
2. Type: "Create customer analysis tool"
3. Click "Build It!"
4. Access your new application

### Through API:
```python
from raiderbot import build_this_out

result = build_this_out("Create revenue tracking dashboard")
print(f"Application ready at: {result['deployment']['url']}")
```

## 📊 Available Data

### Snowflake Tables:
- **ORDERS**: 499K+ transportation orders
- **CUSTOMERS**: Customer master data
- **FUEL_RECEIPTS**: Fuel cost tracking
- **REVENUE**: Financial metrics

### Quick Queries:
- TMS vs TMS2 comparison
- Top customers by revenue
- Daily order volumes
- Fuel cost trends

## 🚀 Deployment Status

### Production Environment:
- **API**: https://raiderbot-production.up.railway.app
- **Foundry**: https://raiderexpress.palantirfoundry.com
- **Workshop**: /workshop/raiderbot-build-console

### Available Tools:
- ✅ `search_orders` - Natural language order search
- ✅ `revenue_summary` - Revenue analytics
- ✅ `analyze_customer` - Customer insights
- ✅ `sql_query` - Direct SQL access
- ✅ `build_this_out` - Foundry automation

## 🔒 Security

- Environment-based credentials
- Read-only Snowflake access
- OAuth 2.0 for Foundry
- Encrypted connections
- Audit trail logging

## 📈 Performance

- **Response Time**: <2 seconds for queries
- **Build Time**: 3-5 minutes for applications  
- **Concurrent Users**: 100+
- **Uptime**: 99.9% SLA

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Submit pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 📞 Support

- **Slack**: #raiderbot-support
- **Email**: raiderbot@raiderexpress.com
- **Wiki**: [Internal documentation]
- **Issues**: [GitHub Issues]

## 🎯 Roadmap

- [ ] Voice command support
- [ ] Mobile app builder
- [ ] Advanced ML pipelines
- [ ] Multi-language support
- [ ] Custom widget library

## 📄 License

Proprietary - Raider Express Internal Use Only

---

**Built with ❤️ by the RaiderBot Team**

*Turning transportation data into actionable insights*
