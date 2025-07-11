from .base import *

DEBUG = False
ALLOWED_HOSTS = ['decen-develop.onrender.com']

# Reuse database connections instead of creating new ones
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# MEMORY OPTIMIZATION: Optimize sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour instead of 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# MEMORY OPTIMIZATION: Limit file upload memory usage
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://decen-develop.onrender.com',
    'http://localhost:5173'
]
CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://decen-develop.onrender.com',
    'https://develop.yourdomain.com',
    'http://localhost:5173'
]
