from django.db import models
from apps.tokens.models import TokenMaster

class CoingeckoPrice(models.Model):
    """
    Model to store coingecko prices of tokens
    """
    token_master = models.OneToOneField(
            TokenMaster,
            on_delete=models.PROTECT,
            related_name='coingecko_price'
            )
    price_usd = models.DecimalField(max_digits=30, decimal_places=12)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CoinGecko price of {self.token_master.symbol} ({self.token_master.name})"

class CoinMarketCapPrice(models.Model):
    """
    Model to store coinmarketcap prices of tokens
    """
    token_master = models.OneToOneField(
            TokenMaster,
            on_delete=models.PROTECT,
            related_name='coimarketcap_price'
            )
    price_usd = models.DecimalField(max_digits=30, decimal_places=12)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CoinMarketCap price of {self.token_master.symbol} ({self.token_master.name})"

