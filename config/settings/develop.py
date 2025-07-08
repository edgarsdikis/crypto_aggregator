from .base import *

DEBUG = False
ALLOWED_HOSTS = ['decen-develop.onrender.com']  # Update with your develop domain


# Reuse database connections instead of creating new ones
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# Limit concurrent database connections
DATABASES['default']['OPTIONS'] = {
    'MAX_CONNS': 3,  # Maximum 3 concurrent connections (down from default 20)
}

# Disable task result storage (saves memory)
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = None

# Use JSON serialization (more memory efficient than pickle)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

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
