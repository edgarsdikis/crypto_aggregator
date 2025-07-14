from django.contrib import admin
from .models import Token, TokenMaster, SolanaTokenDecimals

@admin.register(TokenMaster)
class TokenMasterAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenMaster model
    """
    list_display = ('symbol', 'name', 'coingecko_id', 'coingecko_updated_at')
    search_fields = ('name', 'symbol', 'coingecko_id')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for Token model
    """
    list_display = ('master__name', 'chain', 'contract_address', 'coingecko_updated_at')
    search_fields = ('master__name', 'chain', 'contract_address')
    list_filter = ['chain']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('master')

@admin.register(SolanaTokenDecimals)
class SolanaTokenDecimalsAdmin(admin.ModelAdmin):
    """
Admin configuration for SolanaTokenDecimals model
    """
    list_display = ('token__contract_address', 'decimals', 'jupiter_updated')
    search_fields = ['token__contract_address']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('token')

