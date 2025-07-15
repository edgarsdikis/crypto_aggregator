from django.db import models
from apps.tokens.models import TokenMaster

class CoingeckoPrice(models.Model):
    """
    Model to store coingecko prices of tokens
    """
    token_master = models.OneToOneField(
            TokenMaster,
            on_delete=models.CASCADE,
            related_name='coingecko_price'
            )
    price_usd = models.DecimalField(max_digits=70, decimal_places=50)
    updated_at = models.DateTimeField(auto_now=True)
    percentage_24h = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return f"CoinGecko price of {self.token_master.symbol} ({self.token_master.name})"

