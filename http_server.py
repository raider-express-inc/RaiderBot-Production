#!/usr/bin/env python3
"""
RaiderBot HTTP Server - Cloud Deployment Version
Simple HTTP wrapper around MCP functionality for Railway deployment
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from flask import Flask, request, jsonify

# Enhanced Snowflake client
import sys
sys.path.append(os.path.dirname(__file__))
from src.snowflake.cortex_analyst_client import cortex_client

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Snowflake client is now imported from enhanced cortex_analyst_client

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        result = cortex_client.execute_query("SELECT CURRENT_USER(), CURRENT_WAREHOUSE(), CURRENT_DATABASE()")
        return jsonify({
            "status": "healthy",
            "user": result[0]["CURRENT_USER()"] if result else None,
            "warehouse": result[0]["CURRENT_WAREHOUSE()"] if result else None,
            "database": result[0]["CURRENT_DATABASE()"] if result else None,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/search_orders', methods=['POST'])
def search_orders():
    """Search orders endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        logger.info(f"🔍 Processing search query: {query}")
        
        # Handle TMS vs TMS2 comparison
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
        
        results = cortex_client.execute_query(sql_query)
        
        # Format results
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
            
            return jsonify({
                "query": query,
                "comparison_type": "TMS vs TMS2",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "results": formatted_results,
                "summary": f"Company comparison: {len(formatted_results)} divisions analyzed"
            })
        else:
            return jsonify({
                "query": query,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "results": results[:20],
                "total_found": len(results),
                "summary": f"Found {len(results)} orders"
            })
        
    except Exception as e:
        logger.error(f"❌ search_orders failed: {e}")
        return jsonify({"error": str(e), "query": query}), 500

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        "service": "RaiderBot MCP Server",
        "status": "running",
        "version": "1.0.0", 
        "endpoints": {
            "health": "/health",
            "search_orders": "/search_orders"
        }
    })

if __name__ == "__main__":
    # Production startup
    logger.info("🚀 Starting RaiderBot HTTP Server (Production)")
    
    # Test enhanced Snowflake connection
    if cortex_client.connect():
        logger.info("✅ Enhanced Snowflake connection established")
    else:
        logger.error("❌ Failed to connect to Snowflake")
    
    # Start HTTP server
    port = int(os.getenv('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
