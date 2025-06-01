from django.urls import path
from .views import AddWalletView, RemoveWalletView

urlpatterns = [
        path('add/', AddWalletView.as_view(), name='add-wallet'),
        path('remove/', RemoveWalletView.as_view(), name='remove-wallet'),
        ]
