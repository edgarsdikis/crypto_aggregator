from django.db import models
from apps.wallets.models import Wallet


class WalletTokenBalance(models.Model):
    """
    Model to store all token balances in a wallet
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('wallet', 'address')

    def __str__(self):
        return f"{self.wallet} - {self.name} - {self.balance}"
