"""
Performance Optimization for Palantir Foundry Integration
Implements connection pooling, caching, and pagination
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
import httpx
from src.foundry.sls_logging import get_structured_logger, emit_metric

@dataclass
class CacheEntry:
    """Cache entry with TTL"""
    data: Any
    expires_at: datetime
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at

class MemoryCache:
    """In-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.logger = get_structured_logger("cache")
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                self.hit_count += 1
                self.logger.debug("cache_hit", key=key)
                emit_metric("cache_hit", 1, {"cache_type": "memory"})
                return entry.data
            else:
                del self.cache[key]
                self.logger.debug("cache_expired", key=key)
        
        self.miss_count += 1
        self.logger.debug("cache_miss", key=key)
        emit_metric("cache_miss", 1, {"cache_type": "memory"})
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value with TTL"""
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = CacheEntry(value, expires_at)
        self.logger.debug("cache_set", key=key, ttl=ttl)
    
    def clear(self) -> None:
        """Clear all cached entries"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
        self.logger.info("cache_cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests) if total_requests > 0 else 0
        
        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache)
        }

class ConnectionPool:
    """HTTP connection pool for Foundry API calls"""
    
    def __init__(self, max_connections: int = 20, max_keepalive: int = 5):
        self.limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive
        )
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        self.logger = get_structured_logger("connection_pool")
        self._client = None
    
    async def get_client(self) -> httpx.AsyncClient:
        """Get configured HTTP client with connection pooling"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                limits=self.limits,
                timeout=self.timeout,
                follow_redirects=True
            )
            self.logger.info("connection_pool_initialized", 
                           max_connections=self.limits.max_connections)
        
        return self._client
    
    async def close(self):
        """Close the connection pool"""
        if self._client:
            await self._client.aclose()
            self._client = None
            self.logger.info("connection_pool_closed")

class PaginationHelper:
    """Helper for paginated API responses"""
    
    def __init__(self, page_size: int = 100):
        self.page_size = page_size
        self.logger = get_structured_logger("pagination")
    
    async def paginate_results(
        self,
        fetch_function: Callable,
        max_pages: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Paginate through API results"""
        all_results = []
        page = 0
        
        start_time = time.time()
        
        while page < max_pages:
            try:
                page_start_time = time.time()
                
                results = await fetch_function(
                    offset=page * self.page_size,
                    limit=self.page_size,
                    **kwargs
                )
                
                page_duration = time.time() - page_start_time
                
                if not results:
                    self.logger.debug("pagination_complete", page=page, total_results=len(all_results))
                    break
                
                all_results.extend(results)
                page += 1
                
                self.logger.debug(
                    "pagination_page_fetched",
                    page=page,
                    results_count=len(results),
                    total_results=len(all_results),
                    page_duration=page_duration
                )
                
                emit_metric("pagination_page_duration", page_duration)
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error("pagination_error", page=page, error=str(e))
                break
        
        total_duration = time.time() - start_time
        
        emit_metric("pagination_total_results", len(all_results))
        emit_metric("pagination_total_duration", total_duration)
        
        self.logger.info(
            "pagination_complete",
            total_pages=page,
            total_results=len(all_results),
            total_duration=total_duration
        )
        
        return all_results
    
    async def paginate_with_cursor(
        self,
        fetch_function: Callable,
        cursor_field: str = "next_cursor",
        max_iterations: int = 50,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Paginate using cursor-based pagination"""
        all_results = []
        cursor = None
        iteration = 0
        
        while iteration < max_iterations:
            try:
                if cursor:
                    kwargs[cursor_field] = cursor
                
                response = await fetch_function(**kwargs)
                
                if not response or not response.get("data"):
                    break
                
                results = response["data"]
                all_results.extend(results)
                
                cursor = response.get(cursor_field)
                if not cursor:
                    break
                
                iteration += 1
                
                self.logger.debug(
                    "cursor_pagination_iteration",
                    iteration=iteration,
                    results_count=len(results),
                    total_results=len(all_results)
                )
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error("cursor_pagination_error", iteration=iteration, error=str(e))
                break
        
        return all_results

class QueryOptimizer:
    """Optimize database and API queries"""
    
    def __init__(self):
        self.logger = get_structured_logger("query_optimizer")
        self.query_cache = MemoryCache(default_ttl=600)
    
    def optimize_snowflake_query(self, query: str) -> str:
        """Optimize Snowflake queries for better performance"""
        optimized = query.strip()
        
        if not optimized.upper().startswith("SELECT"):
            return optimized
        
        if "LIMIT" not in optimized.upper():
            optimized += " LIMIT 1000"
        
        if "ORDER BY" in optimized.upper() and "LIMIT" in optimized.upper():
            pass
        elif "ORDER BY" not in optimized.upper() and len(optimized.split()) > 10:
            optimized = optimized.replace("LIMIT", "ORDER BY 1 LIMIT")
        
        self.logger.debug("query_optimized", original_length=len(query), optimized_length=len(optimized))
        
        return optimized
    
    async def execute_cached_query(self, query_func: Callable, cache_key: str, ttl: int = 300, *args, **kwargs):
        """Execute query with caching"""
        cached_result = self.query_cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        start_time = time.time()
        result = await query_func(*args, **kwargs)
        duration = time.time() - start_time
        
        self.query_cache.set(cache_key, result, ttl)
        
        emit_metric("query_execution_duration", duration)
        self.logger.info("query_executed_and_cached", cache_key=cache_key, duration=duration)
        
        return result

cache = MemoryCache()
connection_pool = ConnectionPool()
pagination_helper = PaginationHelper()
query_optimizer = QueryOptimizer()
