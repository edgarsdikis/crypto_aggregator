from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser if none exists (only in deployed environments)'

    def handle(self, *_args, **_kwargs):
        # Only run in develop/production, not local
        environment = os.environ.get('DJANGO_ENVIRONMENT', 'local')
        
        if environment == 'local':
            self.stdout.write('Local environment detected - skipping automated superuser creation')
            return
            
        if not User.objects.filter(is_superuser=True).exists():
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            
            if not all([email, password]):
                self.stdout.write('Superuser environment variables not set, skipping...')
                return
            
            User.objects.create_superuser( # type: ignore
                email=email,
                password=password
            )
            self.stdout.write(f'Superuser {email} created successfully')
        else:
            self.stdout.write('Superuser already exists')
