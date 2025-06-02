from django.urls import path
from .views import UserWalletsListView, WalletAssetsView

urlpatterns = [
    path('', UserWalletsListView.as_view(), name='list-wallets'),
    path('wallet/', WalletAssetsView.as_view(), name='wallet-assets'),
]
