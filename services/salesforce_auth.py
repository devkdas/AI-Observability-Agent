"""
Salesforce Authentication Service for Copado Integration
Handles OAuth authentication with Salesforce/Copado orgs
"""

import os
import logging
import aiohttp
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SalesforceAuth:
    """Handle Salesforce OAuth authentication"""
    
    def __init__(self):
        self.instance_url = os.getenv("COPADO_SANDBOX_URL", "https://copadotrial44223329.my.salesforce.com")
        self.username = os.getenv("COPADO_USERNAME")
        self.password = os.getenv("COPADO_PASSWORD")
        self.session_id = os.getenv("COPADO_SANDBOX_API_KEY")  # This is actually a session ID
        self.session = None
        self.access_token = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def get_access_token(self) -> Optional[str]:
        """Get valid access token for Salesforce API calls"""
        if self.access_token:
            return self.access_token
            
        # Try session ID first (if it's actually a session ID)
        if self.session_id and len(self.session_id) > 50:
            # Test if session ID works directly
            if await self._test_session_id():
                self.access_token = self.session_id
                return self.access_token
        
        # Try OAuth flow if we have credentials
        if self.username and self.password:
            token = await self._oauth_login()
            if token:
                self.access_token = token
                return self.access_token
        
        return None
    
    async def _test_session_id(self) -> bool:
        """Test if the provided session ID works"""
        try:
            headers = {
                "Authorization": f"Bearer {self.session_id}",
                "Content-Type": "application/json"
            }
            
            async with self.session.get(
                f"{self.instance_url}/services/data/v58.0/",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status == 200
                
        except Exception as e:
            logger.debug(f"Session ID test failed: {e}")
            return False
    
    async def _oauth_login(self) -> Optional[str]:
        """Perform OAuth login using username/password"""
        try:
            # Get OAuth credentials from environment variables
            client_id = os.getenv("SALESFORCE_CLIENT_ID")
            client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                logger.warning("Salesforce OAuth credentials not configured")
                return None
            
            auth_data = {
                "grant_type": "password",
                "client_id": client_id,
                "client_secret": client_secret,
                "username": self.username,
                "password": self.password
            }
            
            async with self.session.post(
                f"{self.instance_url}/services/oauth2/token",
                data=auth_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("access_token")
                else:
                    logger.debug(f"OAuth login failed: {response.status}")
                    return None
                    
        except Exception as e:
            logger.debug(f"OAuth login error: {e}")
            return None
    
    async def make_api_call(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make authenticated API call to Salesforce"""
        access_token = await self.get_access_token()
        if not access_token:
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with self.session.get(
                f"{self.instance_url}{endpoint}",
                headers=headers,
                params=params or {},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.debug(f"API call failed: {response.status}")
                    return None
                    
        except Exception as e:
            logger.debug(f"API call error: {e}")
            return None
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
