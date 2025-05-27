from rest_framework import serializers

# CMC_TO_MORALIS_MAPPING = {
#     'Ethereum': 'eth',
#     'BNB': 'bsc',
#     'Polygon': 'polygon', 
#     'Avalanche C-Chain': 'avalanche',
#     'Fantom': 'fantom',
#     'Arbitrum One': 'arbitrum',
#     'Optimism': 'optimism',
#     'Ethereum Testnet Sepolia': 'sepolia',
#     'Ethereum Testnet Holesky': 'holesky',
#     'Cronos': 'cronos',
#     'Gnosis Chain': 'gnosis', 
#     'Chiliz Chain': 'chiliz',
#     'Base': 'base',
#     'Linea': 'linea',
#     'Moonbeam': 'moonbeam',
#     'Moonriver': 'moonriver',
#     'Flow': 'flow',
#     'Ronin': 'ronin',
#     'Lisk': 'lisk',
#     'PulseChain': 'pulse',
#     'Solana': 'solana',
# }

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

class CoinMarketCapTokenInfoSerializer(serializers.Serializer):
    """
    Serializer for individual token from CoinMarketCap info API
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    symbol = serializers.CharField()
    logo = serializers.URLField()

    chain = serializers.SerializerMethodField()
    contract_address = serializers.SerializerMethodField()

    def get_chain(self,obj):
        platform = obj.get('platform')
        if not platform:
            return 'native'

        platform_name = platform.get('name', '')
        # return CMC_TO_MORALIS_MAPPING.get(platform_name, 'unknown')
        return platform_name

    def get_contract_address(self, obj):
        platform = obj.get('platform')
        return platform.get('token_address') if platform else None
        
class CoinMarketCapTokenPriceSerializer(serializers.Serializer):
    """
    Serializer for individual token from CoinMarketCap price API
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """Extract USD price with safe None checks like get_contract_address"""
        quote = obj.get('quote')
        if not quote:
            return None
            
        usd = quote.get('USD')
        if not usd:
            return None
            
        return usd.get('price')

