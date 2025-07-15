from django.urls import path
from .views import UserWalletsListView, WalletAssetsView, UserPortfolioView

urlpatterns = [
    path('', UserWalletsListView.as_view(), name='list-wallets'),
    path('wallet/', WalletAssetsView.as_view(), name='wallet-assets'),
    path('allwallets/', UserPortfolioView.as_view(), name='user-portfolio'),
]
