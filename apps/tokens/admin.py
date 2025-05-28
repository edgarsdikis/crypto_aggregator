from django.contrib import admin
from .models import Token, TokenMaster

@admin.register(TokenMaster)
class TokenMasterAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenMaster model
    """
    list_display = ('symbol', 'name', 'coingecko_id', 'coinmarketcap_id', 'coingecko_updated_at', 'coinmarketcap_updated_at')
    search_fields = ('name', 'symbol', 'coingecko_id', 'coinmarketcap_id')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for Token model
    """
    list_display = ('master__name', 'chain', 'contract_address', 'coingecko_updated_at', 'coinmarketcap_updated_at')
    search_fields = ('master__name', 'chain', 'contract_address')
    list_filter = ['chain']


