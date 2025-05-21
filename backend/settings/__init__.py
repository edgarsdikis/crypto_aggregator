import os

# Default to local settings if not specified
environment = os.environ.get('DJANGO_ENVIRONMENT', 'local')

if environment == 'production':
    from .production import *
elif environment == 'develop':
    from .develop import *
else:
    from .local import *
