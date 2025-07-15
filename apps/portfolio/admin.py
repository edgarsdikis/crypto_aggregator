from django.contrib import admin
from .models import WalletTokenBalance

@admin.register(WalletTokenBalance)
class WalletTokenBalanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for WalletTokenBalance model
    """
    list_display = ('wallet__address', 'wallet__chain','token__contract_address', 'balance')
    search_fields = ('wallet__address', 'token__contract_address')
    list_filter = ('wallet__address', 'token__contract_address')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('wallet', 'token')
