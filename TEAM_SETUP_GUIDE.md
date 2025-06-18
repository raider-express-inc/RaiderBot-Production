# RaiderBot Team Setup Guide
## Connect Your Team to RaiderBot Business Intelligence

**RaiderBot Cloud Server**: https://raiderbot-production-production.up.railway.app

---

## 🚀 Quick Setup for Team Members (5 minutes)

### **Step 1: Install Claude Desktop**
1. Download from: https://claude.ai/desktop
2. Install and sign in with your account

### **Step 2: Download RaiderBot Wrapper**
```bash
# Download the wrapper script
curl -o ~/raiderbot_wrapper.py https://raw.githubusercontent.com/raider-express-inc/RaiderBot-Production/main/claude_desktop_wrapper.py

# Make it executable
chmod +x ~/raiderbot_wrapper.py
```

### **Step 3: Update Claude Desktop Config**

**Mac/Linux**: Edit this file:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**: Edit this file:
```
%APPDATA%/Claude/claude_desktop_config.json
```

**Add this to your mcpServers section:**
```json
{
  "mcpServers": {
    "raiderbot-cloud": {
      "command": "python3",
      "args": ["~/raiderbot_wrapper.py"]
    }
  }
}
```

### **Step 4: Restart Claude Desktop**
- **Quit completely** (⌘+Q on Mac)
- **Reopen** Claude Desktop
- **Start new conversation**

### **Step 5: Test RaiderBot**
Ask: **"Show me TMS vs TMS2 orders today"**

**Expected Response:**
```json
{
  "company_name": "Raider Logistics (Brokerage)",
  "total_orders": 14350+,
  "recent_orders": 10+,
  "today_orders": 2+
}
```

---

## 🎯 Available Queries

### **Operations Queries:**
- "Show me TMS vs TMS2 orders today"
- "What's our revenue summary for this week?"
- "Who are our top 10 customers?"

### **Custom Analysis:**
- "Run this SQL: SELECT COUNT(*) FROM ORDERS WHERE COMPANY_ID = 'TMS2'"
- "Show me fuel costs for last month"
- "Check driver performance metrics"

---

## 🔧 Troubleshooting

### **If RaiderBot doesn't appear:**
1. **Check config file syntax** (valid JSON)
2. **Restart Claude Desktop** completely
3. **Start new conversation** (tools load per conversation)
4. **Verify wrapper script** is executable

### **If queries fail:**
1. **Check internet connection**
2. **Verify cloud server** is running
3. **Contact IT** if persistent issues

---

## 👥 Team Roles & Access

### **Executives** 
- Full access to all business intelligence
- Strategic queries and analysis
- Cross-divisional comparisons

### **Managers**
- Departmental performance metrics
- Operational insights
- Customer analytics

### **Analysts**
- Custom SQL queries
- Detailed reporting
- Data exploration

---

## 🚨 Security Notes

- **No sensitive data** stored locally
- **All queries** go through secure cloud server
- **Audit trail** maintained for compliance
- **Read-only access** to prevent data modification

---

## 📞 Support

**Issues or Questions?**
- **IT Support**: Contact Dan Eggleton
- **Feature Requests**: Submit via GitHub issues
- **Training**: Available upon request

**RaiderBot Server Status**: https://raiderbot-production-production.up.railway.app/health

---

*RaiderBot: Real-time business intelligence for Raider Express operations*