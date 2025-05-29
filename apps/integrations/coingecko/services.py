from django.db import transaction
from django.utils import timezone
from apps.tokens.models import Token, TokenMaster
from apps.prices.models import CoingeckoPrice
from .client import CoinGeckoClient
from .serializers import CoinGeckoCoinsListSerializer, CoinGeckoMarketDataSerializer

class CoinGeckoSyncService:
    """Service for syncing CoinGecko token data and prices"""

    def __init__(self):
        self.client = CoinGeckoClient()
    
    def sync_all(self):
        """
        Complete sync: market data first, then implementations
        """
        print("Starting complete CoinGecko sync...")
        
        # Step 1: Sync master tokens and prices
        market_result = self.sync_market_data()
        
        # Step 2: Sync chain implementations
        impl_result = self.sync_token_implementations()
        
        return f"Complete sync: {market_result}, {impl_result}"

    def sync_market_data(self):
        """
        Sync TokenMaster records and prices from CoinGecko markets endpoint

        This gets all of the tokens on CoinGecko
        """

        print("Starting CoinGecko market data sync...")
        sync_start_time = timezone.now()

        try:
            market_data, failed_pages = self.client.get_coins_markets()

            if failed_pages:
                print(f"  Warning: {len(failed_pages)} pages failed during fetch")
                # TODO: something with failed paiges!

            print(f"Processing {len(market_data)} tokens from market data...")
            success_count, error_count = self._process_market_data(market_data)

            self._remove_stale_tokens(sync_start_time)

            print(f"Market sync completed: {success_count} successful, {error_count} errors")
            return f"Synced {success_count} tokens, {error_count} errors"

        except Exception as e:
            print(f"Market sync failed: {e}")
            raise

    def sync_token_implementations(self):
        """
        Sync Token records (chain implementations) from CoinGecko list endpoint
        
        This creates multiple Token records per TokenMaster (one per chain)
        """
        print("Starting CoinGecko token implementations sync...")
        try:
            coins_list = self.client.get_coins_list(include_platform=True)
            print(f"Processing {len(coins_list)} tokens for chain implementations...")

            success_count, error_count = self._process_token_implementations(coins_list)

            print(f"Implementations sync completed: {success_count} successful, {error_count} errors")
            return f"Created {success_count} token implementations, {error_count} errors"
        
        except Exception as e:
            print(f"Implementations sync failed: {e}")
            raise

    @transaction.atomic
    def _process_market_data(self, market_data):
        """
        Process market data and create/update TokenMaster and CoingeckoPrice records
        """
        success_count = 0
        error_count = 0
        
        for coin_data in market_data:
            try:
                # Validate the API response structure
                serializer = CoinGeckoMarketDataSerializer(data=coin_data)
                
                if not serializer.is_valid():
                    print(f"Validation error for {coin_data.get('id', 'unknown')}: {serializer.errors}")
                    error_count += 1
                    continue
                
                validated_data = serializer.validated_data
                
                # Create or update TokenMaster
                token_master, created = TokenMaster.objects.update_or_create(
                        coingecko_id=validated_data['id'], #type: ignore
                    defaults={
                        'symbol': validated_data['symbol'], #type: ignore
                        'name': validated_data['name'], #type: ignore
                        'image': validated_data['image'], #type: ignore
                        'coingecko_rank': validated_data['market_cap_rank'], #type: ignore
                        'coingecko_updated_at': timezone.now(),
                    }
                )
                
                # Create or update price records
                if validated_data['current_price'] is not None: #type: ignore
                    CoingeckoPrice.objects.update_or_create(
                        token_master=token_master,
                        defaults={
                            'price_usd': validated_data['current_price'], #type: ignore
                        }
                    )
                
                if created:
                    print(f"Created new TokenMaster: {token_master.symbol}")
                
                success_count += 1
                
            except Exception as e:
                print(f"Error processing {coin_data.get('id', 'unknown')}: {e}")
                error_count += 1
        
        return success_count, error_count
    
    @transaction.atomic  
    def _process_token_implementations(self, coins_list):
        """
        Process coins list and create Token records for each chain implementation
        Creates native Token records for tokens without platform contracts
        """
        success_count = 0
        error_count = 0
        
        for coin_data in coins_list:
            try:
                # Validate the API response structure
                serializer = CoinGeckoCoinsListSerializer(data=coin_data)
                
                if not serializer.is_valid():
                    print(f"Validation error for {coin_data['id']}: {serializer.errors}")
                    error_count += 1
                    continue
                
                validated_data = serializer.validated_data
                coingecko_id = validated_data['id'] # type: ignore
                
                # Find the corresponding TokenMaster
                try:
                    token_master = TokenMaster.objects.get(coingecko_id=coingecko_id)
                except TokenMaster.DoesNotExist:
                    print(f"No TokenMaster found for {coingecko_id}, skipping implementations")
                    error_count += 1
                    continue
                
                # Extract platform/contract data
                platforms = serializer.get_chain_contracts(validated_data)
                
                if platforms:
                    # Create Token record for each chain implementation  
                    for chain, contract_address in platforms.items():
                        if contract_address:
                            Token.objects.update_or_create(
                                master=token_master,
                                chain=chain,
                                defaults={
                                    'contract_address': contract_address,
                                    'coingecko_updated_at': timezone.now(),
                                }
                            )
                else:
                    
                    Token.objects.update_or_create(
                        master=token_master,
                        chain="native",
                        defaults={
                            'contract_address': None,  # Native tokens have no contract
                            'coingecko_updated_at': timezone.now(),
                        }
                    )

                success_count += 1
                
            except Exception as e:
                print(f"❌ Error processing implementations for {coin_data['id']}: {e}")
                error_count += 1
        
        return success_count, error_count

    def _remove_stale_tokens(self, sync_start_time):
        stale_tokens = TokenMaster.objects.filter(
            coingecko_id__isnull=False,
            coingecko_updated_at__lt=sync_start_time
        )
        
        stale_count = stale_tokens.count()
        if stale_count > 0:
            print(f"🧹 Removing {stale_count} stale tokens...")
            stale_tokens.delete()

