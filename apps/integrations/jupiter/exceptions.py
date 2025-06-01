class JupiterError(Exception):
    """Base exception for CoinGecko API errors"""
    pass

class JupiterRateLimitError(JupiterError):
    """Raised when rate limit is exceeded"""
    pass

class JupiterConnectionError(JupiterError):
    """Raised when unable to connect to API"""
    pass
