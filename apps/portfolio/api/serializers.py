from rest_framework import serializers

class WalletListSerializer(serializers.Serializer):
    """Serializer for wallet list with USD balance"""
    address = serializers.CharField()
    chain = serializers.CharField()
    balance_usd = serializers.CharField()
