from django.db import models

class TokenMaster(models.Model):
    """
    Master record for a token across all serivces and chains
    """
    # External serivce IDs
    coingecko_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    # Core token data (same across all chains)
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    image = models.URLField(max_length=512, null=True, blank=True)

    #Rankings
    coingecko_rank = models.IntegerField(null=True, blank=True)

    # Sync timestamps
    coingecko_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} ({self.name})"

class Token(models.Model):
    """
    Chain-specific implementation of a token
    """
    master = models.ForeignKey(
            TokenMaster,
            on_delete=models.CASCADE,
            related_name='implementations'
            )

    # Chain-specific
    chain = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=255, null=True, blank=True)
    
    # Sync timestamps
    coingecko_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('chain', 'contract_address')

    def __str__(self):
        return f"{self.master.symbol} ({self.master.name} on {self.chain} chain)"


class SolanaTokenDecimals(models.Model):
    """Model to store Solana based tokens decimals"""
    token = models.OneToOneField(
            Token,
            on_delete=models.CASCADE,
            limit_choices_to={'chain': 'solana'}
            )

    decimals = models.IntegerField()
    jupiter_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.token}: {self.decimals} decimals"
