from rest_framework import serializers

class CoinGeckoCoinsListSerializer(serializers.Serializer):
    """
    Serializer for individual coin from CoinGecko coins/list API
    """

    id = serializers.CharField()
    platforms = serializers.DictField(required=False, default=dict)

class CoinGeckoMarketDataSerializer(serializers.Serializer):
    """
    Serializer for individual coin from CoinGecko coins/markets API
    """

    id = serializers.CharField()
    symbol = serializers.CharField(allow_blank=False)
    name = serializers.CharField()
    image = serializers.URLField(allow_null=True, required=False)
    current_price = serializers.DecimalField(max_digits=70, decimal_places=50, required=True)
    market_cap_rank = serializers.IntegerField(allow_null=True)
    price_change_percentage_24h = serializers.DecimalField(max_digits=10, decimal_places=5, required=False)
