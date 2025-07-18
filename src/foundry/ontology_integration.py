"""
Palantir Ontology SDK Integration for Transportation Domain Objects
Defines business entities and relationships for RaiderBot
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

try:
    from ontology_sdk import FoundryClient
    from ontology_sdk.ontology.objects import ObjectType, LinkType
    ONTOLOGY_SDK_AVAILABLE = True
except ImportError:
    ONTOLOGY_SDK_AVAILABLE = False
    print("Warning: ontology_sdk not available. Using mock implementation.")

class TransportationObjectType(Enum):
    TRANSPORTATION_ORDER = "TransportationOrder"
    FLEET_VEHICLE = "FleetVehicle"
    DELIVERY_ROUTE = "DeliveryRoute"
    SAFETY_INCIDENT = "SafetyIncident"
    DRIVER = "Driver"
    CUSTOMER = "Customer"

@dataclass
class TransportationOrder:
    """Transportation order domain object"""
    order_id: str
    customer_id: str
    pickup_location: str
    delivery_location: str
    status: str
    created_date: datetime
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    assigned_vehicle_id: Optional[str] = None
    assigned_driver_id: Optional[str] = None
    
    def to_ontology_object(self) -> Dict[str, Any]:
        return {
            "objectType": TransportationObjectType.TRANSPORTATION_ORDER.value,
            "properties": {
                "orderId": self.order_id,
                "customerId": self.customer_id,
                "pickupLocation": self.pickup_location,
                "deliveryLocation": self.delivery_location,
                "status": self.status,
                "createdDate": self.created_date.isoformat(),
                "scheduledDate": self.scheduled_date.isoformat() if self.scheduled_date else None,
                "completedDate": self.completed_date.isoformat() if self.completed_date else None,
                "assignedVehicleId": self.assigned_vehicle_id,
                "assignedDriverId": self.assigned_driver_id
            }
        }

@dataclass
class FleetVehicle:
    """Fleet vehicle domain object"""
    vehicle_id: str
    vehicle_type: str
    license_plate: str
    capacity: float
    status: str
    current_location: Optional[str] = None
    assigned_driver_id: Optional[str] = None
    last_maintenance_date: Optional[datetime] = None
    
    def to_ontology_object(self) -> Dict[str, Any]:
        return {
            "objectType": TransportationObjectType.FLEET_VEHICLE.value,
            "properties": {
                "vehicleId": self.vehicle_id,
                "vehicleType": self.vehicle_type,
                "licensePlate": self.license_plate,
                "capacity": self.capacity,
                "status": self.status,
                "currentLocation": self.current_location,
                "assignedDriverId": self.assigned_driver_id,
                "lastMaintenanceDate": self.last_maintenance_date.isoformat() if self.last_maintenance_date else None
            }
        }

@dataclass
class DeliveryRoute:
    """Delivery route domain object"""
    route_id: str
    route_name: str
    start_location: str
    end_location: str
    waypoints: List[str]
    estimated_duration: int
    distance_miles: float
    assigned_vehicle_id: Optional[str] = None
    status: str = "planned"
    
    def to_ontology_object(self) -> Dict[str, Any]:
        return {
            "objectType": TransportationObjectType.DELIVERY_ROUTE.value,
            "properties": {
                "routeId": self.route_id,
                "routeName": self.route_name,
                "startLocation": self.start_location,
                "endLocation": self.end_location,
                "waypoints": self.waypoints,
                "estimatedDuration": self.estimated_duration,
                "distanceMiles": self.distance_miles,
                "assignedVehicleId": self.assigned_vehicle_id,
                "status": self.status
            }
        }

@dataclass
class SafetyIncident:
    """Safety incident domain object"""
    incident_id: str
    incident_type: str
    severity: str
    description: str
    location: str
    incident_date: datetime
    involved_vehicle_id: Optional[str] = None
    involved_driver_id: Optional[str] = None
    resolved: bool = False
    
    def to_ontology_object(self) -> Dict[str, Any]:
        return {
            "objectType": TransportationObjectType.SAFETY_INCIDENT.value,
            "properties": {
                "incidentId": self.incident_id,
                "incidentType": self.incident_type,
                "severity": self.severity,
                "description": self.description,
                "location": self.location,
                "incidentDate": self.incident_date.isoformat(),
                "involvedVehicleId": self.involved_vehicle_id,
                "involvedDriverId": self.involved_driver_id,
                "resolved": self.resolved
            }
        }

class OntologyManager:
    """Manager for Palantir Ontology operations"""
    
    def __init__(self, foundry_client):
        self.foundry_client = foundry_client
        self.ontology_client = self._init_ontology_client()
    
    def _init_ontology_client(self):
        """Initialize ontology client"""
        if ONTOLOGY_SDK_AVAILABLE and self.foundry_client:
            return self.foundry_client.ontology
        return None
    
    async def create_transportation_order(self, order: TransportationOrder) -> Dict[str, Any]:
        """Create transportation order in ontology"""
        if self.ontology_client:
            try:
                result = await self.ontology_client.objects.TransportationOrder.create(
                    order.to_ontology_object()
                )
                return {"success": True, "object_rid": result.rid}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "object_rid": f"mock_order_{order.order_id}",
                "note": "Mock ontology implementation"
            }
    
    async def create_fleet_vehicle(self, vehicle: FleetVehicle) -> Dict[str, Any]:
        """Create fleet vehicle in ontology"""
        if self.ontology_client:
            try:
                result = await self.ontology_client.objects.FleetVehicle.create(
                    vehicle.to_ontology_object()
                )
                return {"success": True, "object_rid": result.rid}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "object_rid": f"mock_vehicle_{vehicle.vehicle_id}",
                "note": "Mock ontology implementation"
            }
    
    async def get_active_orders(self) -> List[Dict[str, Any]]:
        """Get active transportation orders"""
        if self.ontology_client:
            try:
                orders = await self.ontology_client.objects.TransportationOrder.where(
                    self.ontology_client.objects.TransportationOrder.status == "active"
                )
                return [order.properties for order in orders]
            except Exception as e:
                return []
        else:
            return [
                {"orderId": "mock_001", "status": "active", "note": "Mock data"},
                {"orderId": "mock_002", "status": "active", "note": "Mock data"}
            ]
    
    async def get_fleet_vehicles(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get fleet vehicles, optionally filtered by status"""
        if self.ontology_client:
            try:
                if status:
                    vehicles = await self.ontology_client.objects.FleetVehicle.where(
                        self.ontology_client.objects.FleetVehicle.status == status
                    )
                else:
                    vehicles = await self.ontology_client.objects.FleetVehicle.all()
                return [vehicle.properties for vehicle in vehicles]
            except Exception as e:
                return []
        else:
            mock_vehicles = [
                {"vehicleId": "mock_v001", "status": "available", "note": "Mock data"},
                {"vehicleId": "mock_v002", "status": "in_transit", "note": "Mock data"}
            ]
            if status:
                return [v for v in mock_vehicles if v.get("status") == status]
            return mock_vehicles
    
    async def create_safety_incident(self, incident: SafetyIncident) -> Dict[str, Any]:
        """Create safety incident in ontology"""
        if self.ontology_client:
            try:
                result = await self.ontology_client.objects.SafetyIncident.create(
                    incident.to_ontology_object()
                )
                return {"success": True, "object_rid": result.rid}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "object_rid": f"mock_incident_{incident.incident_id}",
                "note": "Mock ontology implementation"
            }
