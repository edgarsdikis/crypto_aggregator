import requests
import time
from django.conf import settings
from .exceptions import (
        CoinGeckoError,
        CoinGeckoApiError,
        CoinGeckoRateLimitError,
        CoinGeckoConnectionError
        )

class CoinGeckoClient:
    """Client for interacting with Coingecko API"""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key=None):
        """
        Initialize the Client with API key

        Args:
            api_key: Coingecko API key (defaults to settings)
        """
        self.api_key = api_key or getattr(settings, "COINGECKO_API_KEY", None)

        # Validate API key exists
        if not self.api_key:
            raise CoinGeckoError("Coingecko API key is rerquired")

    def _make_request(self, endpoint, params=None):
        """
        Make HTTP request to CoinGecko API

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            Various CoinGeckoError subclasses
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": self.api_key
                }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        except requests.exceptions.ConnectionError:
            raise CoinGeckoConnectionError("Failed to connect to Coingecko API")
        except requests.exceptions.Timeout:
            raise CoinGeckoConnectionError("Coingecko API request timed out")

        # Handle rate limiting
        if response.status_code == 429:
            raise CoinGeckoRateLimitError("Rate limit exceeded")

        # Handle other errors
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f'HTTP {response.status_code}')
                raise CoinGeckoApiError(f"API error: {error_msg}")
            except ValueError:
                raise CoinGeckoApiError(f"HTTP error: {response.status_code}")

        try:
            return response.json()
        except ValueError:
            raise CoinGeckoError("Invalid JSON response from API")

    def get_coins_list(self, include_platform=True):
        """
        Get list of all CoinGecko coins with IDs, symbols, names

        Args:
            include_platform: Whether to include platform contract addresses for every token

        Returns:
            List of coin data
        """
        endpoint = "/coins/list"
        params = {}

        if include_platform:
            params["include_platform"] = "true"

        return self._make_request(endpoint, params)
    
    def get_coins_markets_single_page(self, page=1, vs_currency='usd', per_page=250, order='market_cap_desc', precision='full'):
        """
        Get market data for a single page to minimize memory usage
        
        Returns: Single page of coin market data or empty list if no more data
        """
        endpoint = "/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'per_page': per_page,
            'page': page,
            'order': order,
            'sparkline': 'false',
            'price_change_percentage': '1h',
            'precision': precision
        }
        
        try:
            return self._make_request(endpoint, params)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            return []
