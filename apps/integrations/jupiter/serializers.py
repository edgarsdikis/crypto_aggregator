from rest_framework import serializers

class JupiterTaggedCoinsSerializer(serializers.Serializer):
    """
    Serializer for individual coin from Jupiter tagged coins API
    """

    address = serializers.CharField()
    decimals = serializers.IntegerField()

