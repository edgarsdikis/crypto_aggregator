from django.db import transaction
from django.utils import timezone
from apps.tokens.models import Token, TokenMaster
from apps.prices.models import CoingeckoPrice
from .client import CoinGeckoClient
from .serializers import CoinGeckoCoinsListSerializer, CoinGeckoMarketDataSerializer
from config.chain_mapping import COINGECKO_NATIVE_TOKEN_MAPPING
from django.utils import timezone
import time
import gc

class CoinGeckoSyncService:
    def __init__(self):
        self.client = CoinGeckoClient()

    def sync_all(self):
        """Complete sync"""
        sync_start_time = timezone.now()
        market_result = self.sync_market_data()
        deleted_count, _ = self._remove_stale_tokens(sync_start_time)        
        return f"Market sync: {market_result}.  Removed {deleted_count} stale tokens"

    def sync_market_data(self):
        """Market data sync"""
        
        try:
            success_count, error_count = self._process_market_data_chunked()
            return f"Synced {success_count} tokens, {error_count} errors"

        except Exception as e:
            print(f"sync_market_data failed: {e}")
            raise

    def _process_market_data_chunked(self):
        """Chunked market data processing"""
        total_success = 0
        total_errors = 0
        page = 1
        
        while True:
            page_data = self.client.get_coins_markets_single_page(page=page)
            
            if not page_data:
                break
            
            # Process page
            success_count, error_count = self._process_market_data_page(page_data)
            total_success += success_count
            total_errors += error_count
            
            # Check if last page
            is_last_page = len(page_data) < 250
            
            # Delete page data
            del page_data
            
            # Garbage collect every 5 pages
            if page % 5 == 0:
                gc.collect()
            
            if is_last_page:
                break
                
            page += 1
            time.sleep(2.5)
        
        return total_success, total_errors

    def _process_market_data_page(self, page_data):
        """Process page"""
        success_count = 0
        error_count = 0
        
        for coin_data in page_data:
            try:
                serializer = CoinGeckoMarketDataSerializer(data=coin_data)
                
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    
                    # Capture the token_master from update_or_create
                    token_master, created = TokenMaster.objects.update_or_create(
                        coingecko_id=validated_data['id'], # type: ignore
                        defaults={
                            'symbol': validated_data['symbol'], # type: ignore
                            'name': validated_data['name'], # type: ignore
                            'image': validated_data['image'], # type: ignore
                            'coingecko_rank': validated_data['market_cap_rank'], # type: ignore
                            'coingecko_updated_at': timezone.now(),
                        }
                    )
                    
                    CoingeckoPrice.objects.update_or_create(
                        token_master=token_master,
                        defaults={
                            'price_usd': validated_data['current_price'], # type: ignore
                        }
                    )
                    
                    success_count += 1
                    
                else:
                    error_count += 1
                    
            except Exception as e:
                print(f"Failed to serialize coin data: {e}")
                error_count += 1
            
        return success_count, error_count

    def sync_multi_chain_tokens(self):
        """
        Sync cross-chain Token records from CoinGecko list endpoint
        
        Creates Token records showing how each TokenMaster exists across multiple chains
        """
        print("Starting CoinGecko token multi-chain sync...")
        try:
            coins_list = self.client.get_coins_list(include_platform=True)
            print(f"Processing {len(coins_list)} tokens")

            success_count, error_count = self._process_multi_chain_tokens(coins_list)

            print(f"Implementations sync completed: {success_count} successful, {error_count} errors")
            return f"Created {success_count} token implementations, {error_count} errors"
        
        except Exception as e:
            print(f"Implementations sync failed: {e}")
            raise

    @transaction.atomic  
    def _process_multi_chain_tokens(self, coins_list):
        """
        Process coins list and create Token records for each multi-chain TokenMaster token
        Creates native Token records for tokens without platform contracts

        Args:
            coins_list: List of dictionaries cointaining token data and chain dictionaries
        """
        success_count = 0
        error_count = 0
        
        for coin_data in coins_list:
            try:
                # Validate the API response structure
                serializer = CoinGeckoCoinsListSerializer(data=coin_data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    coingecko_id = validated_data['id'] # type: ignore

                        # Find the corresponding TokenMaster
                    try:
                        token_master = TokenMaster.objects.get(coingecko_id=coingecko_id)
                    except TokenMaster.DoesNotExist:
                        error_count += 1
                        continue

                    # Extract platform/contract data
                    platforms = serializer.get_chain_contracts(validated_data)

                    if platforms:
                        if coingecko_id == "binancecoin":
                            platforms['binance-smart-chain'] = 'native'
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
                                success_count += 1
                    else:
                        # No platfors = native token
                        if coingecko_id in COINGECKO_NATIVE_TOKEN_MAPPING:
                            chains = COINGECKO_NATIVE_TOKEN_MAPPING[coingecko_id]

                            for chain in chains:
                                # Create record for each chain where this token is native
                                Token.objects.update_or_create(
                                        master=token_master,
                                        chain=chain,
                                        defaults={
                                            'contract_address': 'native',  # Native tokens have no contract
                                            'coingecko_updated_at': timezone.now(),
                                            }
                                        )
                                success_count += 1

                else:
                    print(f"Validation error for {coin_data['id']}: {serializer.errors}")
                    error_count += 1
                
            except Exception as e:
                print(f"Error processing implementations for {coin_data['id']}: {e}")
                error_count += 1
        
        return success_count, error_count

    def _remove_stale_tokens(self, sync_start_time):
        stale_tokens = TokenMaster.objects.filter(
            coingecko_id__isnull=False,
            coingecko_updated_at__lt=sync_start_time
        )
        return stale_tokens.delete()

