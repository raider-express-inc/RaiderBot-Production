"""
Enhanced Palantir-Specific Error Handling for RaiderBot
Implements error hierarchy, retry logic, and monitoring integration
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Type
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.raiderbot_auth import PalantirAuthError, TokenExpiredError, AuthenticationFailedError
from src.foundry.sls_logging import get_structured_logger, emit_metric

class PalantirResourceError(PalantirAuthError):
    """Raised when resource access is denied or unavailable"""
    pass

class PalantirRateLimitError(PalantirAuthError):
    """Raised when rate limits are exceeded"""
    pass

class PalantirTimeoutError(PalantirAuthError):
    """Raised when requests timeout"""
    pass

class PalantirDataError(PalantirAuthError):
    """Raised when data validation or processing fails"""
    pass

class PalantirWorkshopError(PalantirAuthError):
    """Raised when Workshop operations fail"""
    pass

class PalantirOntologyError(PalantirAuthError):
    """Raised when Ontology operations fail"""
    pass

class ErrorHandler:
    """Centralized error handling for Palantir operations"""
    
    def __init__(self):
        self.logger = get_structured_logger("error_handler")
        self.error_counts = {}
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with structured context"""
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        self.logger.error(
            "palantir_error_occurred",
            error_type=error_type,
            error_message=str(error),
            error_count=self.error_counts[error_type],
            context=context or {},
            timestamp=datetime.now().isoformat()
        )
        
        emit_metric(
            "palantir_error_count",
            1,
            dimensions={
                "error_type": error_type,
                "service": "raiderbot"
            }
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((PalantirTimeoutError, PalantirRateLimitError))
    )
    async def execute_with_retry(self, operation, *args, **kwargs):
        """Execute operation with retry logic for transient errors"""
        start_time = time.time()
        try:
            result = await operation(*args, **kwargs)
            
            duration = time.time() - start_time
            emit_metric(
                "operation_success_duration",
                duration,
                dimensions={"operation": operation.__name__}
            )
            
            return result
            
        except (PalantirTimeoutError, PalantirRateLimitError) as e:
            self.log_error(e, {"operation": operation.__name__, "retry_attempt": True})
            raise
        except Exception as e:
            self.log_error(e, {"operation": operation.__name__, "fatal": True})
            raise
    
    def handle_http_error(self, status_code: int, response_text: str, url: str = "") -> Exception:
        """Convert HTTP errors to appropriate Palantir exceptions"""
        context = {"status_code": status_code, "url": url}
        
        if status_code == 401:
            error = AuthenticationFailedError(f"Authentication failed: {response_text}")
        elif status_code == 403:
            error = PalantirResourceError(f"Resource access denied: {response_text}")
        elif status_code == 404:
            error = PalantirResourceError(f"Resource not found: {response_text}")
        elif status_code == 429:
            error = PalantirRateLimitError(f"Rate limit exceeded: {response_text}")
        elif status_code >= 500:
            error = PalantirTimeoutError(f"Server error: {response_text}")
        else:
            error = PalantirDataError(f"Request failed ({status_code}): {response_text}")
        
        self.log_error(error, context)
        return error
    
    def handle_ontology_error(self, error: Exception, operation: str) -> Exception:
        """Handle ontology-specific errors"""
        if "not found" in str(error).lower():
            return PalantirOntologyError(f"Ontology object not found during {operation}: {error}")
        elif "permission" in str(error).lower():
            return PalantirResourceError(f"Insufficient permissions for {operation}: {error}")
        else:
            return PalantirOntologyError(f"Ontology operation failed ({operation}): {error}")
    
    def handle_workshop_error(self, error: Exception, operation: str) -> Exception:
        """Handle Workshop-specific errors"""
        if "workspace" in str(error).lower():
            return PalantirWorkshopError(f"Workshop workspace error during {operation}: {error}")
        elif "widget" in str(error).lower():
            return PalantirWorkshopError(f"Workshop widget error during {operation}: {error}")
        else:
            return PalantirWorkshopError(f"Workshop operation failed ({operation}): {error}")

class CircuitBreaker:
    """Circuit breaker pattern for Palantir API calls"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        self.logger = get_structured_logger("circuit_breaker")
    
    async def call(self, operation, *args, **kwargs):
        """Execute operation with circuit breaker protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.logger.info("circuit_breaker_half_open")
            else:
                raise PalantirTimeoutError("Circuit breaker is OPEN")
        
        try:
            result = await operation(*args, **kwargs)
            
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.logger.info("circuit_breaker_closed")
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.logger.error("circuit_breaker_opened", failure_count=self.failure_count)
            
            raise

error_handler = ErrorHandler()
circuit_breaker = CircuitBreaker()
