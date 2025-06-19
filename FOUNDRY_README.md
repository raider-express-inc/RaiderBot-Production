# RaiderBot Foundry Enterprise Automation 🚀

## "Build This Out" - Natural Language to Production Applications

Transform your ideas into Foundry applications with simple commands like:
- "Build me a fuel cost dashboard"
- "Create a TMS performance tracker"
- "Set up automated revenue reports"

## 🎯 Architecture Overview

```
User Request → RaiderBot → AIP Agent → Foundry Automation → Deployed App
     ↓                         ↓              ↓                    ↓
"Build this"          Understands      Creates safely      Ready in 5 min
```

## 🚀 Quick Start

### 1. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your Foundry credentials
nano .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Deploy to Foundry
```bash
python deployment/deploy.py
```

### 4. Start Using
- Open Foundry Workshop
- Find "RaiderBot Build Console"
- Type: "Build me a dashboard for today's orders"
- Watch it build automatically!

## 🏗️ What Gets Built

### From Natural Language:
- **Workshop Applications** - Full interactive dashboards
- **Data Pipelines** - Automated data transformations
- **Ontology Objects** - Business entities and relationships
- **Automation Workflows** - Scheduled tasks and alerts
- **Reports** - Executive summaries and analytics
- **Visualizations** - Charts, graphs, and metrics

### Example Commands:
```
"Build a dashboard showing TMS vs TMS2 performance"
→ Creates complete Workshop app with:
  - Real-time order tracking
  - Comparative metrics
  - Interactive filters
  - Automated refresh

"Set up daily revenue reports"
→ Creates:
  - Scheduled pipeline
  - Email automation
  - PDF generation
  - Historical tracking

"Create customer analysis tool"
→ Builds:
  - Customer ontology
  - Analysis workflows
  - Interactive explorer
  - Predictive insights
```

## 🔧 Configuration

### Foundry Credentials
Get from Developer Console:
- Client ID
- Client Secret
- Stack URL
- Workspace RID

### AIP Agent Studio
1. Open Agent Studio in Foundry
2. Import `src/aip/agent_config.py`
3. Publish as Function
4. Note the Function RID

### Machinery Processes
1. Open Machinery in Foundry
2. Import processes from `src/foundry/machinery_config.py`
3. Activate automation workflows

## 📊 Architecture Components

### 1. Automation Engine (`src/foundry/automation_engine.py`)
- Interprets natural language requests
- Plans build sequences
- Manages safe branching
- Handles deployment

### 2. AIP Agent (`src/aip/`)
- Natural language understanding
- Build plan generation
- Context awareness
- Learning from usage

### 3. Machinery Workflows (`src/foundry/machinery_config.py`)
- Pre-built automation patterns
- Common build templates
- Process orchestration
- Error handling

### 4. Deployment System (`deployment/`)
- Automated CI/CD
- Branch management
- Testing framework
- Rollback capability

## 🎨 User Interface

### Workshop Widget
```html
<!-- Auto-generated in raiderbot_build_console.html -->
<div class="raiderbot-builder">
  <input type="text" placeholder="Tell me what to build...">
  <button onclick="buildThisOut()">Build It!</button>
</div>
```

### Quick Actions
- 🚛 TMS Dashboard
- 💰 Revenue Tracker
- 👥 Customer Analysis
- ⛽ Fuel Cost Monitor
- 📊 Performance Metrics

## 🔒 Security & Governance

### Branch Protection
- All builds start in isolated branches
- Automated testing before merge
- Approval workflows available
- Full audit trail

### Access Control
- Role-based permissions
- Workspace isolation
- Data access policies
- Compliance tracking

## 📈 Monitoring

### Health Checks
```python
# Check system status
python deployment/health_check.py
```

### Metrics Dashboard
- Build success rate
- Average build time
- User satisfaction
- Resource utilization

## 🤝 Integration Points

### With Existing RaiderBot
- Snowflake queries feed into builds
- Chat interface for requests
- Unified API endpoints
- Shared authentication

### With Other Systems
- Tableau dashboards
- Email notifications
- Slack alerts
- External APIs

## 🐛 Troubleshooting

### Common Issues

1. **"Foundry automation not available"**
   - Check .env configuration
   - Verify credentials
   - Test connection: `python deployment/test_connection.py`

2. **"Build failed"**
   - Check branch permissions
   - Verify data access
   - Review build logs

3. **"Agent not responding"**
   - Restart AIP Agent
   - Check Agent Studio
   - Verify Function deployment

## 📚 Advanced Usage

### Custom Build Types
```python
# Add to automation_engine.py
BuildType.CUSTOM_REPORT = "custom_report"
```

### Extend Machinery Processes
```python
# Add to machinery_config.py
"custom_workflow": {
    "name": "Custom Process",
    "steps": [...]
}
```

## 🎯 Roadmap

- [ ] GPT-4 integration for better understanding
- [ ] Multi-language support
- [ ] Mobile app builder
- [ ] Advanced ML pipelines
- [ ] Voice command support

## 📞 Support

- Internal Wiki: [Your Wiki URL]
- Slack: #raiderbot-support
- Email: raiderbot@yourcompany.com

---

**Built with ❤️ by the RaiderBot Team**

*Turning ideas into applications at the speed of thought*