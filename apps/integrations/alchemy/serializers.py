from rest_framework import serializers

ALCHEMY_NETWORK_MAPPING = {
    'abstract-mainnet': {
        'coingecko_name': 'abstract',
        'native_decimals': 18
    },
    'anime-mainnet': {
        'coingecko_name': 'anime', 
        'native_decimals': 18
    },
    'apechain-mainnet': {
        'coingecko_name': 'apechain',
        'native_decimals': 18
    },
    'arb-mainnet': {
        'coingecko_name': 'arbitrum-one',
        'native_decimals': 18
    },
    'arbnova-mainnet': {
        'coingecko_name': 'arbitrum-nova',
        'native_decimals': 18
    },
    'avax-mainnet': {
        'coingecko_name': 'avalanche',
        'native_decimals': 18
    },
    'bnb-mainnet': {
        'coingecko_name': 'binance-smart-chain',
        'native_decimals': 18
    },
    'base-mainnet': {
        'coingecko_name': 'base',
        'native_decimals': 18
    },
    'berachain-mainnet': {
        'coingecko_name': 'berachain',
        'native_decimals': 18
    },
    'blast-mainnet': {
        'coingecko_name': 'blast',
        'native_decimals': 18
    },
    'celo-mainnet': {
        'coingecko_name': 'celo',
        'native_decimals': 18
    },
    'eth-mainnet': {
        'coingecko_name': 'ethereum',
        'native_decimals': 18
    },
    'gensyn-testnet': {
        'coingecko_name': 'genesys-network',
        'native_decimals': 18  # Verify this
    },
    'gnosis-mainnet': {
        'coingecko_name': 'xdai',
        'native_decimals': 18
    },
    'ink-mainnet': {
        'coingecko_name': 'ink',
        'native_decimals': 18  # Verify this
    },
    'lens-mainnet': {
        'coingecko_name': 'lens',
        'native_decimals': 18  # Verify this
    },
    'linea-mainnet': {
        'coingecko_name': 'linea',
        'native_decimals': 18
    },
    'opt-mainnet': {
        'coingecko_name': 'optimistic-ethereum',
        'native_decimals': 18
    },
    'polygon-mainnet': {
        'coingecko_name': 'polygon-pos',
        'native_decimals': 18
    },
    'ronin-mainnet': {
        'coingecko_name': 'ronin',
        'native_decimals': 18
    },
    'rootstock-mainnet': {
        'coingecko_name': 'rootstock',
        'native_decimals': 18
    },
    'scroll-mainnet': {
        'coingecko_name': 'scroll',
        'native_decimals': 18
    },
    'solana-mainnet': {
        'coingecko_name': 'solana',
        'native_decimals': 9
    },
    'soneium-mainnet': {
        'coingecko_name': 'soneium',
        'native_decimals': 18  # Verify this
    },
    'story-mainnet': {
        'coingecko_name': 'story',
        'native_decimals': 18  # Verify this
    },
    'unichain-mainnet': {
        'coingecko_name': 'unichain',
        'native_decimals': 18  # Verify this
    },
    'worldchain-mainnet': {
        'coingecko_name': 'world-chain',
        'native_decimals': 18
    },
    'zksync-mainnet': {
        'coingecko_name': 'zksync',
        'native_decimals': 18
    },
    'zora-mainnet': {
        'coingecko_name': 'zora-network',
        'native_decimals': 18
    },
}

class AlchemyTokenBalanceSerializer(serializers.Serializer):
    """Basic validation of Alchemy API response structure"""
    address = serializers.CharField()
    network = serializers.CharField()
    tokenAddress = serializers.CharField(allow_null=True)
    tokenBalance = serializers.CharField()
    tokenMetadata = serializers.DictField()
    tokenPrices = serializers.ListField(child=serializers.DictField())

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
