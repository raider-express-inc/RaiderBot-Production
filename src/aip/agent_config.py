"""
RaiderBot AIP Agent Configuration
Defines the AI agent for natural language processing and automation
"""

AIP_AGENT_CONFIG = {
    "name": "RaiderBot Enterprise Builder",
    "description": "AI agent that interprets natural language requests and builds Foundry applications",
    "version": "1.0.0",
    
    "capabilities": [
        "workshop_app_creation",
        "data_pipeline_building",
        "ontology_management",
        "automation_workflows",
        "dashboard_generation",
        "report_creation"
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
