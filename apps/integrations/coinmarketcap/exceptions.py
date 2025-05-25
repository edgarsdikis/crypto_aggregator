class CoinMarketCapError(Exception):
    """Base exception for CoinMarketCap API errors"""
    pass

class CoinMarketCapApiError(CoinMarketCapError):
    """Raised when API key is invalid or missing"""
    pass

class CoinMarketCapRateLimitError(CoinMarketCapError):
    """Raised when rate limit is exceeded"""
    pass

class CoinMarketCapConnectionError(CoinMarketCapError):
    """Raised when unable to connect to API"""
    pass
