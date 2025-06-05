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


NETWORK_MAPPING = {
    'abstract': 'abstract-mainnet',
    'anime': 'anime-mainnet',
    'apechain': 'apechain-mainnet',
    'arbitrum-one': 'arb-mainnet',
    'arbitrum-nova': 'arbnova-mainnet',
    'avalanche': 'avax-mainnet',
    'bsc': 'bnb-mainnet',
    'base': 'base-mainnet',
    'berachain': 'berachain-mainnet',
    'blast': 'blast-mainnet',
    'celo': 'celo-mainnet',
    'eth': 'eth-mainnet',
    'genesys': 'gensyn-testnet',
    'xdai': 'gnosis-mainnet',
    'ink': 'ink-mainnet',
    'lens': 'lens-mainnet',
    'linea': 'linea-mainnet',
    'optimism': 'opt-mainnet',
    'polygon': 'polygon-mainnet',
    'ronin': 'ronin-mainnet',
    'rootstock': 'rootstock-mainnet',
 'scroll': 'scroll-mainnet',
    'solana': 'solana-mainnet',
    'soneium': 'soneium-mainnet',
    'story': 'story-mainnet',
    'unichain': 'unichain-mainnet',
    'worldchain': 'worldchain-mainnet',
    'zksync': 'zksync-mainnet',
    'zora': 'zora-mainnet',
}



# Chain for coingecko native tokens
COINGECKO_NATIVE_TOKEN_MAPPING = {
    'ethereum': ['abstract','ethereum', 'arbitrum-one', 'arbitrum-nova', 'base', 'blast', 'linea', 'optimistic-ethereum', 'scroll', 'unichain', 'world-chain', 'zksync', 'zora-network'],
    'binancecoin': ['binance-smart-chain'],
    'matic-network': ['polygon-pos'],
    'avalanche-2': ['avalanche'],
    'solana': ['solana'],
    'celo': ['celo'],
    'xdai': ['xdai'],
    # ... find more
    # 'abstract': 'abstract-mainnet',
    # 'anime': 'anime-mainnet',
    # 'apechain': 'apechain-mainnet',
    # 'berachain': 'berachain-mainnet',
    # 'genesys': 'gensyn-testnet',
    # 'ink': 'ink-mainnet',
    # 'lens': 'lens-mainnet',
    # 'ronin': 'ronin-mainnet',
    # 'rootstock': 'rootstock-mainnet',
    # 'soneium': 'soneium-mainnet',
    # 'story': 'story-mainnet',
}


COINGECKO_TO_ALCHEMY_MAPPING = {
    'abstract': 'abstract-mainnet',
    'anime': 'anime-mainnet',
    'apechain': 'apechain-mainnet',
    'arbitrum-one': 'arb-mainnet',
    'arbitrum-nova': 'arbnova-mainnet',
    'avalanche': 'avax-mainnet',
    'binance-smart-chain': 'bnb-mainnet',
    'base': 'base-mainnet',
    'berachain': 'berachain-mainnet',
    'blast': 'blast-mainnet',
    'celo': 'celo-mainnet',
    'ethereum': 'eth-mainnet',
    'genesys-network': 'gensyn-testnet',
    'xdai': 'gnosis-mainnet',
    'ink': 'ink-mainnet',
    'lens': 'lens-mainnet',
    'linea': 'linea-mainnet',
    'optimistic-ethereum': 'opt-mainnet',
    'polygon-pos': 'polygon-mainnet',
    'ronin': 'ronin-mainnet',
    'rootstock': 'ronin-mainnet',
    'scroll': 'scroll-mainnet',
    'solana': 'solana-mainnet',
    'soneium': 'soneium-mainnet',
    'story': 'story-mainnet',
    'unichain': 'unichain-mainnet',
    'world-chain': 'worldchain-mainnet',
    'zksync': 'zksync-mainnet',
    'zora-network': 'zksync-mainnet'
}


FRONTEND_TO_COINGECKO_MAPPING = {
    'abstract': 'abstract',
    'anime': 'anime',
    'apechain': 'apechain',
    'arbitrum-one': 'arbitrum-one',
    'arbitrum-nova': 'arbitrum-nova',
    'avalanche': 'avalanche',
    'bsc': 'binance-smart-chain',
    'base': 'base',
    'berachain': 'berachain',
    'blast': 'blast',
    'celo': 'celo',
    'eth': 'ethereum',
    'genesys': 'genesys-network',
    'xdai': 'xdai',
    'ink': 'ink',
    'lens': 'lens',
    'linea': 'linea',
    'optimism': 'optimistic-ethereum',
    'polygon': 'polygon-pos',
    'ronin': 'ronin',
    'rootstock': 'rootstock',
 'scroll': 'scroll',
    'solana': 'solana',
    'soneium': 'soneium',
    'story': 'story',
    'unichain': 'unichain',
    'worldchain': 'world-chain',
    'zksync': 'zksync',
    'zora': 'zora-network',
}
