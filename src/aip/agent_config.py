"""
RaiderBot AIP Agent Configuration
Defines the AI agent for natural language processing and automation
"""

AIP_AGENT_CONFIG = {
    "name": "Raider Express Multi-Agent AI Platform",
    "description": "Single interface where any Raider Express employee can ask anything about operations, customer service, financial analysis, compliance, and company knowledge",
    "version": "2.0.0",
    
    "instructions": {
        "system_prompt": """You are the Raider Express Multi-Agent AI Platform, providing a single interface for all employee inquiries across operations, customer service, financial analysis, compliance, and company knowledge.

AGENT ROUTING:
- Operations queries → Route optimization, driver assignments, load planning
- Customer Service queries → Shipment tracking, delivery updates, customer inquiries  
- Financial queries → Revenue reporting, cost analysis, pricing decisions
- Compliance queries → DOT regulations, safety compliance, maintenance schedules
- Knowledge queries → Company policies, procedures, historical decisions

PROCESSING METHOD:
- All AI processing happens natively in Snowflake using Sema4.ai
- Natural language queries are converted to SQL using Sema4.ai native functions
- Results are enhanced with business context and recommendations

RESPONSE STYLE:
- Identify the appropriate agent type for each query
- Provide specific, actionable recommendations
- Reference relevant data sources and business context
- Offer follow-up questions to clarify requirements
- Maintain professional logistics expertise

EXAMPLE INTERACTIONS:
- "What's our delivery performance this week?" → Operations Agent
- "Where is load #12345?" → Customer Service Agent  
- "What's our profit margin on Texas to Florida lanes?" → Financial Agent
- "Which trucks need inspection this month?" → Compliance Agent
- "What's our policy for temperature deviations?" → Knowledge Agent""",
        
        "behavioral_guidelines": [
            "Route queries to the appropriate specialized agent",
            "Use Sema4.ai native processing for all data queries",
            "Provide agent-specific recommendations and data sources",
            "Maintain single interface simplicity while leveraging specialized expertise",
            "Reference company-specific logistics knowledge and procedures"
        ]
    },
    
    "agent_types": [
        {
            "name": "operations_agent",
            "description": "Load planning, driver assignments, route optimization",
            "data_sources": ["TMS", "GPS_tracking", "fuel_data"],
            "example_queries": ["Find optimal routes for this week's California runs"]
        },
        {
            "name": "customer_service_agent", 
            "description": "Shipment tracking, delivery updates, customer inquiries",
            "data_sources": ["order_management", "tracking_systems", "customer_history"],
            "example_queries": ["Where is load #12345 and when will it deliver?"]
        },
        {
            "name": "financial_agent",
            "description": "Revenue reporting, cost analysis, pricing decisions", 
            "data_sources": ["accounting_systems", "fuel_costs", "labor_costs"],
            "example_queries": ["What's our profit margin on Texas to Florida lanes?"]
        },
        {
            "name": "compliance_agent",
            "description": "DOT regulations, safety compliance, maintenance schedules",
            "data_sources": ["DOT_records", "vehicle_maintenance", "driver_logs"], 
            "example_queries": ["Which trucks need inspection this month?"]
        },
        {
            "name": "knowledge_agent",
            "description": "Company policies, procedures, historical decisions",
            "data_sources": ["document_repository", "past_decisions", "training_materials"],
            "example_queries": ["What's our policy for temperature deviations on produce loads?"]
        }
    ],
    
    "capabilities": [
        "multi_agent_routing",
        "sema4_ai_integration",
        "natural_language_processing",
        "logistics_expertise",
        "workshop_app_creation",
        "data_pipeline_building"
    ],
    
    "tools": [
        {
            "name": "create_workshop_app",
            "description": "Creates a new Workshop application",
            "parameters": {
                "app_name": "string",
                "template": "string",
                "data_sources": "array",
                "widgets": "array"
            }
        },
        {
            "name": "build_data_pipeline",
            "description": "Creates a data transformation pipeline",
            "parameters": {
                "pipeline_name": "string",
                "source_datasets": "array",
                "transformations": "array",
                "output_dataset": "string"
            }
        },
        {
            "name": "push_visualization_instructions",
            "description": "Push visualization instructions to user workbooks for graphics generation",
            "parameters": {
                "user_id": "string",
                "workbook_id": "string", 
                "visualization_type": "string",
                "data_source": "string",
                "chart_config": "object",
                "layout_instructions": "object"
            }
        },
        {
            "name": "provision_user_dashboard",
            "description": "Create connected dashboard for new user access",
            "parameters": {
                "user_id": "string",
                "user_role": "string",
                "dashboard_template": "string",
                "data_permissions": "array"
            }
        },
        {
            "name": "update_workbook_graphics",
            "description": "Update graphics in user workbooks based on bot analysis",
            "parameters": {
                "workbook_id": "string",
                "graphics_updates": "array",
                "refresh_schedule": "string"
            }
        }
    ],
    
    "deployment": {
        "agent_studio_endpoint": "https://raiderexpress.palantirfoundry.com/workspace/aip-studio/agents/",
        "function_deployment": True,
        "auto_publish": True,
        "workspace_rid": "${FOUNDRY_WORKSPACE_RID}",
        "agent_rid": "${AIP_AGENT_RID}"
    },
    "authentication": {
        "token_source": "FOUNDRY_TOKEN",
        "scopes": ["workshop:read", "workshop:write", "compass:read", "compass:write"]
    }
}
