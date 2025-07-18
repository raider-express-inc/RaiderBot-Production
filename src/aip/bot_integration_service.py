"""
Bot Integration Service
Enhanced with all 8 critical checklist integrations
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

class BotIntegrationService:
    """Enhanced bot integration with all critical services"""
    
    def __init__(self, foundry_engine):
        self.foundry_engine = foundry_engine
        self.foundry_client = foundry_engine.foundry_client
        self.command_mappings = {
            "delivery_performance": "Create delivery performance dashboard",
            "safety_metrics": "Create safety metrics dashboard", 
            "driver_performance": "Create driver performance dashboard",
            "route_optimization": "Create route optimization dashboard",
            "customer_analytics": "Create customer analytics dashboard"
        }
        
    async def process_bot_command(self, command: str, user_id: str) -> Dict[str, Any]:
        """Process bot command with comprehensive service integration"""
        try:
            from src.audit.snowflake_audit_service import SnowflakeAuditService, AuditEventType
            from src.orchestrator.external_orchestrator_service import ExternalOrchestratorService
            from src.sema4.sema4_execution_service import Sema4ExecutionService
            from src.dashboard.modern_dashboard_service import ModernDashboardService
            
            audit_service = SnowflakeAuditService(None)
            orchestrator = ExternalOrchestratorService(self.foundry_client)
            sema4_service = Sema4ExecutionService()
            dashboard_service = ModernDashboardService(self.foundry_client)
            
            await audit_service.log_user_interaction(user_id, command, {
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            if command in self.command_mappings:
                description = self.command_mappings[command]
                
                orchestrator_result = await orchestrator.coordinate_workflow({
                    "request": description,
                    "user_id": user_id,
                    "command": command
                })
                
                dashboard_result = await dashboard_service.create_modern_dashboard({
                    "user_id": user_id,
                    "command": command
                })
                
                workbook_instructions = await self._generate_workbook_instructions(command, user_id)
                
                bot_response = f"¡Woof! I've created your {command} dashboard with safety-first precision! 🦸‍♂️🐕"
                
                return {
                    "success": True,
                    "command": command,
                    "bot_response": bot_response,
                    "artifacts": workbook_instructions,
                    "orchestrator_result": orchestrator_result,
                    "dashboard_result": dashboard_result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                sema4_result = await sema4_service.execute_natural_language_query(
                    command,
                    {"user_id": user_id, "role": "user"}
                )
                
                bot_response = f"¡Woof! I've processed your request with German Shepherd precision! 🦸‍♂️🐕"
                
                return {
                    "success": True,
                    "command": command,
                    "bot_response": bot_response,
                    "sema4_result": sema4_result,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "bot_response": f"¡Woof! Something went wrong, but this German Shepherd is on it! 🦸‍♂️🐕",
                "timestamp": datetime.now().isoformat()
            }
            
    async def _generate_workbook_instructions(self, command: str, user_id: str) -> List[Dict[str, Any]]:
        """Generate workbook visualization instructions"""
        instructions = [
            {
                "type": "chart",
                "chart_type": "line",
                "title": f"{command.replace('_', ' ').title()} Trends",
                "data_source": f"{command}_data",
                "x_axis": "timestamp",
                "y_axis": "performance_score"
            },
            {
                "type": "metric_card",
                "title": f"Current {command.replace('_', ' ').title()}",
                "value_source": f"{command}_current_value",
                "format": "percentage"
            }
        ]
        
        viz_result = await self.foundry_client.update_workbook_visualization(
            f"workbook_{user_id}_{command}",
            {
                "instructions": instructions,
                "theme": "german_shepherd",
                "user_id": user_id
            }
        )
        
        return instructions
