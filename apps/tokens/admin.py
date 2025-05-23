from django.contrib import admin
from .models import TokenId, TokenMetadata

@admin.register(TokenMetadata)
class TokenMetadataAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenMetadata model
    """
    list_display = ('address__address', 'name', 'symbol', 'chain')
    search_fields = ('address__address', 'name', 'symbol', 'chain')
    list_filter = ['chain']

@admin.register(TokenId)
class TokenIdAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenId model
    """
    list_display = ('address__address__address', 'coinmarketcap')
    search_fields = ('address__address__address', 'coinmarketcap')
