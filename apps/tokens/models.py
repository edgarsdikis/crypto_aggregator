from django.db import models
from apps.portfolio.models import WalletTokenBalance

class TokenMetadata(models.Model):
    """
    Model to store token metadata
    """
    address = models.ForeignKey(WalletTokenBalance, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    chain = models.CharField(max_length=50)
    logo = models.URLField(max_length=500, null=True, blank=True)
    symbol = models.CharField(max_length=50)

    class Meta:
        unique_together = ('address', 'chain')

    def __str__(self):
        return f"{self.address.adress} ({self.chain})"


class TokenId(models.Model):
    """
    Model to store token id mapping
    """
    address = models.ForeignKey(TokenMetadata, on_delete=models.CASCADE)
    coinmarketcap = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)

    class Meta:
        unique_together = ('address', 'coinmarketcap')

    def __str__(self):
        return f"{self.address.address} -> {self.coinmarketcap}"
