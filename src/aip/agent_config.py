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
        }