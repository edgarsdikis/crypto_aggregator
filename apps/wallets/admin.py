from django.contrib import admin
from .models import Wallet, UserWallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Admin configuration for Wallet model"""
    list_display = ('address', 'chain')
    search_fields = ('address', 'chain')
    list_filter = ('address', 'chain')


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    """Admin configuration for WalletUser model"""
    list_display = ('user', 'wallet__address', 'wallet__chain', 'name')
    search_fields = ('user__username', 'wallet__address')
    list_filter = ('wallet__address', 'wallet__chain')    

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'wallet')
