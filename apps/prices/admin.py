from django.contrib import admin
from .models import Price

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Price model
    """
    list_display = ('token__contract_address', 'token__name', 'token__chain', 'price', 'last_updated')
    search_fields = ('token__contract_address', 'token__name')
    list_filter = ['token__chain']
