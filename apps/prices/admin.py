from django.contrib import admin
from .models import Prices

@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):
    """
    Admin configuration for Prices model
    """
    list_display = ('address__address', 'address__name', 'chain', 'cmc_price')
    search_fields = ('address__address', 'address__name')
    list_filter = ['chain']
