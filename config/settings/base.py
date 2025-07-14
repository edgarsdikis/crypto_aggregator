import os
from pathlib import Path
import environ
from datetime import timedelta
from celery.schedules import crontab

# Initialize environ
env = environ.Env(
    # Set casting and default values
    DEBUG=(bool, False),
    DATABASE_URL=(str, 'postgres://postgres:postgres@db:5432/crypto_portfolio'),
    REDIS_URL=(str, 'redis://redis:6379/0'),
)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file if it exists
env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    # Local apps
    "apps.users",
    "apps.wallets",
    "apps.tokens", 
    "apps.prices",
    "apps.portfolio",
    "apps.integrations",
]

# User Model
AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    'default': env.db()
}

REDIS_URL = env('REDIS_URL')

# Caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}



# Celery settings
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = None
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = REDIS_URL
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1

# Celery Beat settings (for scheduled tasks)
CELERY_BEAT_SCHEDULE = {

    'sync-market-data-and-cleanup': {
        'task': 'apps.integrations.coingecko.tasks.sync_market_data_and_cleanup_task',
        'schedule': crontab(minute=21, hour='18'), # type: ignore
    },
    'sync-multichain-tokens': {
        'task': 'apps.integrations.coingecko.tasks.sync_multichain_tokens_task',
        'schedule': crontab(minute=31, hour='18'),  # type: ignore
    },
    'sync-solana-decimals': {
        'task': 'apps.integrations.jupiter.tasks.sync_jupiter_solana_decimals_task',
        'schedule': crontab(minute=38, hour='18'), # type: ignore
        },
}
CELERY_TIMEZONE = 'Europe/Riga'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# API documentation settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Crypto Portfolio API',
    'DESCRIPTION': 'API for tracking cryptocurrency portfolios across multiple chains and exchanges',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'Authentication', 'description': 'User authentication and JWT token refresh endpoints'},
        {'name': 'User', 'description': 'User profile endpoints'},
        {'name': 'Wallets', 'description': 'Wallet management endpoints'},
        {'name': 'Portfolio', 'description': 'Portfolio management endpoints'},
    ],
    # Use our custom generator
    'DEFAULT_GENERATOR_CLASS': 'spectacular.schema.CustomSchemaGenerator',
}

# Internationalization
LANGUAGE_CODE = "en-gb"  # British English uses 24-hour format by default
TIME_ZONE = "Europe/Riga"  # Riga time zone
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# API Keys
COINGECKO_API_KEY= env('COINGECKO_API_KEY')
ALCHEMY_API_KEY= env('ALCHEMY_API_KEY')
