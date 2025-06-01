from rest_framework import serializers
from ..models import Wallet, UserWallet

class AddWalletSerializer(serializers.Serializer):
    """Serializer for adding a new wallet"""
    address = serializers.CharField(max_length=255, allow_blank=False)
    chain = serializers.CharField(max_length=50, allow_blank=False)
    name = serializers.CharField(max_length=50, required=False, allow_blank=True)

