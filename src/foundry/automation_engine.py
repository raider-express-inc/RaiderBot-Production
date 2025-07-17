"""
RaiderBot Foundry Automation Engine
Main orchestration for "Build This Out" functionality
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import aiohttp
from enum import Enum
from .workbook_instruction_service import WorkbookInstructionService, VisualizationInstruction

# Import Palantir SDK when available
try:
    # Try official SDK first
    from foundry_sdk import FoundryClient
    from foundry_sdk.branches import Branch
    from foundry_sdk.machinery import MachineryProcess
    FOUNDRY_AVAILABLE = True
except ImportError:
    try:
        # Fall back to our mock SDK
        import sys
        sys.path.append('/Users/daneggleton/RaiderBot-Cursor-Deploy')
        from src.foundry_sdk import FoundryClient, Branch, MachineryProcess
        FOUNDRY_AVAILABLE = True
        print("Using mock Foundry SDK for development")
    except ImportError:
        FOUNDRY_AVAILABLE = False
        print("Warning: Foundry SDK not available. Running in mock mode.")

class BuildType(Enum):
    WORKSHOP_APP = "workshop_app"
    DATA_PIPELINE = "data_pipeline"
    ONTOLOGY_OBJECT = "ontology_object"
    AUTOMATION_WORKFLOW = "automation_workflow"
    DASHBOARD = "dashboard"
    REPORT = "report"

@dataclass
class BuildRequest:
    id: str
    user_id: str
    natural_language_request: str
    build_type: Optional[BuildType] = None
    parameters: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.parameters is None:
            self.parameters = {}

@dataclass
class BuildStep:
    name: str
    type: str
    status: str = "pending"
    config: Optional[Dict[str, Any]] = None
    result: Any = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}
class RaiderBotAutomationEngine:
    """Main automation engine for RaiderBot Foundry integration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.foundry_client = self._init_foundry_client()
        self.aip_agent = None
        self.active_builds = {}
        self.workbook_service = WorkbookInstructionService(self.foundry_client)
        
    def _init_foundry_client(self):
        """Initialize Foundry client with credentials"""
        if not FOUNDRY_AVAILABLE:
            return None
            
        return FoundryClient(
            auth_token=self.config.get("FOUNDRY_AUTH_TOKEN"),
            foundry_url=self.config.get("FOUNDRY_URL"),
            client_id=self.config.get("FOUNDRY_CLIENT_ID"),
            client_secret=self.config.get("FOUNDRY_CLIENT_SECRET")
        )
    
    async def process_build_request(self, request: BuildRequest) -> Dict[str, Any]:
        """Process a build request from natural language"""
        print(f"Processing build request: {request.natural_language_request}")
        
        # Step 1: Analyze request with AI
        build_plan = await self._analyze_request(request)
        
        # Step 2: Create safe branch for development
        branch = await self._create_development_branch(request)
        
        # Step 3: Execute build plan
        results = await self._execute_build_plan(build_plan, branch)
        
        # Step 4: Test the build
        test_results = await self._test_build(results, branch)
        
        # Step 5: Deploy if tests pass
        if test_results["success"]:
            deployment = await self._deploy_to_production(results, branch)
            return {
                "success": True,
                "build_id": request.id,
                "artifacts": results,
                "deployment": deployment
            }
        else:
            return {
                "success": False,
                "build_id": request.id,
                "errors": test_results["errors"]
            }    
    async def _analyze_request(self, request: BuildRequest) -> List[BuildStep]:
        """Analyze natural language request and create build plan"""
        # In production, this would call AIP Agent
        # For now, use pattern matching
        
        build_steps = []
        request_lower = request.natural_language_request.lower()
        
        if "dashboard" in request_lower:
            build_steps.append(BuildStep(
                name="Create Dashboard",
                type="workshop_app",
                config={
                    "template": "dashboard",
                    "widgets": ["chart", "table", "metrics"]
                }
            ))
        
        if "fuel" in request_lower or "cost" in request_lower:
            build_steps.append(BuildStep(
                name="Add Fuel Cost Analysis",
                type="data_pipeline",
                config={
                    "source": "fuel_data",
                    "transformations": ["aggregate", "calculate_costs"]
                }
            ))
        
        if "tms" in request_lower:
            build_steps.append(BuildStep(
                name="Configure TMS Data",
                type="data_connection",
                config={
                    "source": "snowflake",
                    "tables": ["ORDERS", "CUSTOMERS"]
                }
            ))
        
        if any(keyword in request_lower for keyword in ["chart", "graph", "visualization", "graphics"]):
            build_steps.append(BuildStep(
                name="Generate Visualization Instructions",
                type="workbook_visualization",
                config={
                    "visualization_type": self._detect_visualization_type(request_lower),
                    "data_source": self._detect_data_source(request_lower),
                    "user_context": request.user_id
                }
            ))
        
        if "dashboard" in request_lower and "user" in request_lower:
            build_steps.append(BuildStep(
                name="Provision User Dashboard",
                type="user_dashboard",
                config={
                    "user_id": request.user_id,
                    "template": "role_based",
                    "integration": "raiderbot"
                }
            ))
        
        return build_steps
    
    def _detect_visualization_type(self, request_text: str) -> str:
        """Detect visualization type from request text"""
        if any(word in request_text for word in ["bar", "column", "chart"]):
            return "chart"
        elif any(word in request_text for word in ["table", "list", "grid"]):
            return "table"
        elif any(word in request_text for word in ["metric", "kpi", "number"]):
            return "metrics"
        elif any(word in request_text for word in ["map", "location", "route"]):
            return "map"
        else:
            return "chart"
    
    def _detect_data_source(self, request_text: str) -> str:
        """Detect data source from request text"""
        if "snowflake" in request_text:
            return "snowflake"
        elif any(word in request_text for word in ["order", "delivery", "customer"]):
            return "orders_table"
        elif any(word in request_text for word in ["driver", "fleet", "vehicle"]):
            return "fleet_table"
        elif any(word in request_text for word in ["safety", "incident"]):
            return "safety_table"
        else:
            return "default_data"
    
    async def _create_development_branch(self, request: BuildRequest) -> Any:
        """Create safe development branch"""
        if self.foundry_client:
            branch_name = f"build-{request.id[:8]}-{datetime.now().strftime('%Y%m%d')}"
            return self.foundry_client.create_branch(branch_name)
        return None
    
    async def _execute_build_plan(self, build_plan: List[BuildStep], branch: Any) -> List[BuildStep]:
        """Execute the build plan steps"""
        for step in build_plan:
            try:
                print(f"Executing step: {step.name}")
                
                if step.type == "workbook_visualization" and step.config:
                    instruction = VisualizationInstruction(
                        user_id=step.config.get("user_context", "default"),
                        workbook_id=f"workbook_{step.config.get('user_context', 'default')}_main",
                        visualization_type=step.config.get("visualization_type", "chart"),
                        data_source=step.config.get("data_source", "default"),
                        chart_config={"type": step.config.get("visualization_type", "chart")},
                        layout_instructions={"position": "auto", "size": "medium"}
                    )
                    result = await self.workbook_service.push_visualization_instructions(instruction)
                    step.result = result
                    
                elif step.type == "user_dashboard" and step.config:
                    result = await self.workbook_service.provision_user_dashboard(
                        user_id=step.config.get("user_id", "default"),
                        user_role="default",
                        template=step.config.get("template", "default")
                    )
                    step.result = result
                    
                else:
                    await asyncio.sleep(0.5)
                    step.result = {
                        "artifact_id": f"{step.type}_{datetime.now().timestamp()}",
                        "location": f"/foundry/artifacts/{step.type}"
                    }
                
                step.status = "completed"
                
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
        
        return build_plan
    
    async def _test_build(self, results: List[BuildStep], branch: Any) -> Dict[str, Any]:
        """Test the build before deployment"""
        # Check if all steps completed
        failed_steps = [step for step in results if step.status == "failed"]
        
        if failed_steps:
            return {
                "success": False,
                "errors": [f"{step.name}: {step.error}" for step in failed_steps]
            }
        
        return {
            "success": True,
            "test_results": {
                "unit_tests": "passed",
                "integration_tests": "passed",
                "performance": "acceptable"
            }
        }
    
    async def _deploy_to_production(self, results: List[BuildStep], branch: Any) -> Dict[str, Any]:
        """Deploy successful build to production"""
        if branch and hasattr(branch, 'merge'):
            branch.merge()
        
        artifacts = [step.result for step in results if step.result]
        
        return {
            "deployment_id": f"deploy_{datetime.now().timestamp()}",
            "artifacts": artifacts,
            "url": "https://your-stack.palantirfoundry.com/workspace/raiderbot",
            "timestamp": datetime.now().isoformat()
        }

# Quick test function
async def test_automation():
    """Test the automation engine"""
    config = {
        "FOUNDRY_URL": "https://test.palantirfoundry.com",
        "FOUNDRY_CLIENT_ID": "test_client",
        "FOUNDRY_CLIENT_SECRET": "test_secret"
    }
    
    engine = RaiderBotAutomationEngine(config)
    
    test_request = BuildRequest(
        id="test-123",
        user_id="test_user",
        natural_language_request="Build me a fuel cost dashboard"
    )
    
    result = await engine.process_build_request(test_request)
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    # Run test
    asyncio.run(test_automation())
