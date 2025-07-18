"""
Palantir SLS Logging Integration for RaiderBot
Implements structured logging with correlation IDs and metrics emission
"""

import os
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import structlog
from contextlib import contextmanager

try:
    from slslogging import install_metrics, MetricArg
    SLS_AVAILABLE = True
except ImportError:
    SLS_AVAILABLE = False
    print("Warning: slslogging not available. Using structlog fallback.")

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

if SLS_AVAILABLE:
    install_metrics(origin_prefix="raiderbot:service")

class CorrelationContext:
    """Thread-local correlation context for request tracking"""
    _context: Dict[str, Any] = {}
    
    @classmethod
    def get_correlation_id(cls) -> str:
        return cls._context.get('correlation_id', str(uuid.uuid4()))
    
    @classmethod
    def set_correlation_id(cls, correlation_id: str):
        cls._context['correlation_id'] = correlation_id
    
    @classmethod
    def get_context(cls) -> Dict[str, Any]:
        return cls._context.copy()

@contextmanager
def correlation_context(correlation_id: Optional[str] = None):
    """Context manager for correlation ID tracking"""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    old_context = CorrelationContext._context.copy()
    CorrelationContext.set_correlation_id(correlation_id)
    
    try:
        yield correlation_id
    finally:
        CorrelationContext._context = old_context

def get_structured_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger with correlation context"""
    logger = structlog.get_logger(name)
    return logger.bind(
        correlation_id=CorrelationContext.get_correlation_id(),
        service="raiderbot",
        environment=os.getenv("ENVIRONMENT", "development")
    )

def emit_metric(metric_name: str, value: float, dimensions: Optional[Dict[str, str]] = None):
    """Emit metrics using SLS logging or fallback"""
    if SLS_AVAILABLE:
        logger = get_structured_logger("metrics")
        logger.info(MetricArg(metric_name, value, dimensions=dimensions or {}))
    else:
        logger = get_structured_logger("metrics")
        logger.info("metric_emission", 
                   metric_name=metric_name, 
                   value=value, 
                   dimensions=dimensions or {})

def log_function_execution(function_name: str, execution_time: float, success: bool = True):
    """Log function execution with metrics"""
    logger = get_structured_logger("function_execution")
    
    logger.info(
        "function_executed",
        function_name=function_name,
        execution_time=execution_time,
        success=success,
        timestamp=datetime.now().isoformat()
    )
    
    emit_metric(
        "function_execution_time",
        execution_time,
        dimensions={
            "function": function_name,
            "success": str(success)
        }
    )
