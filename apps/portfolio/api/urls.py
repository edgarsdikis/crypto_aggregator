from django.urls import path
from .views import UserWalletsListView

urlpatterns = [
    path('', UserWalletsListView.as_view(), name='list-wallets'),
]
