from rest_framework import serializers

class CoinGeckoCoinsListSerializer(serializers.Serializer):
    """
    Serializer for individual coin from CoinGecko coins/list API
    """

    id = serializers.CharField()
    platforms = serializers.DictField(required=False, default=dict)

    def get_chain_contracts(self, obj):
        """
        Extract contract addresses per chain from platforms data
        Returns: dict like {'ethereum': '0x123...', 'bsc': '0x456...'}
        """
        platforms = obj.get("platforms", {})
        return platforms


class CoinGeckoMarketDataSerializer(serializers.Serializer):
    """
    Serializer for individual coin from CoinGecko coins/markets API
    """

    id = serializers.CharField()
    symbol = serializers.CharField()
    name = serializers.CharField()
    image = serializers.URLField()
    current_price = serializers.DecimalField(max_digits=50, decimal_places=24, allow_null=True)
    market_cap_rank = serializers.IntegerField(allow_null=True)
    last_updated = serializers.DateTimeField()
