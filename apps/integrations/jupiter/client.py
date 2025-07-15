import requests
from .exceptions import (
    JupiterError,
    JupiterRateLimitError,
    JupiterConnectionError
)

class JupiterClient:
    """Client for interacting with Jupiter Token API V2"""
    
    BASE_URL = "https://lite-api.jup.ag/"

    def _make_request(self, endpoint, params=None):
        """
        Make HTTP request to Jupiter Token API V2
        
        Args:
            endpoint: API endpoint (without base url)
            params: Query parameters dict
        Returns:
            JSON response data
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        headers = {
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        except requests.exceptions.ConnectionError:
            raise JupiterConnectionError("Failed to connect to Jupiter API")
        except requests.exceptions.Timeout:
            raise JupiterConnectionError("Jupiter API request timed out")

        if response.status_code != 200:
            raise JupiterError(f"HTTP error: {response.status_code}")
        
        try:
            return response.json()
        except ValueError:
            raise JupiterError("Invalid JSON response from API")

    def get_tagged_coins(self):
        """
        Get list of verified tokens using Token API V2
        
        Returns:
            List of verified token data with decimals information
        """
        endpoint = "tokens/v2/tag"
        params = {"query": "verified"}
        
        return self._make_request(endpoint, params)
