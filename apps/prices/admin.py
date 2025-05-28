from django.contrib import admin
from .models import CoingeckoPrice, CoinMarketCapPrice

@admin.register(CoingeckoPrice)
class CoingeckoPriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for CoingeckoPrice model
    """
    list_display = ('token_master__name', 'price_usd', 'updated_at')
    search_fields = ('token_master__name', 'token_master__symbol')

@admin.register(CoinMarketCapPrice)
class CoinMarketCapPriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for CoingeckoPrice model
    """
    list_display = ('token_master__name', 'price_usd', 'updated_at')
    search_fields = ('token_master__name', 'token_master__symbol')
