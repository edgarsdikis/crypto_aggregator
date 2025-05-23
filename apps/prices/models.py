from django.db import models
from django.db.models.deletion import CASCADE
from apps.tokens.models import Token

class Price(models.Model):
    """
    Model to store token prices
    """
    token = models.OneToOneField(Token, on_delete=CASCADE, related_name='current_price')
    price = models.DecimalField(max_digits=20, decimal_places=8)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.token.name} ({self.price})"
