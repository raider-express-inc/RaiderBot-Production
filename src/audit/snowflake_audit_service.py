"""
Snowflake Audit Logging Service
Comprehensive audit trail for all RaiderBot operations
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class AuditEventType(Enum):
    USER_LOGIN = "user_login"
    DASHBOARD_ACCESS = "dashboard_access"
    QUERY_EXECUTION = "query_execution"
    WORKSHOP_APP_CREATION = "workshop_app_creation"
    AGENT_INTERACTION = "agent_interaction"
    DATA_EXPORT = "data_export"
    SYSTEM_ERROR = "system_error"
    SECURITY_EVENT = "security_event"

class SnowflakeAuditService:
    """Comprehensive audit logging to Snowflake"""
    
    def __init__(self, snowflake_client):
        self.snowflake_client = snowflake_client
        self.audit_table = "AUDIT.RAIDERBOT_AUDIT_LOG"
        
    async def log_event(self, event_type: AuditEventType, user_id: str, details: Dict[str, Any]) -> bool:
        """Log audit event to Snowflake"""
        try:
            audit_record = {
                "event_id": f"{event_type.value}_{datetime.now().timestamp()}",
                "event_type": event_type.value,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "details": json.dumps(details),
                "session_id": details.get("session_id"),
                "ip_address": details.get("ip_address"),
                "user_agent": details.get("user_agent"),
                "success": details.get("success", True),
                "error_message": details.get("error_message"),
                "duration_ms": details.get("duration_ms"),
                "data_accessed": json.dumps(details.get("data_accessed", [])),
                "actions_performed": json.dumps(details.get("actions_performed", []))
            }
            
            if self.snowflake_client is None:
                print(f"AUDIT LOG: {audit_record}")
                return True
            
            cursor = self.snowflake_client.cursor()
            
            insert_sql = f"""
            INSERT INTO {self.audit_table} (
                event_id, event_type, user_id, timestamp, details,
                session_id, ip_address, user_agent, success, error_message,
                duration_ms, data_accessed, actions_performed
            ) VALUES (
                %(event_id)s, %(event_type)s, %(user_id)s, %(timestamp)s, %(details)s,
                %(session_id)s, %(ip_address)s, %(user_agent)s, %(success)s, %(error_message)s,
                %(duration_ms)s, %(data_accessed)s, %(actions_performed)s
            )
            """
            
            cursor.execute(insert_sql, audit_record)
            self.snowflake_client.commit()
            
            return True
            
        except Exception as e:
            print(f"Audit logging failed: {e}")
            return False
            
    async def log_user_interaction(self, user_id: str, interaction_type: str, details: Dict[str, Any]) -> bool:
        """Log user interaction with audit context"""
        if self.snowflake_client is None:
            print(f"AUDIT USER INTERACTION: {user_id} - {interaction_type} - {details}")
            return True
            
        return await self.log_event(
            AuditEventType.AGENT_INTERACTION,
            user_id,
            {
                **details,
                "interaction_type": interaction_type,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    async def log_data_access(self, user_id: str, tables_accessed: List[str], query: str) -> bool:
        """Log data access for compliance"""
        return await self.log_event(
            AuditEventType.QUERY_EXECUTION,
            user_id,
            {
                "tables_accessed": tables_accessed,
                "query": query,
                "data_classification": "operational",
                "access_reason": "business_intelligence"
            }
        )
        
    async def create_audit_tables(self) -> bool:
        """Create audit tables if they don't exist"""
        try:
            if self.snowflake_client is None:
                print("AUDIT TABLE CREATION: Would create audit tables in Snowflake")
                return True
                
            cursor = self.snowflake_client.cursor()
            
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.audit_table} (
                event_id VARCHAR(255) PRIMARY KEY,
                event_type VARCHAR(100) NOT NULL,
                user_id VARCHAR(100) NOT NULL,
                timestamp TIMESTAMP_NTZ NOT NULL,
                details VARIANT,
                session_id VARCHAR(255),
                ip_address VARCHAR(45),
                user_agent VARCHAR(500),
                success BOOLEAN DEFAULT TRUE,
                error_message VARCHAR(1000),
                duration_ms INTEGER,
                data_accessed VARIANT,
                actions_performed VARIANT,
                created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
            """
            
            cursor.execute(create_table_sql)
            self.snowflake_client.commit()
            
            return True
            
        except Exception as e:
            print(f"Failed to create audit tables: {e}")
            return False
            
    async def get_audit_report(self, user_id: Optional[str] = None, event_type: Optional[AuditEventType] = None, 
                              start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate audit report with filters"""
        try:
            where_conditions = []
            params = {}
            
            if user_id:
                where_conditions.append("user_id = %(user_id)s")
                params["user_id"] = user_id
                
            if event_type:
                where_conditions.append("event_type = %(event_type)s")
                params["event_type"] = event_type.value
                
            if start_date:
                where_conditions.append("timestamp >= %(start_date)s")
                params["start_date"] = start_date
                
            if end_date:
                where_conditions.append("timestamp <= %(end_date)s")
                params["end_date"] = end_date
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            query = f"""
            SELECT event_type, COUNT(*) as event_count, 
                   MIN(timestamp) as first_event, MAX(timestamp) as last_event
            FROM {self.audit_table}
            WHERE {where_clause}
            GROUP BY event_type
            ORDER BY event_count DESC
            """
            
            cursor = self.snowflake_client.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            return {
                "report_data": [dict(zip(columns, row)) for row in results],
                "total_events": sum(row[1] for row in results),
                "report_generated": datetime.now().isoformat(),
                "filters_applied": {
                    "user_id": user_id,
                    "event_type": event_type.value if event_type else None,
                    "date_range": f"{start_date} to {end_date}" if start_date and end_date else None
                }
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
