"""
RaiderBot Workbook Visualization Instruction Service
Handles pushing visualization instructions to Foundry Workshop workbooks
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class VisualizationInstruction:
    user_id: str
    workbook_id: str
    visualization_type: str
    data_source: str
    chart_config: Dict[str, Any]
    layout_instructions: Dict[str, Any]
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class WorkbookInstructionService:
    """Service for pushing visualization instructions to user workbooks"""
    
    def __init__(self, foundry_client):
        self.foundry_client = foundry_client
        self.active_instructions = {}
        
    async def push_visualization_instructions(self, instruction: VisualizationInstruction) -> Dict[str, Any]:
        """Push visualization instructions to user workbook"""
        try:
            viz_config = self._generate_visualization_config(instruction)
            
            result = await self._push_to_workbook(instruction.workbook_id, viz_config)
            
            self.active_instructions[instruction.workbook_id] = instruction
            
            return {
                "success": True,
                "instruction_id": f"viz_{datetime.now().timestamp()}",
                "workbook_id": instruction.workbook_id,
                "visualization_type": instruction.visualization_type,
                "pushed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "instruction": instruction
            }
    
    def _generate_visualization_config(self, instruction: VisualizationInstruction) -> Dict[str, Any]:
        """Generate Foundry-compatible visualization configuration"""
        base_config = {
            "type": instruction.visualization_type,
            "data_source": instruction.data_source,
            "user_id": instruction.user_id,
            "created_by": "raiderbot_ai",
            "timestamp": instruction.timestamp.isoformat() if instruction.timestamp else datetime.now().isoformat()
        }
        
        if instruction.visualization_type == "chart":
            chart_config = {
                "chart_type": instruction.chart_config.get("type", "bar"),
                "x_axis": instruction.chart_config.get("x_axis"),
                "y_axis": instruction.chart_config.get("y_axis"),
                "color_scheme": "raider_red_theme"
            }
            base_config.update(chart_config)
        elif instruction.visualization_type == "table":
            table_config = {
                "columns": instruction.chart_config.get("columns", []),
                "filters": instruction.chart_config.get("filters", {}),
                "sorting": instruction.chart_config.get("sorting", {})
            }
            base_config.update(table_config)
        elif instruction.visualization_type == "metrics":
            metrics_config = {
                "metrics": instruction.chart_config.get("metrics", []),
                "time_range": instruction.chart_config.get("time_range", "24h"),
                "comparison": instruction.chart_config.get("comparison", "previous_period")
            }
            base_config.update(metrics_config)
        
        layout_config = {"layout": instruction.layout_instructions}
        base_config.update(layout_config)
        
        return base_config
    
    async def _push_to_workbook(self, workbook_id: str, viz_config: Dict[str, Any]) -> Dict[str, Any]:
        """Push visualization config to Foundry workbook"""
        if self.foundry_client:
            return await self.foundry_client.update_workbook_visualization(workbook_id, viz_config)
        else:
            return {
                "status": "pushed",
                "workbook_id": workbook_id,
                "config": viz_config
            }
    
    async def provision_user_dashboard(self, user_id: str, user_role: str, template: str = "default") -> Dict[str, Any]:
        """Provision connected dashboard for user"""
        try:
            dashboard_config = {
                "user_id": user_id,
                "role": user_role,
                "template": template,
                "widgets": self._get_role_based_widgets(user_role),
                "data_permissions": self._get_role_permissions(user_role),
                "raiderbot_integration": True,
                "german_shepherd_theme": True
            }
            
            if self.foundry_client:
                result = await self.foundry_client.create_user_dashboard(dashboard_config)
            else:
                result = {
                    "dashboard_id": f"dashboard_{user_id}_{datetime.now().timestamp()}",
                    "url": f"https://foundry.raiderexpress.com/workspace/user/{user_id}/dashboard",
                    "status": "provisioned"
                }
            
            return {
                "success": True,
                "user_id": user_id,
                "dashboard": result,
                "provisioned_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user_id": user_id
            }
    
    def _get_role_based_widgets(self, role: str) -> List[str]:
        """Get default widgets based on user role"""
        role_widgets = {
            "dispatch": ["delivery_performance", "route_optimization", "driver_status"],
            "fleet": ["safety_metrics", "vehicle_status", "maintenance_alerts"],
            "customer_service": ["email_analysis", "customer_satisfaction", "response_times"],
            "management": ["executive_dashboard", "kpi_overview", "financial_metrics"],
            "safety": ["safety_scores", "incident_reports", "compliance_status"]
        }
        return role_widgets.get(role.lower(), ["basic_dashboard", "help_center"])
    
    def _get_role_permissions(self, role: str) -> List[str]:
        """Get data permissions based on user role"""
        role_permissions = {
            "dispatch": ["orders", "drivers", "routes"],
            "fleet": ["vehicles", "maintenance", "safety"],
            "customer_service": ["customers", "emails", "satisfaction"],
            "management": ["all_data", "financial", "analytics"],
            "safety": ["safety_data", "incidents", "compliance"]
        }
        return role_permissions.get(role.lower(), ["basic_data"])
