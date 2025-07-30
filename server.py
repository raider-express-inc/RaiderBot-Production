#!/usr/bin/env python3
"""
RaiderBot MCP Server - Cursor Cloud Production Version
Cloud-optimized with environment variables and production features
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# MCP imports
from mcp.server.fastmcp import FastMCP

# Enhanced Snowflake client with MCP integration
import sys
sys.path.append(os.path.dirname(__file__))
from src.snowflake.mcp_snowflake_client import mcp_snowflake_client as snowflake_client
from src.foundry.quarterback_functions import operations_agent, customer_service_agent, financial_agent, compliance_agent, knowledge_agent
from src.sema4.sema4_integration_service import sema4_integration
from src.mcp.mcp_snowflake_integration import mcp_integration

# Foundry automation imports
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from src.foundry.automation_engine import RaiderBotAutomationEngine, BuildRequest
    from src.aip.bot_integration_service import BotIntegrationService
    from src.aip.studio_deployment_service import AIPStudioDeploymentService
    from src.orchestrator.external_orchestrator_service import ExternalOrchestratorService
    from src.sema4.sema4_execution_service import Sema4ExecutionService
    from src.audit.snowflake_audit_service import SnowflakeAuditService, AuditEventType
    from src.dashboard.modern_dashboard_service import ModernDashboardService
    FOUNDRY_AUTOMATION_AVAILABLE = True
except ImportError as e:
    FOUNDRY_AUTOMATION_AVAILABLE = False

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = FastMCP("RaiderBot-Production")

# Initialize Foundry automation if available
foundry_engine = None
if FOUNDRY_AUTOMATION_AVAILABLE:
    try:
        foundry_config = {
            "FOUNDRY_URL": os.getenv('FOUNDRY_URL'),
            "FOUNDRY_CLIENT_ID": os.getenv('FOUNDRY_CLIENT_ID'),
            "FOUNDRY_CLIENT_SECRET": os.getenv('FOUNDRY_CLIENT_SECRET'),
            "FOUNDRY_AUTH_TOKEN": os.getenv('FOUNDRY_AUTH_TOKEN')
        }
        foundry_engine = RaiderBotAutomationEngine(foundry_config)
        bot_integration = BotIntegrationService(foundry_engine)
        studio_deployment = AIPStudioDeploymentService(foundry_engine.foundry_client)
        orchestrator = ExternalOrchestratorService(foundry_engine.foundry_client)
        sema4_service = Sema4ExecutionService(None)
        audit_service = SnowflakeAuditService(None)
        dashboard_service = ModernDashboardService(foundry_engine.foundry_client)
        
        logger.info("✅ All services initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Foundry automation: {e}")


@app.tool()
def multi_agent_query(query: str, agent_type: str = "auto") -> Dict[str, Any]:
    """
    Single interface for all employee inquiries with intelligent agent routing
    Implements platform specification: "One interface where any Raider Express employee can ask anything"
    """
    try:
        logger.info(f"Processing multi-agent query: {query} (agent_type: {agent_type})")
        
        result = sema4_integration.process_multi_agent_query(query, agent_type)
        
        result["platform_version"] = "2.0.0"
        result["interface_type"] = "single_agent_studio_interface"
        result["processing_location"] = "snowflake_native"
        
        return result
        
    except Exception as e:
        logger.error(f"Multi-agent query failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "agent_type": agent_type,
            "platform_version": "2.0.0"
        }

@app.tool()
def search_orders(query: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
    """Search for orders based on natural language query"""
    try:
        logger.info(f"🔍 Processing search query: {query}")
        
        # Handle TMS vs TMS2 comparison specifically
        if "TMS" in query.upper() and ("VS" in query.upper() or "VERSUS" in query.upper()):
            sql_query = """
            SELECT 
                COMPANY_ID,
                COUNT(*) as order_count,
                COUNT(CASE WHEN ORDERED_DATE >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as recent_orders,
                COUNT(CASE WHEN ORDERED_DATE >= CURRENT_DATE() THEN 1 END) as today_orders
            FROM ORDERS 
            WHERE COMPANY_ID IN ('TMS', 'TMS2')
            GROUP BY COMPANY_ID 
            ORDER BY order_count DESC
            """
        else:
            # General order search - today's orders
            sql_query = """
            SELECT 
                COMPANY_ID,
                CUSTOMER_ID,
                ORDERED_DATE,
                BILL_DATE
            FROM ORDERS 
            WHERE DATE(ORDERED_DATE) = CURRENT_DATE()
            ORDER BY ORDERED_DATE DESC
            LIMIT 50
            """
        
        results = snowflake_client.execute_query(sql_query)["rows"]
        
        # Format results with business context
        if "TMS" in query.upper() and ("VS" in query.upper() or "VERSUS" in query.upper()):
            formatted_results = []
            for row in results:
                company_name = "Raider Express (Trucking)" if row['COMPANY_ID'] == 'TMS' else "Raider Logistics (Brokerage)"
                formatted_results.append({
                    "company_id": row['COMPANY_ID'],
                    "company_name": company_name,
                    "total_orders": int(row['ORDER_COUNT']) if row['ORDER_COUNT'] else 0,
                    "recent_orders": int(row['RECENT_ORDERS']) if row['RECENT_ORDERS'] else 0,
                    "today_orders": int(row['TODAY_ORDERS']) if row['TODAY_ORDERS'] else 0
                })
            
            return {
                "query": query,
                "comparison_type": "TMS vs TMS2",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "results": formatted_results,
                "summary": f"Company comparison: {len(formatted_results)} divisions analyzed",
                "generated_at": datetime.now().isoformat()
            }
        else:
            return {
                "query": query,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "results": results[:20],  # Limit for readability
                "total_found": len(results),
                "summary": f"Found {len(results)} orders for today",
                "generated_at": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"❌ search_orders failed: {e}")
        return {
            "error": str(e), 
            "query": query,
            "generated_at": datetime.now().isoformat()
        }

@app.tool()
def revenue_summary(timeframe: str = "week") -> Dict[str, Any]:
    """Get revenue summary for specified timeframe"""
    try:
        logger.info(f"📊 Generating revenue summary for: {timeframe}")
        
        # Calculate date range based on timeframe
        if timeframe.lower() == "week":
            date_filter = "DATE(ORDERED_DATE) >= DATEADD(day, -7, CURRENT_DATE())"
            period_desc = "Last 7 Days"
        elif timeframe.lower() == "month":
            date_filter = "DATE(ORDERED_DATE) >= DATEADD(day, -30, CURRENT_DATE())"
            period_desc = "Last 30 Days"
        elif timeframe.lower() == "today":
            date_filter = "DATE(ORDERED_DATE) = CURRENT_DATE()"
            period_desc = "Today"
        else:
            date_filter = "DATE(ORDERED_DATE) >= DATEADD(day, -7, CURRENT_DATE())"
            period_desc = "Last 7 Days"
        
        query = f"""
        SELECT 
            COMPANY_ID,
            COUNT(*) as order_count,
            MIN(ORDERED_DATE) as earliest_order,
            MAX(ORDERED_DATE) as latest_order
        FROM ORDERS 
        WHERE {date_filter}
        GROUP BY COMPANY_ID
        ORDER BY order_count DESC
        """
        
        results = snowflake_client.execute_query(query)["rows"]
        
        # Calculate totals and add business context
        total_orders = sum(int(row['ORDER_COUNT']) if row['ORDER_COUNT'] else 0 for row in results)
        
        # Add company names
        formatted_results = []
        for row in results:
            company_name = "Raider Express (Trucking)" if row['COMPANY_ID'] == 'TMS' else "Raider Logistics (Brokerage)"
            formatted_results.append({
                "company_id": row['COMPANY_ID'],
                "company_name": company_name,
                "order_count": int(row['ORDER_COUNT']) if row['ORDER_COUNT'] else 0,
                "earliest_order": str(row['EARLIEST_ORDER']) if row['EARLIEST_ORDER'] else None,
                "latest_order": str(row['LATEST_ORDER']) if row['LATEST_ORDER'] else None
            })
        
        return {
            "timeframe": timeframe,
            "period_description": period_desc,
            "total_orders": total_orders,
            "companies": formatted_results,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ revenue_summary failed: {e}")
        return {
            "error": str(e), 
            "timeframe": timeframe,
            "generated_at": datetime.now().isoformat()
        }

@app.tool()
def analyze_customer(analysis_type: str = "top_customers", limit: int = 10) -> Dict[str, Any]:
    """Analyze customer data"""
    try:
        logger.info(f"👥 Analyzing customers: {analysis_type}")
        
        if analysis_type == "top_customers":
            query = f"""
            SELECT 
                CUSTOMER_ID,
                COUNT(*) as order_count,
                MAX(ORDERED_DATE) as last_order_date
            FROM ORDERS 
            WHERE DATE(ORDERED_DATE) >= DATEADD(day, -30, CURRENT_DATE())
                AND CUSTOMER_ID IS NOT NULL
            GROUP BY CUSTOMER_ID
            ORDER BY order_count DESC
            LIMIT {limit}
            """
        else:
            query = f"""
            SELECT 
                CUSTOMER_ID,
                COUNT(*) as order_count,
                MAX(ORDERED_DATE) as last_order_date
            FROM ORDERS 
            WHERE CUSTOMER_ID IS NOT NULL
            GROUP BY CUSTOMER_ID
            ORDER BY order_count DESC
            LIMIT {limit}
            """
        
        results = snowflake_client.execute_query(query)["rows"]
        
        return {
            "analysis_type": analysis_type,
            "limit": limit,
            "period": "Last 30 Days",
            "results": results,
            "total_customers_analyzed": len(results),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ analyze_customer failed: {e}")
        return {
            "error": str(e), 
            "analysis_type": analysis_type,
            "generated_at": datetime.now().isoformat()
        }

@app.tool()
def sql_query(query: str) -> Dict[str, Any]:
    """Execute custom SQL query (SELECT only for security)"""
    try:
        logger.info(f"💻 Executing custom SQL query")
        
        # Security check - only allow SELECT queries
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            return {
                "error": "Only SELECT queries are allowed for security reasons",
                "query": query,
                "generated_at": datetime.now().isoformat()
            }
        
        # Prevent potentially dangerous operations
        dangerous_keywords = ['DELETE', 'UPDATE', 'INSERT', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE']
        if any(keyword in query_upper for keyword in dangerous_keywords):
            return {
                "error": "Query contains potentially dangerous operations",
                "query": query,
                "generated_at": datetime.now().isoformat()
            }
        
        results = snowflake_client.execute_query(query)["rows"]
        
        return {
            "query": query,
            "row_count": len(results),
            "results": results[:100],  # Limit results for performance
            "executed_at": datetime.now().isoformat(),
            "note": "Results limited to 100 rows for performance" if len(results) > 100 else None
        }
        
    except Exception as e:
        logger.error(f"❌ sql_query failed: {e}")
        return {
            "error": str(e), 
            "query": query,
            "generated_at": datetime.now().isoformat()
        }

@app.tool()
def build_this_out(request: str, user_id: str = "default_user") -> Dict[str, Any]:
    """Build Foundry applications from natural language requests with workbook visualization"""
    try:
        logger.info(f"🏗️ Processing build request: {request}")
        
        if not foundry_engine:
            return {
                "error": "Foundry automation not available",
                "suggestion": "Please configure Foundry credentials in .env file",
                "generated_at": datetime.now().isoformat()
            }
        
        if bot_integration and any(cmd in request.lower() for cmd in bot_integration.command_mappings.keys()):
            import asyncio
            
            command = next((cmd for cmd in bot_integration.command_mappings.keys() if cmd in request.lower()), "general")
            
            try:
                loop = asyncio.get_running_loop()
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, bot_integration.process_bot_command(command, user_id))
                    result = future.result()
            except RuntimeError:
                result = asyncio.run(bot_integration.process_bot_command(command, user_id))
            
            return {
                "request": request,
                "command": command,
                "user_id": user_id,
                "success": result["success"],
                "workbook_instructions": result.get("artifacts", []),
                "bot_response": result.get("bot_response", ""),
                "generated_at": datetime.now().isoformat()
            }
        
        import uuid
        build_request = BuildRequest(
            id=str(uuid.uuid4()),
            user_id=user_id,
            natural_language_request=request
        )
        
        import asyncio
        
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, foundry_engine.process_build_request(build_request))
                result = future.result()
        except RuntimeError:
            result = asyncio.run(foundry_engine.process_build_request(build_request))
        
        return {
            "request": request,
            "build_id": build_request.id,
            "user_id": user_id,
            "success": result["success"],
            "artifacts": result.get("artifacts", []),
            "deployment": result.get("deployment", {}),
            "errors": result.get("errors", []),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ build_this_out failed: {e}")
        return {
            "error": str(e),
            "request": request,
            "generated_at": datetime.now().isoformat()
        }

@app.tool()
def operations_query(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Operations Agent: Load planning, driver assignments, route optimization"""
    try:
        result = operations_agent(query, context)
        result["sema4_enhanced"] = sema4_integration.process_multi_agent_query(query, "operations")
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "agent_type": "operations"}

@app.tool()
def customer_service_query(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Customer Service Agent: Shipment tracking, delivery updates, customer inquiries"""
    try:
        result = customer_service_agent(query, context)
        result["sema4_enhanced"] = sema4_integration.process_multi_agent_query(query, "customer_service")
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "agent_type": "customer_service"}

@app.tool()
def financial_query(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Financial Agent: Revenue reporting, cost analysis, pricing decisions"""
    try:
        result = financial_agent(query, context)
        result["sema4_enhanced"] = sema4_integration.process_multi_agent_query(query, "financial")
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "agent_type": "financial"}

@app.tool()
def compliance_query(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Compliance Agent: DOT regulations, safety compliance, maintenance schedules"""
    try:
        result = compliance_agent(query, context)
        result["sema4_enhanced"] = sema4_integration.process_multi_agent_query(query, "compliance")
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "agent_type": "compliance"}

@app.tool()
def knowledge_query(query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Knowledge Agent: Company policies, procedures, historical decisions"""
    try:
        result = knowledge_agent(query, context)
        result["sema4_enhanced"] = sema4_integration.process_multi_agent_query(query, "knowledge")
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "agent_type": "knowledge"}

@app.tool()
def platform_health_check() -> Dict[str, Any]:
    """Health check for multi-agent platform following platform specifications"""
    try:
        snowflake_health = snowflake_client.execute_query("SELECT CURRENT_TIMESTAMP() as health_check_time")
        
        sema4_health = sema4_integration._check_sema4_availability()
        
        agent_health = {}
        for agent_type in ["operations", "customer_service", "financial", "compliance", "knowledge"]:
            try:
                test_result = sema4_integration.process_multi_agent_query(f"test {agent_type} agent", agent_type)
                agent_health[agent_type] = test_result.get("success", False)
            except:
                agent_health[agent_type] = False
        
        return {
            "platform_status": "healthy" if snowflake_health["success"] else "degraded",
            "snowflake_connected": snowflake_health["success"],
            "sema4_available": sema4_health,
            "agent_health": agent_health,
            "platform_version": "2.0.0",
            "architecture": "single_interface_multi_agent",
            "processing_method": "sema4_ai_native_snowflake",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "platform_status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Production startup
    logger.info("🚀 Starting RaiderBot MCP Server (Production)")
    logger.info(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    
    # Test Snowflake connection on startup
    try:
        test_result = snowflake_client.execute_query("SELECT CURRENT_TIMESTAMP() as test_time")
        if test_result["success"]:
            logger.info("✅ Snowflake connection established")
            logger.info(f"✅ Connected to unified Snowflake client")
        else:
            logger.error(f"❌ Failed to connect to Snowflake: {test_result['error']}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Snowflake: {e}")
    
    # Start production server
    logger.info("🌐 Starting MCP server...")
    
    # Run as HTTP server for cloud deployment
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
