from .base import *

DEBUG = True  # Can be True in develop for easier debugging
ALLOWED_HOSTS = ['https://decen-develop.onrender.com']  # Update with your develop domain

# Security settings - slightly relaxed for develop environment
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://decen-develop.onrender.com',  # Update with your develop frontend
    'http://localhost:5173'  # Allow local frontend development
]
CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://decen-develop.onrender.com',  # Backend
    'https://develop.yourdomain.com',  # Frontend
    'http://localhost:5173'  # Local development
]
