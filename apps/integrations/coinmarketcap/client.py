import requests
from django.conf import settings
from .exceptions import (
        CoinMarketCapError,
        CoinMarketCapApiError,
        CoinMarketCapConnectionError,
        CoinMarketCapRateLimitError
        )

class CoinMarketCapClient:
    """Client for interacting with CoinMarketCap API"""
    
    BASE_URL = "https://pro-api.coinmarketcap.com"

    def __init__(self, api_key=None):
        """
        Initialize the Client with API key

        Args:
            api_key: CoinMarketCap API key (defaults to settings)
        """
        self.api_key = api_key or getattr(settings, 'COINMARKETCAP_API_KEY', None)

        # Validate API key exists
        if not self.api_key:
            raise CoinMarketCapError('CoinMarketCap API key is required')

    def _make_request(self, endpoint, params=None):
        """
        Make HTTP request to CoinMarketCap API
        
        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            Various CoinMarketCapError subclasses
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
                'X-CMC_PRO_API_KEY': self.api_key,
                'Accept': 'application/json'
                }
        try:
            response = requests.get(url, headers=headers,params=params, timeout=30)
        except requests.exceptions.ConnectionError:
            raise CoinMarketCapConnectionError("Failed to connect to CoinMarketCap API")
        except requests.exceptions.Timeout:
            raise CoinMarketCapConnectionError("CoinMarketCap API request timed out")

        if response.status_code == 429:
            raise CoinMarketCapRateLimitError("Rate limit exceeed")
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_code = error_data["status"]["error_code"]
                error_msg = error_data["status"]["error_message"]
                raise CoinMarketCapApiError(f"API error {error_code}: {error_msg}")
            except ValueError:
                raise CoinMarketCapApiError(f"Cant parse the JSON: {response.status_code}")

        try:
            return response.json()
        except ValueError:
            raise CoinMarketCapError("Invalid JSON response from API")

    def get_cmc_crypto_map(self, start=1, limit=5000, sort="id"):
        """
        Get a mapping of all cryptocurrencies to unique CoinMarketCap IDs
        
        Args:
            start: Starting record(default: 1)
            limit: Number of results (default: 5000, max: 5000)
            sort: Sort field (default: "id")

        Returns:
            List of cryptocurrency mappings
        """
        endpoint = "/v1/cryptocurrency/map"

        params = {
                'start': start,
                'limit': limit,
                'sort': sort
                }

        response_data = self._make_request(endpoint, params)

        return response_data['data']
        # TODO: Implement pagination to fetch all tokens (CMC has 27,000+)

