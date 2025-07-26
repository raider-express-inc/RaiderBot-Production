#!/usr/bin/env python3
"""
Test script to verify AIP agent instructions and logistics expertise
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentInstructionTester:
    def __init__(self):
        self.agent_rid = "ri.aip-agents..agent.e6e9ff2f-0952-4774-98b5-4388a96ddbf1"
        self.base_url = "https://raiderexpress.palantirfoundry.com"
        
    def test_instruction_configuration(self) -> Dict[str, Any]:
        """Test that instructions are properly configured"""
        logger.info("🧪 Testing instruction configuration...")
        
        from src.aip.agent_config import AIP_AGENT_CONFIG
        
        instructions = AIP_AGENT_CONFIG.get("instructions", {})
        
        results = {
            "has_system_prompt": bool(instructions.get("system_prompt")),
            "has_behavioral_guidelines": bool(instructions.get("behavioral_guidelines")),
            "has_example_interactions": bool(instructions.get("example_interactions")),
            "system_prompt_length": len(instructions.get("system_prompt", "")),
            "guideline_count": len(instructions.get("behavioral_guidelines", [])),
            "example_count": len(instructions.get("example_interactions", []))
        }
        
        logger.info(f"   ✅ System prompt: {'Configured' if results['has_system_prompt'] else 'Missing'} ({results['system_prompt_length']} chars)")
        logger.info(f"   ✅ Behavioral guidelines: {results['guideline_count']} configured")
        logger.info(f"   ✅ Example interactions: {results['example_count']} configured")
        
        return results
    
    def test_logistics_expertise(self) -> Dict[str, Any]:
        """Test logistics-specific configuration"""
        logger.info("🚛 Testing logistics expertise configuration...")
        
        from src.aip.agent_config import AIP_AGENT_CONFIG
        
        instructions = AIP_AGENT_CONFIG.get("instructions", {})
        system_prompt = instructions.get("system_prompt", "")
        
        logistics_keywords = [
            "transportation", "fleet", "logistics", "TMS", "route optimization",
            "driver safety", "delivery", "supply chain", "compliance"
        ]
        
        keyword_matches = [keyword for keyword in logistics_keywords if keyword.lower() in system_prompt.lower()]
        
        results = {
            "logistics_keywords_found": len(keyword_matches),
            "total_keywords_checked": len(logistics_keywords),
            "coverage_percentage": (len(keyword_matches) / len(logistics_keywords)) * 100,
            "matched_keywords": keyword_matches
        }
        
        logger.info(f"   ✅ Logistics coverage: {results['coverage_percentage']:.1f}% ({results['logistics_keywords_found']}/{results['total_keywords_checked']} keywords)")
        
        return results
    
    def test_german_shepherd_personality(self) -> Dict[str, Any]:
        """Test German Shepherd personality configuration"""
        logger.info("🐕 Testing German Shepherd personality...")
        
        from src.aip.agent_config import AIP_AGENT_CONFIG
        
        instructions = AIP_AGENT_CONFIG.get("instructions", {})
        system_prompt = instructions.get("system_prompt", "")
        
        personality_elements = [
            "German Shepherd", "🐕", "🦸‍♂️", "Wunderbar", "Achtung", 
            "loyalty", "protective", "superhero", "working dog"
        ]
        
        found_elements = [element for element in personality_elements if element in system_prompt]
        
        results = {
            "personality_elements_found": len(found_elements),
            "total_elements_checked": len(personality_elements),
            "personality_strength": (len(found_elements) / len(personality_elements)) * 100,
            "found_elements": found_elements
        }
        
        logger.info(f"   ✅ Personality strength: {results['personality_strength']:.1f}% ({results['personality_elements_found']}/{results['total_elements_checked']} elements)")
        
        return results
    
    def test_tool_logistics_integration(self) -> Dict[str, Any]:
        """Test that tools are properly configured for logistics use cases"""
        logger.info("🛠️ Testing tool logistics integration...")
        
        from src.aip.agent_config import AIP_AGENT_CONFIG
        
        tools = AIP_AGENT_CONFIG.get("tools", [])
        tools_with_logistics = 0
        
        for tool in tools:
            if any(key in tool for key in ["logistics_use_cases", "logistics_visualizations", "role_templates", "update_types"]):
                tools_with_logistics += 1
        
        results = {
            "total_tools": len(tools),
            "tools_with_logistics": tools_with_logistics,
            "logistics_integration_rate": (tools_with_logistics / len(tools)) * 100 if tools else 0
        }
        
        logger.info(f"   ✅ Tool integration: {results['logistics_integration_rate']:.1f}% ({results['tools_with_logistics']}/{results['total_tools']} tools)")
        
        return results

async def main():
    """Run comprehensive agent instruction tests"""
    print("🧪 AIP Agent Instruction Test Suite")
    print("=" * 60)
    
    tester = AgentInstructionTester()
    
    instruction_results = tester.test_instruction_configuration()
    logistics_results = tester.test_logistics_expertise()
    personality_results = tester.test_german_shepherd_personality()
    tool_results = tester.test_tool_logistics_integration()
    
    scores = [
        instruction_results["guideline_count"] > 0,
        instruction_results["system_prompt_length"] > 500,
        logistics_results["coverage_percentage"] > 70,
        personality_results["personality_strength"] > 60,
        tool_results["logistics_integration_rate"] > 80
    ]
    
    overall_score = (sum(scores) / len(scores)) * 100
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Instruction Configuration: {'✅' if instruction_results['has_system_prompt'] else '❌'}")
    print(f"   Logistics Expertise: {logistics_results['coverage_percentage']:.1f}%")
    print(f"   German Shepherd Personality: {personality_results['personality_strength']:.1f}%")
    print(f"   Tool Integration: {tool_results['logistics_integration_rate']:.1f}%")
    print(f"   Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 80:
        print("\n🎉 Agent Instructions: READY FOR DEPLOYMENT")
    else:
        print("\n⚠️ Agent instructions need improvement before deployment")
    
    return overall_score

if __name__ == "__main__":
    asyncio.run(main())
