from rest_framework import serializers

class JupiterTaggedCoinsSerializer(serializers.Serializer):
    """
    Serializer for Jupiter Token API V2 response
    """
    id = serializers.CharField()  # Token API V2 uses 'id' for mint address
    decimals = serializers.IntegerField()
    name = serializers.CharField(required=False)
    symbol = serializers.CharField(required=False)
    isVerified = serializers.BooleanField(required=False, default=False)
