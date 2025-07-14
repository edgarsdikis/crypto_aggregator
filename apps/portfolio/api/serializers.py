from rest_framework import serializers

class WalletListSerializer(serializers.Serializer):
    """Serializer for wallet list with USD balance"""
    address = serializers.CharField()
    chain = serializers.CharField()
    balance_usd = serializers.CharField()
    name = serializers.CharField()

class WalletAssetsRequestSerializer(serializers.Serializer):
    """Serializer for wallet assets request"""
    address = serializers.CharField(max_length=255, help_text="Wallet address")
    chain = serializers.CharField(max_length=50, help_text="Blockchain network")


class TokenDataSerializer(serializers.Serializer):
    """Serializer for individual Token data"""
    address = serializers.CharField()
    chain = serializers.CharField()
    symbol = serializers.CharField()
    name = serializers.CharField()
    logo = serializers.URLField(allow_blank=True, allow_null=True)
    price_usd = serializers.CharField()
    percentage_24h = serializers.CharField()

class TokenBalanceSerializer(serializers.Serializer):
    """Serializer for individual Token balance"""
    token_balance_formatted = serializers.CharField()
    usd_value = serializers.CharField()

class WalletTokenSerializer(serializers.Serializer):
    """Serializer for individual Token data and balance"""
    token_details = TokenDataSerializer()
    token_balance = TokenBalanceSerializer()

class WalletAssetsSerializer(serializers.Serializer):
    """Serializer for wallet assets list"""
    wallet_name = serializers.CharField(allow_blank=True, allow_null=True)
    wallet_address = serializers.CharField()
    wallet_chain = serializers.CharField()
    tokens = WalletTokenSerializer(many=True)

class UserPortfolioSerializer(serializers.Serializer):
    """Serializer for aggregated user portfolio"""
    tokens = WalletTokenSerializer(many=True)
