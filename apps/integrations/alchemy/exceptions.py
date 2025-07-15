class AlchemyError(Exception):
    """Base exception for Alchemy API error"""
    pass

class AlchemyApiError(AlchemyError):
    """Raised when API return an error response"""
    pass

class AlchemyRateLimitError(AlchemyError):
    """Raised when rate limit is exceeded"""
    pass

class AlchemyConnectionError(AlchemyError):
    """Raised when unable to connect to API"""
    pass

class AlchemyInvalidWalletError(AlchemyError):
    """Raised when wallet address is invalid or not found"""
    pass
