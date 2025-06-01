from django.urls import path
from .views import AddWalletView

urlpatterns = [
        path('add/', AddWalletView.as_view(), name='add-wallet'),
        ]
