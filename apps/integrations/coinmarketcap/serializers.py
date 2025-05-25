from rest_framework import serializers

class CoinMarketCapTokenMapSerializer(serializers.Serializer):
    """
    Serializer for individual token from CoinMarketCap map API
    """
    id = serializers.IntegerField()
    rank = serializers.IntegerField()
    name = serializers.CharField()
    symbol = serializers.CharField()
    slug = serializers.CharField()
    is_active = serializers.IntegerField()
    # TODO: use is_active to remove unactive tokens from db?
