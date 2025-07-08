from .base import *

DEBUG = False
ALLOWED_HOSTS = ['decen-develop.onrender.com']

# Add this to your develop.py to guarantee logging works
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps.integrations.coingecko.services': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Reuse database connections instead of creating new ones
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# MEMORY OPTIMIZATION: Use dummy cache instead of Redis (we only use Redis for Celery)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# MEMORY OPTIMIZATION: Optimize sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour instead of 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# MEMORY OPTIMIZATION: Limit file upload memory usage
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB

# MEMORY OPTIMIZATION: Minimal middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Disable task result storage (saves memory)
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = None

# Use JSON serialization (more memory efficient than pickle)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

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
