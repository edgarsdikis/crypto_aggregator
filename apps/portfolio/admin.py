from django.contrib import admin
from .models import WalletTokenBalance

@admin.register(WalletTokenBalance)
class WalletTokenBalanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for WalletTokenBalance model
    """
    list_display = ('wallet__address', 'wallet__chain','name', 'address', 'balance')
    search_fields = ('wallet__address', 'name', 'address')
    list_filter = ('wallet__address', 'name', 'address')
