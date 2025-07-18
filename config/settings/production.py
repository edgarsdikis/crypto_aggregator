from .base import *

DEBUG = False
ALLOWED_HOSTS = ['decen-production.onrender.com']

# Reuse database connections instead of creating new ones
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# MEMORY OPTIMIZATION: Optimize sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour instead of 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# MEMORY OPTIMIZATION: Limit file upload memory usage
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB

# Tell Django to trust Render's proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://decen.app',
    'https://www.decen.app',
    'https://decen-production.onrender.com',
]
CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://decen-production.onrender.com',
    'https://decen.app',
    'https://www.decen.app',
]
