from rest_framework import serializers


class AlchemyTokenBalanceSerializer(serializers.Serializer):
    """Basic validation of Alchemy API response structure"""
    address = serializers.CharField()
    network = serializers.CharField()
    tokenAddress = serializers.CharField(allow_null=True)
    tokenBalance = serializers.CharField()
    tokenMetadata = serializers.DictField()
    tokenPrices = serializers.ListField()

    def has_price_data(self, obj):
        """Check if token has price data"""
        return bool(obj.get('tokenPrices'))

    def is_zero_balance(self, obj):
        """Check if balance is zero"""
        hex_balance = obj.get('tokenBalance', '')
        if not hex_balance:
            return True
        
        hex_part = hex_balance[2:] if hex_balance.startswith('0x') else hex_balance
        return hex_part == '0' * len(hex_part)
