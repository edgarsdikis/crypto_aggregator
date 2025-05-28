class CoinGeckoError(Exception):
    """Base exception for CoinGecko API errors"""
    pass

class CoinGeckoApiError(CoinGeckoError):
    """Raised when API key is invalid or missing"""
    pass

class CoinGeckoRateLimitError(CoinGeckoError):
    """Raised when rate limit is exceeded"""
    pass

class CoinGeckoConnectionError(CoinGeckoError):
    """Raised when unable to connect to API"""
    pass
