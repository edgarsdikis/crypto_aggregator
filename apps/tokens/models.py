from django.db import models

class Token(models.Model):
    """
    Token metadata
    """
    contract_address = models.CharField(max_length=255)
    chain = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    logo_url = models.URLField(max_length=500, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('contract_address', 'chain')
    
    def __str__(self):
        return f"{self.symbol} on {self.chain}"


class TokenExternalId(models.Model):
    """
    External service IDs for tokens
    """
    token = models.OneToOneField(
        Token, 
        on_delete=models.CASCADE, 
        related_name='external_ids',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    coinmarketcap_id = models.IntegerField(null=True, blank=True, db_index=True)
    mapping_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.symbol} IDs"
