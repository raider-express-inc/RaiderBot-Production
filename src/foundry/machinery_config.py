"""
Machinery Process Configuration for RaiderBot
Defines automated workflows for common build patterns
"""

MACHINERY_PROCESSES = {
    "dashboard_builder": {
        "name": "Dashboard Builder Process",
        "description": "Automated process for creating dashboards",
        "steps": [
            {
                "id": "analyze_request",
                "type": "ai_analysis",
                "name": "Analyze Dashboard Requirements",
                "config": {
                    "prompt_template": "Extract dashboard requirements from: {request}"
                }
            },
            {
                "id": "identify_data",
                "type": "data_discovery",
                "name": "Identify Required Data Sources",
                "depends_on": ["analyze_request"]
            },
            {
                "id": "create_workshop",
                "type": "workshop_creation",
                "name": "Create Workshop Application",
                "depends_on": ["identify_data"]
            },
            {
                "id": "add_widgets",
                "type": "widget_configuration",
                "name": "Configure Dashboard Widgets",
                "depends_on": ["create_workshop"]
            }
        ]
    },
    
    "tms_automation": {
        "name": "TMS Automation Process",
        "description": "Specialized process for TMS-related builds",
        "steps": [
            {
                "id": "tms_analysis",
                "type": "domain_analysis",
                "name": "Analyze TMS Requirements"
            },
            {
                "id": "data_integration",
                "type": "data_pipeline",
                "name": "Integrate TMS Data Sources"
            }
        ]
    }
}