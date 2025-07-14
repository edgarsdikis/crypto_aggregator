from django.db import models
from apps.tokens.models import Token
from apps.wallets.models import Wallet


class WalletTokenBalance(models.Model):
    """
    Model to store all token balances in a wallet
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=36, decimal_places=18)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('wallet', 'token')
        indexes = [
            models.Index(fields=['wallet', 'token']),  # Compound index
            models.Index(fields=['wallet']),           # For wallet filtering
        ]

    def __str__(self):
        return f"{self.wallet.address}: {self.token.contract_address} - ({self.balance})"
