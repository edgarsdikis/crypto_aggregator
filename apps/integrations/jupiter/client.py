import requests
from .exceptions import (
        JupiterError,
        JupiterRateLimitError,
        JupiterConnectionError
        )

class JupiterClient:
    """Client for interacting witn Jupiter API"""

    BASE_URL = "https://lite-api.jup.ag/"

    def _make_request(self, endpoint, tag):
        """
        Make HTTP request to Jupiter API

        Args:
            endpoint: API endpoint (without base url)
            tag: Filter for response
        Returns:
            JSON response data

        Raises:
            Various JupiterError subclasses
        """
        url = f"{self.BASE_URL}{endpoint}{tag}"

        headers = {
                'Accept': 'application/json'
                }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
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
        Get list of all coins with metadata and decimals
        Args:
            tag:
                A list of one or more tags to filter the response

        Returns:
            List of coin data
        """
        tag = 'verified,lst,token-2022'
        endpoint = "tokens/v1/tagged/"

        return self._make_request(endpoint, tag)

