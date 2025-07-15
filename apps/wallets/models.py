from django.db import models
from django.conf import settings

class Wallet(models.Model):
    """
    Model to store wallet address and chain 
    """
    address = models.CharField(max_length=255)
    chain = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('address', 'chain')
    
    def __str__(self):
        return f"{self.address} ({self.chain})"


class UserWallet(models.Model):
    """
    Association between user and wallet address
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'wallet')

    def __str__(self):
        return f"{self.user.username} - {self.wallet}"
