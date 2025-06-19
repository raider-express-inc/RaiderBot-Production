# 🚀 RaiderBot User Guide - "Build This Out" Automation

## What is RaiderBot?
RaiderBot is your AI-powered automation assistant that transforms natural language requests into production Palantir Foundry applications in minutes.

## 🎯 Two Ways to Use RaiderBot

### Method 1: Through Claude Desktop (Natural Language)
Perfect for quick builds and conversational interaction.

#### How to Use:
1. Open Claude Desktop
2. Ask RaiderBot to build something:
   ```
   Build me a fuel cost dashboard
   ```
   ```
   Create a TMS performance tracker with revenue metrics
   ```
   ```
   Set up automated daily reports for customer orders
   ```

#### Example Conversation:
```
You: Build me a dashboard showing TMS vs TMS2 performance
Claude: I'll create that dashboard for you using the build_this_out tool...
[RaiderBot creates Workshop app, connects data, deploys]
Claude: ✅ Your dashboard is ready at: https://raiderexpress.palantirfoundry.com/workshop/tms-comparison
```

### Method 2: Directly in Palantir Foundry
Perfect for power users and integrated workflows.

#### Access Points:
1. **Workshop Build Console**: https://raiderexpress.palantirfoundry.com/workshop/raiderbot-build-console
2. **AIP Agent Studio**: Find "RaiderBot Enterprise Builder"
3. **Machinery Workflows**: Access pre-built automation patterns

#### How to Use in Workshop:
1. Navigate to the RaiderBot Build Console
2. Type your request in the input box
3. Click "Build It!" or press Enter
4. Watch the real-time progress
5. Access your new application when complete

## 📋 What Can You Build?

### Dashboards
```
"Build a fuel cost analysis dashboard"
"Create executive revenue dashboard with YoY comparisons"
"Make a real-time order tracking dashboard"
```

### Reports
```
"Set up daily revenue summary reports"
"Create weekly customer analysis report"
"Build monthly TMS performance report"
```

### Data Pipelines
```
"Create pipeline to process fuel receipts"
"Build automated data flow from Snowflake to Foundry"
"Set up hourly order data sync"
```

### Automation Workflows
```
"Automate customer alerts for delayed shipments"
"Create workflow for daily metrics calculation"
"Build approval process for high-value orders"
```

## 🎨 Quick Action Templates

### TMS Dashboard
- **What it builds**: Complete transportation management dashboard
- **Includes**: Order tracking, revenue metrics, performance KPIs
- **Command**: "Build TMS operations dashboard"

### Customer 360
- **What it builds**: Comprehensive customer view
- **Includes**: Order history, revenue trends, satisfaction metrics
- **Command**: "Create customer 360 view"

### Fuel Cost Tracker
- **What it builds**: Fuel expense monitoring system
- **Includes**: Cost trends, efficiency metrics, alerts
- **Command**: "Build fuel cost tracking system"

## 💡 Pro Tips

### Be Specific
❌ "Build a dashboard"
✅ "Build a dashboard showing today's orders by customer with revenue totals"

### Include Time Frames
❌ "Show me revenue"
✅ "Show me revenue for the last 30 days compared to previous period"

### Mention Data Sources
❌ "Create customer report"
✅ "Create customer report using ORDERS and CUSTOMERS tables from Snowflake"

### Request Features
❌ "Make it interactive"
✅ "Add filters for date range, customer, and company (TMS/TMS2)"

## 🔧 Advanced Features

### Branching for Safe Development
All builds automatically:
- Create isolated development branch
- Run tests before merging
- Provide rollback capability

### Monitoring & Alerts
Every application includes:
- Health checks
- Performance monitoring
- Error alerting
- Usage analytics

### Integration Points
Your builds can connect to:
- Snowflake databases
- Tableau dashboards
- Email systems
- Slack channels
- External APIs

## 🚨 Troubleshooting

### "Build Failed"
- Check data permissions
- Verify table/column names
- Review error details in log

### "Cannot Connect to Data"
- Ensure Snowflake credentials are valid
- Check network connectivity
- Verify data source exists

### "Application Not Loading"
- Clear browser cache
- Check Workshop permissions
- Try different browser

## 📊 Example Builds

### Example 1: Executive Dashboard
```
Request: "Build executive dashboard with daily revenue, top 10 customers, and TMS comparison"

Result:
- Workshop application with 3 pages
- Auto-refreshing every hour
- Mobile-responsive design
- Email summary option
```

### Example 2: Operational Alerts
```
Request: "Create alerts for orders delayed more than 2 days"

Result:
- Automated monitoring workflow
- Slack notifications
- Daily summary email
- Drill-down investigation tools
```

### Example 3: Customer Analysis
```
Request: "Build customer churn prediction model with visualization"

Result:
- ML pipeline for churn scoring
- Interactive customer list
- Risk visualization
- Intervention recommendations
```

## 🎯 Best Practices

1. **Start Simple**: Begin with basic dashboards, then add complexity
2. **Iterate Quickly**: Use "update my dashboard to add..." for modifications
3. **Test First**: All builds are tested in isolation before production
4. **Monitor Usage**: Check analytics to see how your apps are used
5. **Share Knowledge**: Save successful patterns for team reuse

## 📞 Getting Help

### In Claude Desktop:
```
"Help me understand what I can build"
"Show me examples of dashboards"
"What data sources are available?"
```

### In Foundry:
- Click "?" icon in Build Console
- Check Machinery process library
- Review AIP Agent capabilities

### Support Channels:
- Slack: #raiderbot-support
- Email: raiderbot@raiderexpress.com
- Wiki: [Internal Wiki Link]

## 🚀 Start Building!

Ready to transform your ideas into applications? Just describe what you need, and RaiderBot will build it for you!

**Remember**: If you can describe it, RaiderBot can build it! 🎉