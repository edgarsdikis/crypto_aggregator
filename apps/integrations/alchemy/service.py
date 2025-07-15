from apps.tokens.models import SolanaTokenDecimals
from .serializers import AlchemyTokenBalanceSerializer
from config.chain_mapping import ALCHEMY_NETWORK_MAPPING


class AlchemyWalletService:
    def process_wallet_balances(self, wallet_response):
        """Process and filter wallet balance data"""
        tokens = wallet_response.get('tokens')
        valid_tokens = []

        for token_data in tokens:

            # Validate basic structure
            serializer = AlchemyTokenBalanceSerializer(data=token_data)
            if not serializer.is_valid():
                continue

            # Filter out the potential scam coins
            if not self._should_include_token(token_data, serializer):
                continue

            # Conver and enrich data
            processed_token = self._convert_token_data(token_data)
            if processed_token:
                valid_tokens.append(processed_token)

        return valid_tokens

    def _should_include_token(self, token_data, serializer):
        """Logic for filtering tokens"""

        if serializer.is_zero_balance(token_data):
            return False

        if token_data['network'] == 'solana-mainnet' and token_data['tokenAddress']:
            return SolanaTokenDecimals.objects.filter(token__contract_address=token_data['tokenAddress']).exists()

        return True

    def _convert_token_data(self, token_data):
        """Convert hex to decimal, map chains, etc..."""
    
        try:
            # Get network info
            network_info = ALCHEMY_NETWORK_MAPPING.get(token_data['network'])
            if not network_info:
                return None
            
            # Calculate balance
            decimal_balance = self._hex_to_decimal_balance(
                    token_data['tokenBalance'],
                    token_data['tokenMetadata'],
                    token_data['network'],
                    token_data['tokenAddress']
                    )

            return {
                'wallet_address': token_data['address'],
                'coingecko_chain': network_info['coingecko_name'],
                'contract_address': token_data['tokenAddress'],
                'decimal_balance': decimal_balance,
                'name': token_data['tokenMetadata'].get('name'),
            }
        
        except Exception as e:
            print(f"Error converting token data: {e}")
            return None

    def _hex_to_decimal_balance(self, hex_balance, metadata, network, token_address):
        """Convert hex balance to human readable decimal"""
        raw_balance = int(hex_balance, 16)
        
        # Native token
        if token_address is None:
            network_info = ALCHEMY_NETWORK_MAPPING.get(network)
            decimals = network_info['native_decimals'] # type: ignore
        elif network == "solana-mainnet" and token_address:
            solana_decimal = SolanaTokenDecimals.objects.select_related('token').get(token__contract_address=token_address)
            decimals = solana_decimal.decimals
        else:
            decimals = metadata.get('decimals')

        return raw_balance / (10 ** decimals)

