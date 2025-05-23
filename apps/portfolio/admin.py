from django.contrib import admin
from .models import WalletTokenBalance

@admin.register(WalletTokenBalance)
class WalletTokenBalanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for WalletTokenBalance model
    """
    list_display = ('wallet__address', 'wallet__chain','token__name', 'token__contract_address', 'balance')
    search_fields = ('wallet__address', 'token__name', 'token__contract_address')
    list_filter = ('wallet__address', 'token__name', 'token__contract_address')
