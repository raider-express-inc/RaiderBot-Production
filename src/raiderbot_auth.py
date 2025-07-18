"""
RaiderBot Palantir Authentication Module

Implements proper Palantir token-based authentication with OAuth flow,
token refresh logic, and security context handling for Foundry Functions.
"""

import os
import time
import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class AuthToken:
    """Represents a Palantir authentication token with metadata."""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None


class PalantirAuthError(Exception):
    """Base exception for Palantir authentication errors."""
    pass


class TokenExpiredError(PalantirAuthError):
    """Raised when an authentication token has expired."""
    pass


class AuthenticationFailedError(PalantirAuthError):
    """Raised when authentication fails due to invalid credentials."""
    pass


class PalantirAuthenticator:
    """
    Handles Palantir Foundry authentication with OAuth 2.0 flow,
    token refresh, and security context management.
    """
    
    def __init__(
        self,
        base_url: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id or os.getenv('FOUNDRY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('FOUNDRY_CLIENT_SECRET')
        self.token = token or os.getenv('FOUNDRY_TOKEN')
        
        self._current_token: Optional[AuthToken] = None
        self._token_lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        
        if self.token:
            self._current_token = AuthToken(
                access_token=self.token,
                expires_at=datetime.now() + timedelta(hours=24)  # Default 24h expiry
            )
    
    async def get_valid_token(self) -> str:
        """
        Get a valid authentication token, refreshing if necessary.
        
        Returns:
            str: Valid access token
            
        Raises:
            AuthenticationFailedError: If authentication fails
            TokenExpiredError: If token cannot be refreshed
        """
        async with self._token_lock:
            if self._is_token_valid():
                return self._current_token.access_token
            
            if self._current_token and self._current_token.refresh_token:
                try:
                    await self._refresh_token()
                    return self._current_token.access_token
                except Exception as e:
                    self.logger.warning(f"Token refresh failed: {e}")
            
            await self._authenticate()
            return self._current_token.access_token
    
    def _is_token_valid(self) -> bool:
        """Check if current token is valid and not expired."""
        if not self._current_token:
            return False
        
        if not self._current_token.expires_at:
            return True  # No expiry set, assume valid
        
        buffer_time = timedelta(minutes=5)
        return datetime.now() + buffer_time < self._current_token.expires_at
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _authenticate(self) -> None:
        """
        Perform OAuth 2.0 authentication flow.
        
        Raises:
            AuthenticationFailedError: If authentication fails
        """
        if not self.client_id or not self.client_secret:
            if self.token:
                self._current_token = AuthToken(
                    access_token=self.token,
                    expires_at=datetime.now() + timedelta(hours=24)
                )
                return
            else:
                raise AuthenticationFailedError(
                    "No authentication credentials provided. "
                    "Set FOUNDRY_TOKEN or FOUNDRY_CLIENT_ID/FOUNDRY_CLIENT_SECRET"
                )
        
        auth_url = f"{self.base_url}/oauth2/token"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    auth_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "scope": "api:read api:write"
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self._current_token = AuthToken(
                        access_token=token_data["access_token"],
                        refresh_token=token_data.get("refresh_token"),
                        expires_at=datetime.now() + timedelta(
                            seconds=token_data.get("expires_in", 3600)
                        ),
                        token_type=token_data.get("token_type", "Bearer"),
                        scope=token_data.get("scope")
                    )
                    
                    self.logger.info("Successfully authenticated with Palantir Foundry")
                    
                else:
                    error_msg = f"Authentication failed: {response.status_code} {response.text}"
                    self.logger.error(error_msg)
                    raise AuthenticationFailedError(error_msg)
                    
            except httpx.RequestError as e:
                error_msg = f"Network error during authentication: {e}"
                self.logger.error(error_msg)
                raise AuthenticationFailedError(error_msg)
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=5)
    )
    async def _refresh_token(self) -> None:
        """
        Refresh the current authentication token.
        
        Raises:
            TokenExpiredError: If token refresh fails
        """
        if not self._current_token or not self._current_token.refresh_token:
            raise TokenExpiredError("No refresh token available")
        
        refresh_url = f"{self.base_url}/oauth2/token"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    refresh_url,
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": self._current_token.refresh_token,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self._current_token = AuthToken(
                        access_token=token_data["access_token"],
                        refresh_token=token_data.get("refresh_token", self._current_token.refresh_token),
                        expires_at=datetime.now() + timedelta(
                            seconds=token_data.get("expires_in", 3600)
                        ),
                        token_type=token_data.get("token_type", "Bearer"),
                        scope=token_data.get("scope")
                    )
                    
                    self.logger.info("Successfully refreshed Palantir authentication token")
                    
                else:
                    error_msg = f"Token refresh failed: {response.status_code} {response.text}"
                    self.logger.error(error_msg)
                    raise TokenExpiredError(error_msg)
                    
            except httpx.RequestError as e:
                error_msg = f"Network error during token refresh: {e}"
                self.logger.error(error_msg)
                raise TokenExpiredError(error_msg)
    
    async def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dict[str, str]: Headers with authorization token
        """
        token = await self.get_valid_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def validate_token(self) -> bool:
        """
        Validate current token by making a test API call.
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            headers = await self.get_auth_headers()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/user/me",
                    headers=headers,
                    timeout=10.0
                )
                
                return response.status_code == 200
                
        except Exception as e:
            self.logger.warning(f"Token validation failed: {e}")
            return False
    
    def get_security_context(self) -> Dict[str, Any]:
        """
        Get security context for Foundry Function calls.
        
        Returns:
            Dict[str, Any]: Security context metadata
        """
        if not self._current_token:
            return {}
        
        return {
            "token_type": self._current_token.token_type,
            "scope": self._current_token.scope,
            "expires_at": self._current_token.expires_at.isoformat() if self._current_token.expires_at else None,
            "authenticated_at": datetime.now().isoformat()
        }


_global_authenticator: Optional[PalantirAuthenticator] = None


async def get_authenticator() -> PalantirAuthenticator:
    """
    Get or create the global Palantir authenticator instance.
    
    Returns:
        PalantirAuthenticator: Configured authenticator instance
    """
    global _global_authenticator
    
    if _global_authenticator is None:
        base_url = os.getenv('FOUNDRY_BASE_URL', 'https://raiderexpress.palantirfoundry.com')
        _global_authenticator = PalantirAuthenticator(base_url=base_url)
    
    return _global_authenticator


async def get_auth_headers() -> Dict[str, str]:
    """
    Convenience function to get authentication headers.
    
    Returns:
        Dict[str, str]: Headers with authorization token
    """
    authenticator = await get_authenticator()
    return await authenticator.get_auth_headers()
