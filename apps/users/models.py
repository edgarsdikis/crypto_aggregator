from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    """
    Custom user manager that uses email as the unique identifier
    instead of username for authentication.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The email must be set')
        
        email = self.normalize_email(email)
        # Set username equal to email to satisfy AbstractUser requirements
        username = extra_fields.pop('username', email)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        # We accept username parameter to match parent signature, but ignore it
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required by USERNAME_FIELD
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"User {self.pk}: {self.email}"
