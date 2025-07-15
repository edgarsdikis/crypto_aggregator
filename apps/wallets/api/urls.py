from django.urls import path
from .views import AddWalletView, RemoveWalletView, SupportedChainsView, UpdateWalletNameView, SyncWalletsView

urlpatterns = [
        path('add/', AddWalletView.as_view(), name='add-wallet'),
        path('remove/', RemoveWalletView.as_view(), name='remove-wallet'),
        path('supported-chains/', SupportedChainsView.as_view(), name='supported-chains'),
        path('update-name/', UpdateWalletNameView.as_view(), name='update-wallet-name'),
        path('sync/', SyncWalletsView.as_view(), name='sync-wallets'),
        ]
