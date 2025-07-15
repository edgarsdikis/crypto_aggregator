import requests
from django.conf import settings
from .exceptions import AlchemyError, AlchemyApiError, AlchemyConnectionError, AlchemyInvalidWalletError, AlchemyRateLimitError

class AlchemyClient:
    """Client for interacting with Alchemy API"""

    BASE_URL = "https://api.g.alchemy.com/data/v1/"

    def __init__(self, api_key=None):
        """
        Initialize the Client with API key

        Args:
            api_key: Alchemy API key (defaults to settings)
        """
        self.api_key = api_key or getattr(settings, "ALCHEMY_API_KEY", None)

        # Validate API key exists
        if not self.api_key:
            raise AlchemyError("Alchemy API key is required")

    def _make_request(self, endpoint, data=None):
        """
        Make HTTP request to Alchemy API

        Args:
            endpoint: API endpoint (without base URL)
            data: JSON data for POST request

        Returns:
            JSON response data

        Raise:
            Various AlchemyError subclasses
        """

        url = f"{self.BASE_URL}{self.api_key}{endpoint}"

        headers = {
                "Content-Type": "application/json"
                }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
        except requests.exceptions.ConnectionError:
            raise AlchemyConnectionError("Failed to connect to Alchemy API")
        except requests.exceptions.Timeout:
            raise AlchemyConnectionError("Alchemy API request timed out")

        # Handle rate limiting
        if response.status_code == 429:
            raise AlchemyRateLimitError("Rate limit exceeded")

        # Handle invalid wallet/bad request
        if response.status_code == 400:
            raise AlchemyInvalidWalletError("Invalid wallet address or request")

        # Handle authentication errors
        if response.status_code == 401:
            raise AlchemyApiError("Invalid API key")

        # Hanlde other errors
        if response.status_code != 200:
            try:
                error_data = response.json()
                if 'error' in error_data and 'message' in error_data['error']:
                    error_msg = error_data['error']['message']
                else:
                    error_msg = f"HTTP {response.status_code}"
                raise AlchemyApiError(f"API error: {error_msg}")
            except ValueError:
                raise AlchemyApiError(f"HTTP error: {response.status_code}")

        try:
            return response.json()
        except ValueError:
            raise AlchemyError("Invalid JSON response from API")

    def get_wallet_balances(self, address, networks):
        """
        Get token balances for wallet across all supported chains
        Args:
            address: Wallet address
            networks: List of network names

        Return:
            Dictionary with wallet balance data
        """
        endpoint = "/assets/tokens/by-address"
        
        request_data = {
                "addresses": [
                    {
                        "address": address,
                        "networks": networks
                        }
                    ]
                }

        response_data = self._make_request(endpoint, request_data)
        return response_data.get("data", {})
