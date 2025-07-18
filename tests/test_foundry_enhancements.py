"""
Test suite for Palantir Foundry enhancements
"""

import pytest
import asyncio
from datetime import datetime
from src.foundry.sls_logging import get_structured_logger, emit_metric, correlation_context
from src.foundry.ontology_integration import TransportationOrder, FleetVehicle, OntologyManager
from src.foundry.error_handling import error_handler, PalantirAuthError
from src.foundry.performance_optimization import cache, pagination_helper
from src.foundry.aip_integration import AIPModelClient, RAGEngine
from src.foundry.testing_framework import MockFoundryClient, FoundryTestHarness

class TestSLSLogging:
    """Test SLS logging functionality"""
    
    def test_structured_logger_creation(self):
        """Test structured logger creation"""
        logger = get_structured_logger("test_logger")
        assert logger is not None
    
    def test_correlation_context(self):
        """Test correlation context management"""
        with correlation_context() as correlation_id:
            assert correlation_id is not None
            assert len(correlation_id) > 0
    
    def test_metric_emission(self):
        """Test metric emission"""
        emit_metric("test_metric", 1.0, {"test": "value"})

class TestOntologyIntegration:
    """Test ontology integration functionality"""
    
    def test_transportation_order_creation(self):
        """Test transportation order object creation"""
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
        assert ontology_obj["properties"]["orderId"] == "test_001"
    
    def test_fleet_vehicle_creation(self):
        """Test fleet vehicle object creation"""
        vehicle = FleetVehicle(
            vehicle_id="truck_001",
            vehicle_type="truck",
            license_plate="ABC123",
            capacity=1000.0,
            status="available"
        )
        
        ontology_obj = vehicle.to_ontology_object()
        assert ontology_obj["objectType"] == "FleetVehicle"
        assert ontology_obj["properties"]["vehicleId"] == "truck_001"
    
    @pytest.mark.asyncio
    async def test_ontology_manager(self):
        """Test ontology manager operations"""
        mock_client = MockFoundryClient()
        manager = OntologyManager(mock_client)
        
        order = TransportationOrder(
            order_id="test_002",
            customer_id="customer_002",
            pickup_location="Location C",
            delivery_location="Location D",
            status="active",
            created_date=datetime.now()
        )
        
        result = await manager.create_transportation_order(order)
        assert result["success"] is True

class TestErrorHandling:
    """Test error handling functionality"""
    
    def test_error_logging(self):
        """Test error logging"""
        test_error = PalantirAuthError("Test error")
        error_handler.log_error(test_error, {"test": "context"})
    
    def test_http_error_handling(self):
        """Test HTTP error conversion"""
        error = error_handler.handle_http_error(401, "Unauthorized", "/test/url")
        assert "Authentication failed" in str(error)

class TestPerformanceOptimization:
    """Test performance optimization functionality"""
    
    def test_cache_operations(self):
        """Test cache set and get operations"""
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        assert value == "test_value"
    
    def test_cache_expiration(self):
        """Test cache expiration"""
        cache.set("expire_key", "expire_value", ttl=0)
        value = cache.get("expire_key")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_pagination_helper(self):
        """Test pagination helper"""
        async def mock_fetch(offset=0, limit=10):
            if offset >= 20:
                return []
            return [{"id": i} for i in range(offset, min(offset + limit, 20))]
        
        results = await pagination_helper.paginate_results(mock_fetch, max_pages=3)
        assert len(results) == 20

class TestAIPIntegration:
    """Test AIP integration functionality"""
    
    @pytest.mark.asyncio
    async def test_aip_model_client(self):
        """Test AIP model client"""
        mock_client = MockFoundryClient()
        aip_client = AIPModelClient(mock_client)
        
        result = await aip_client.create_completion("Test prompt")
        assert "text" in result
    
    @pytest.mark.asyncio
    async def test_rag_engine(self):
        """Test RAG engine"""
        mock_client = MockFoundryClient()
        rag_engine = RAGEngine(mock_client)
        
        await rag_engine.add_knowledge(["Test document 1", "Test document 2"])
        context = await rag_engine.retrieve_relevant_context("test query")
        assert isinstance(context, list)

class TestFoundryTestingFramework:
    """Test the testing framework itself"""
    
    @pytest.mark.asyncio
    async def test_mock_foundry_client(self):
        """Test mock Foundry client"""
        mock_client = MockFoundryClient()
        
        headers = await mock_client.get_auth_headers()
        assert "Authorization" in headers
        
        config = {"name": "test_app", "template": "dashboard"}
        result = await mock_client.create_workshop_app(config)
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_foundry_test_harness(self):
        """Test Foundry test harness"""
        harness = FoundryTestHarness()
        
        async def test_function(input_value):
            return {"result": input_value * 2}
        
        test_cases = [
            {"inputs": {"input_value": 5}, "expected": {"result": 10}},
            {"inputs": {"input_value": 3}, "expected": {"result": 6}}
        ]
        
        results = await harness.test_function(test_function, test_cases)
        assert results["passed"] == 2
        assert results["failed"] == 0

if __name__ == "__main__":
    pytest.main([__file__])
