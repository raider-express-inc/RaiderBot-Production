#!/usr/bin/env python3

import json
import time
from datetime import datetime
from typing import Dict, Any


class QuarterbackTester:
    def __init__(self, config_path: str = "tools.routing.json"):
        with open(config_path, "r") as f:
            self.routing_config = json.load(f)

        self.metrics = {
            "test_run_timestamp": datetime.utcnow().isoformat() + "Z",
            "scenarios": [],
        }

    def test_scenario(
        self, scenario_name: str, test_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Test a quarterback scenario and measure performance"""

        start_time = time.time()

        try:
            intent_config = None
            for intent in self.routing_config["intent_mappings"]:
                if intent["intent"] == scenario_name:
                    intent_config = intent
                    break

            if not intent_config:
                return {
                    "scenario": scenario_name,
                    "success": False,
                    "error": "Intent not found in routing config",
                    "latency_ms": 0,
                }

            best_tool = max(intent_config["tools"], key=lambda t: t["weight"])

            if "mcp://" in best_tool["endpoint"]:
                result = self._simulate_mcp_call(best_tool, test_payload)
            else:
                result = self._simulate_http_call(best_tool, test_payload)

            latency_ms = int((time.time() - start_time) * 1000)

            return {
                "scenario": scenario_name,
                "success": result["success"],
                "selected_tool": best_tool["tool_id"],
                "latency_ms": latency_ms,
                "result": result.get("data"),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "scenario": scenario_name,
                "success": False,
                "error": str(e),
                "latency_ms": latency_ms,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    def _simulate_mcp_call(
        self, tool: Dict[str, Any], payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate MCP tool call"""
        return {
            "success": True,
            "data": f"MCP tool {tool['tool_id']} executed successfully",
        }

    def _simulate_http_call(
        self, tool: Dict[str, Any], payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate HTTP endpoint call"""
        try:
            if "functions" in tool["endpoint"]:
                return {
                    "success": True,
                    "data": {"row_count": 5, "rows": [{"test": "data"}]},
                }
            else:
                return {
                    "success": True,
                    "data": {"hits": [{"title": "Test Document", "score": 0.95}]},
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_all_scenarios(self) -> Dict[str, Any]:
        """Run all three quarterback scenarios"""

        scenarios = [
            {
                "name": "rate_analysis",
                "payload": {
                    "sql": "SELECT AVG(rate) FROM financial_rates WHERE date >= '2024-01-01'",
                    "limit": 100,
                },
            },
            {
                "name": "document_qa",
                "payload": {
                    "query": "What are the current shipping rates for expedited delivery?",
                    "limit": 5,
                },
            },
            {
                "name": "ops_lookup",
                "payload": {
                    "sql": "SELECT status, count(*) FROM operations WHERE date = CURRENT_DATE GROUP BY status",
                    "limit": 50,
                },
            },
        ]

        results = []
        for scenario in scenarios:
            result = self.test_scenario(scenario["name"], scenario["payload"])
            results.append(result)
            print(
                f"{'✅' if result['success'] else '❌'} {scenario['name']}: {result['latency_ms']}ms"
            )

        successful_tests = [r for r in results if r["success"]]
        success_rate = len(successful_tests) / len(results) if results else 0
        avg_latency = (
            sum(r["latency_ms"] for r in successful_tests) / len(successful_tests)
            if successful_tests
            else 0
        )
        p95_latency = (
            sorted([r["latency_ms"] for r in successful_tests])[
                int(len(successful_tests) * 0.95)
            ]
            if successful_tests
            else 0
        )

        summary = {
            "overall_success": success_rate >= 0.95,
            "success_rate": success_rate,
            "avg_latency_ms": int(avg_latency),
            "p95_latency_ms": p95_latency,
            "total_scenarios": len(results),
            "successful_scenarios": len(successful_tests),
            "scenarios": results,
        }

        return summary


def main():
    tester = QuarterbackTester()
    results = tester.run_all_scenarios()

    with open("observability/quarterback_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n📊 Quarterback Test Results:")
    print(f"Success Rate: {results['success_rate']:.1%}")
    print(f"Average Latency: {results['avg_latency_ms']}ms")
    print(f"P95 Latency: {results['p95_latency_ms']}ms")
    print(f"Overall Success: {'✅' if results['overall_success'] else '❌'}")

    return 0 if results["overall_success"] else 1


if __name__ == "__main__":
    exit(main())
