from django.contrib import admin
from .models import Token, TokenExternalId

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for Token model
    """
    list_display = ('contract_address', 'name', 'symbol', 'chain')
    search_fields = ('contract_address', 'name', 'symbol', 'chain')
    list_filter = ['chain']

@admin.register(TokenExternalId)
class TokenExternalIdAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenExternalId model
    """
    list_display = ('token__name', 'token__contract_address', 'token__chain', 'coinmarketcap_id')
    search_fields = ('token__name', 'token__contract_address', 'token__chain', 'coinmarketcap_id')
