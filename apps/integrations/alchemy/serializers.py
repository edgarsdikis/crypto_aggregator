from rest_framework import serializers

ALCHEMY_NETWORK_MAPPING = {
        'abstract-mainnet': 'abstract',
        'anime-mainnet': 'anime',
        'apechain-mainnet': 'apechain',
        'arb-mainnet': 'arbitrum-one',
        'arbnova-mainnet': 'arbitrum-nova',
        'avax-mainnet': 'avalanche',
        'bnb-mainnet': 'binance-smart-chain',
        'base-mainnet': 'base',
        'berachain-mainnet': 'berachain',
        'blast-mainnet': 'blast',
        'celo-mainnet': 'celo',
        'eth-mainnet': 'ethereum',
        'gensyn-testnet': 'genesys-network',
        'gnosis-mainnet': 'xdai',
        'ink-mainnet': 'ink',
        'lens-mainnet': 'lens',
        'linea-mainnet': 'linea',
        # monad-testnet, add mainnet when launch
        'opt-mainnet': 'optimistic-ethereum',
        'polygon-mainnet': 'polygon-pos',
        'ronin-mainnet': 'ronin',
        'rootstock-mainnet': 'rootstock',
        'scroll-mainnet': 'scroll',
        # settlus chain 
        # shape chain
        'soneium-mainnet': 'soneium',
        'story-mainnet': 'story',
        # tea chain
        'unichain-mainnet': 'unichain',
        'worldchain-mainnet': 'world-chain',
        'zksync-mainnet': 'zksync',
        'zora-mainnet': 'zora-network',
}

class AlchemyTokenBalanceSerializer(serializers.Serializer):
    """Serilizer for wallet adresses individual token balance from Alchemy API"""

    address = serializers.CharField()
    network = serializers.CharField()
    tokenAddress = serializers.CharField(allow_null=True)
    tokenBalance = serializers.CharField()

    def alchemy_chain_to_coingecko(self, obj):
        """Convert Alchemy chain name to CoinGecko chain name"""
        alchemy_network = obj.get('network')
        return ALCHEMY_NETWORK_MAPPING.get(alchemy_network)

    def get_decimal_balance(self, obj):
        """Convert hex balance to decimal"""
        hex_balance = obj.get('tokenBalance')
        if not hex_balance:
            return 0
        try:
            raw_balance = int(hex_balance, 16)
            return raw_balance / 10 ** 18
        except ValueError:
            return 0

    def is_native_token(self, obj):
        """Check if this is a native token"""
        return obj.get('tokenAddress') is None

