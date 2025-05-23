from django.db import models
from apps.portfolio.models import WalletTokenBalance

class Prices(models.Model):
    """
    Model to store token prices
    """
    address = models.ForeignKey(WalletTokenBalance, on_delete=models.CASCADE)
    chain = models.CharField(max_length=50)
    cmc_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('address', 'chain')

    def __str__(self):
        return f"{self.address.address} ({self.chain})"
