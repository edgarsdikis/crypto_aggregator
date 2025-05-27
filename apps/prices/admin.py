from django.contrib import admin
from .models import Price

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Price model
    """
    list_display = ('token_id__name', 'token_id__symbol', 'price', 'last_updated')
    search_fields = ('token_id__name', 'token_id__symbol')
