"""
Palantir AIP Integration for RaiderBot RAG Engine
Implements LLM integration with Palantir's model API
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from src.foundry.sls_logging import get_structured_logger, emit_metric
from src.foundry.performance_optimization import connection_pool, cache
from src.foundry.error_handling import error_handler

try:
    from foundry_sdk.v2.aip_agents.models import CreateCompletionRequest
    from foundry_sdk.v2.client import FoundryClient as FoundryClientV2
    FOUNDRY_V2_AVAILABLE = True
except ImportError:
    FOUNDRY_V2_AVAILABLE = False
    print("Warning: foundry_sdk.v2 not available. Using HTTP API fallback.")

class AIPModelClient:
    """Client for Palantir AIP model API"""
    
    def __init__(self, foundry_client):
        self.foundry_client = foundry_client
        self.logger = get_structured_logger("aip_model")
        self.base_url = getattr(foundry_client, 'foundry_url', 'https://raiderexpress.palantirfoundry.com')
    
    async def create_completion(
        self,
        prompt: str,
        model: str = "claude-3-sonnet",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create completion using Palantir AIP model API"""
        
        cache_key = f"completion:{hash(prompt)}:{model}:{temperature}"
        cached_result = cache.get(cache_key)
        if cached_result:
            self.logger.debug("aip_completion_cache_hit", model=model)
            return cached_result
        
        start_time = time.time()
        
        try:
            if FOUNDRY_V2_AVAILABLE and hasattr(self.foundry_client, 'aip_agents'):
                result = await self._sdk_completion(prompt, model, max_tokens, temperature, context)
            else:
                result = await self._http_completion(prompt, model, max_tokens, temperature, context)
            
            cache.set(cache_key, result, ttl=3600)
            
            duration = time.time() - start_time
            emit_metric("aip_completion_duration", duration, {"model": model})
            emit_metric("aip_completion_success", 1, {"model": model})
            
            self.logger.info(
                "aip_completion_success",
                model=model,
                prompt_length=len(prompt),
                response_length=len(result.get("text", "")),
                duration=duration
            )
            
            return result
            
        except Exception as e:
            emit_metric("aip_completion_error", 1, {"model": model})
            self.logger.error("aip_completion_error", model=model, error=str(e))
            raise error_handler.handle_http_error(500, str(e), "aip_completion")
    
    async def _sdk_completion(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        context: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Use official Foundry SDK v2 for completion"""
        try:
            request = CreateCompletionRequest(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            response = await self.foundry_client.aip_agents.create_completion(request)
            
            return {
                "text": response.text,
                "model": model,
                "source": "foundry_sdk_v2",
                "usage": getattr(response, 'usage', {}),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error("sdk_completion_error", error=str(e))
            raise
    
    async def _http_completion(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        context: Optional[List[str]]
    ) -> Dict[str, Any]:
        """HTTP API fallback for completion"""
        async with await connection_pool.get_client() as client:
            try:
                headers = {}
                if hasattr(self.foundry_client, 'get_auth_headers'):
                    headers = await self.foundry_client.get_auth_headers()
                
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                
                if context:
                    payload["context"] = context
                
                response = await client.post(
                    f"{self.base_url}/api/v2/aip/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data.get("text", ""),
                        "model": model,
                        "source": "http_api",
                        "usage": data.get("usage", {}),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    raise error_handler.handle_http_error(
                        response.status_code,
                        response.text,
                        f"{self.base_url}/api/v2/aip/completions"
                    )
                    
            except httpx.RequestError as e:
                self.logger.error("http_completion_network_error", error=str(e))
                raise
    
    async def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Create text embeddings for RAG"""
        cache_key = f"embedding:{hash(text)}:{model}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            async with await connection_pool.get_client() as client:
                headers = {}
                if hasattr(self.foundry_client, 'get_auth_headers'):
                    headers = await self.foundry_client.get_auth_headers()
                
                response = await client.post(
                    f"{self.base_url}/api/v2/aip/embeddings",
                    headers=headers,
                    json={
                        "model": model,
                        "input": text
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    embedding = data.get("data", [{}])[0].get("embedding", [])
                    cache.set(cache_key, embedding, ttl=7200)
                    return embedding
                else:
                    self.logger.error("embedding_api_error", status=response.status_code)
                    return []
                    
        except Exception as e:
            self.logger.error("embedding_error", error=str(e))
            return []

class RAGEngine:
    """Enhanced RAG engine with Palantir AIP integration"""
    
    def __init__(self, foundry_client):
        self.aip_client = AIPModelClient(foundry_client)
        self.logger = get_structured_logger("rag_engine")
        self.knowledge_base = []
    
    async def add_knowledge(self, documents: List[str]):
        """Add documents to knowledge base with embeddings"""
        for doc in documents:
            embedding = await self.aip_client.create_embedding(doc)
            self.knowledge_base.append({
                "text": doc,
                "embedding": embedding,
                "timestamp": datetime.now().isoformat()
            })
        
        self.logger.info("knowledge_added", document_count=len(documents))
    
    def _calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        if not embedding1 or not embedding2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant context for query"""
        if not self.knowledge_base:
            return []
        
        query_embedding = await self.aip_client.create_embedding(query)
        if not query_embedding:
            return []
        
        similarities = []
        for doc in self.knowledge_base:
            similarity = self._calculate_similarity(query_embedding, doc["embedding"])
            similarities.append((similarity, doc["text"]))
        
        similarities.sort(reverse=True)
        relevant_docs = [doc for _, doc in similarities[:top_k]]
        
        self.logger.debug("context_retrieved", query_length=len(query), context_count=len(relevant_docs))
        
        return relevant_docs
    
    async def generate_response(self, query: str, context: Optional[List[str]] = None) -> str:
        """Generate response using RAG with AIP models"""
        if context is None:
            context = await self.retrieve_relevant_context(query)
        
        context_text = "\n\n".join(context) if context else ""
        
        prompt = f"""
Based on the following context, please provide a helpful and accurate response to the user's query.

Context:
{context_text}

User Query: {query}

Response:"""
        
        result = await self.aip_client.create_completion(
            prompt=prompt,
            context=context,
            max_tokens=1500,
            temperature=0.7
        )
        
        response_text = result.get("text", "")
        
        emit_metric("rag_response_generated", 1, {
            "context_provided": str(bool(context)),
            "response_length": str(len(response_text))
        })
        
        return response_text
    
    async def generate_transportation_insights(self, data: Dict[str, Any]) -> str:
        """Generate transportation-specific insights"""
        context = [
            "Transportation industry best practices and KPIs",
            "Fleet management optimization strategies",
            "Route planning and delivery efficiency metrics",
            "Safety compliance and incident management"
        ]
        
        query = f"Analyze this transportation data and provide insights: {data}"
        
        return await self.generate_response(query, context)
