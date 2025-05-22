from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'date_joined')
    search_fields = ('email', 'id')
    ordering = ('id', 'email', 'is_staff', 'date_joined')
