#!/usr/bin/env python3
"""
Validation script for Palantir Foundry enhancements
Tests all major components to ensure they work correctly
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test that all new modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from src.foundry.sls_logging import get_structured_logger, emit_metric, correlation_context
        print("✅ SLS logging imports successful")
    except Exception as e:
        print(f"❌ SLS logging import failed: {e}")
        return False
    
    try:
        from src.foundry.ontology_integration import TransportationOrder, FleetVehicle, OntologyManager
        print("✅ Ontology integration imports successful")
    except Exception as e:
        print(f"❌ Ontology integration import failed: {e}")
        return False
    
    try:
        from src.foundry.error_handling import error_handler, PalantirAuthError
        print("✅ Error handling imports successful")
    except Exception as e:
        print(f"❌ Error handling import failed: {e}")
        return False
    
    try:
        from src.foundry.performance_optimization import cache, pagination_helper
        print("✅ Performance optimization imports successful")
    except Exception as e:
        print(f"❌ Performance optimization import failed: {e}")
        return False
    
    try:
        from src.foundry.aip_integration import AIPModelClient, RAGEngine
        print("✅ AIP integration imports successful")
    except Exception as e:
        print(f"❌ AIP integration import failed: {e}")
        return False
    
    try:
        from src.foundry.testing_framework import MockFoundryClient, FoundryTestHarness
        print("✅ Testing framework imports successful")
    except Exception as e:
        print(f"❌ Testing framework import failed: {e}")
        return False
    
    try:
        from src.raiderbot_auth import PalantirAuthenticator
        print("✅ Authentication module imports successful")
    except Exception as e:
        print(f"❌ Authentication module import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from src.foundry.sls_logging import get_structured_logger, correlation_context
        logger = get_structured_logger("test")
        
        with correlation_context() as correlation_id:
            logger.info("test_message", test_data="validation")
            print(f"✅ Structured logging works (correlation_id: {correlation_id[:8]}...)")
    except Exception as e:
        print(f"❌ Structured logging test failed: {e}")
        return False
    
    try:
        from src.foundry.ontology_integration import TransportationOrder
        order = TransportationOrder(
            order_id="test_001",
            customer_id="customer_001", 
            pickup_location="Location A",
            delivery_location="Location B",
            status="active",
            created_date=datetime.now()
        )
        ontology_obj = order.to_ontology_object()
        assert ontology_obj["objectType"] == "TransportationOrder"
        print("✅ Ontology object creation works")
    except Exception as e:
        print(f"❌ Ontology object test failed: {e}")
        return False
    
    try:
        from src.foundry.performance_optimization import cache
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        assert value == "test_value"
        print("✅ Cache functionality works")
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        return False
    
    try:
        from src.foundry.testing_framework import MockFoundryClient
        mock_client = MockFoundryClient()
        assert hasattr(mock_client, 'get_auth_headers')
        print("✅ Mock Foundry client creation works")
    except Exception as e:
        print(f"❌ Mock Foundry client test failed: {e}")
        return False
    
    return True

def test_enhanced_quarterback_functions():
    """Test enhanced quarterback functions with new logging"""
    print("\n⚡ Testing enhanced quarterback functions...")
    
    try:
        from src.foundry.quarterback_functions import process_user_query, autonomous_decision_making
        
        result = process_user_query("optimize delivery routes")
        assert result["intent"] == "route_optimization"
        print("✅ Enhanced query processing works")
        
        scenario = {"type": "route_optimization", "priority": "high"}
        decision = autonomous_decision_making(scenario)
        assert decision["decision"] == "IMPLEMENT_DYNAMIC_ROUTING"
        print("✅ Enhanced autonomous decision making works")
        
    except Exception as e:
        print(f"❌ Enhanced quarterback functions test failed: {e}")
        return False
    
    return True

def main():
    """Run all validation tests"""
    print("🚀 Starting Palantir Foundry Enhancement Validation")
    print("=" * 60)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_basic_functionality():
        all_passed = False
    
    if not test_enhanced_quarterback_functions():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL VALIDATION TESTS PASSED!")
        print("✅ Palantir Foundry enhancements are working correctly")
        return 0
    else:
        print("❌ SOME VALIDATION TESTS FAILED!")
        print("⚠️ Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
