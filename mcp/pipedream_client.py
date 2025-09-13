import os
import httpx
from typing import Any, Dict, Optional


class PipedreamClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("PIPEDREAM_API_KEY")
        if not self.api_key:
            raise RuntimeError("PIPEDREAM_API_KEY is required")
        self.base_url = base_url or os.getenv(
            "PIPEDREAM_API_BASE", "https://api.pipedream.com/v1"
        )
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def get_me(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                f"{self.base_url}/users/me",
                headers=self._headers,
                follow_redirects=False,
            )
            r.raise_for_status()
            return r.json()

    async def list_sources(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get(
                f"{self.base_url}/sources",
                headers=self._headers,
                follow_redirects=False,
            )
            r.raise_for_status()
            return r.json()

    async def emit_event(
        self, source_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{self.base_url}/sources/{source_id}/events",
                json=payload,
                headers=self._headers,
                follow_redirects=False,
            )
            r.raise_for_status()
            return r.json()
