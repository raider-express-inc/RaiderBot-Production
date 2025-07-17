"""
Integration service between RaiderBot commands and AIP Studio
"""

import asyncio
from typing import Dict, Any, List, Optional
from ..foundry.automation_engine import RaiderBotAutomationEngine, BuildRequest

class BotIntegrationService:
    """Integrates German Shepherd bot commands with AIP Studio workbook instructions"""
    
    def __init__(self, automation_engine: RaiderBotAutomationEngine):
        self.automation_engine = automation_engine
        self.command_mappings = self._init_command_mappings()
    
    def _init_command_mappings(self) -> Dict[str, str]:
        """Map bot commands to AIP Studio build requests"""
        return {
            "delivery_performance": "Build delivery performance dashboard with charts and metrics",
            "driver_performance": "Create driver performance visualization with safety scores",
            "email_analysis": "Generate customer email sentiment analysis dashboard",
            "safety_metrics": "Build safety metrics dashboard with incident tracking",
            "route_optimization": "Create route optimization visualization with map display"
        }
    
    async def process_bot_command(self, command: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process bot command and generate workbook instructions"""
        try:
            build_request_text = self.command_mappings.get(command, f"Build dashboard for {command}")
            
            enhanced_request = f"{build_request_text} with German Shepherd superhero theme and Fort Worth branding"
            
            build_request = BuildRequest(
                id=f"bot_{command}_{user_id}",
                user_id=user_id,
                natural_language_request=enhanced_request,
                parameters=context or {}
            )
            
            result = await self.automation_engine.process_build_request(build_request)
            
            if result["success"]:
                result["bot_response"] = f"¡Woof! I've created your {command} dashboard with safety-first precision! 🦸‍♂️🐕"
            else:
                result["bot_response"] = f"Woof! I encountered an issue creating your {command} dashboard. Let me try a different approach! 🐕"
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "bot_response": "Woof! Something went wrong, but I'm on it! 🐕"
            }
    
    def get_available_commands(self) -> List[Dict[str, str]]:
        """Get list of available bot commands for AIP Studio"""
        return [
            {"command": cmd, "description": desc} 
            for cmd, desc in self.command_mappings.items()
        ]
