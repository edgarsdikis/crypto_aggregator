from django.db import transaction
from django.utils import timezone
from apps.tokens.models import Token, TokenMaster
from apps.prices.models import CoingeckoPrice
from .client import CoinGeckoClient
from .serializers import CoinGeckoCoinsListSerializer, CoinGeckoMarketDataSerializer
from config.chain_mapping import COINGECKO_NATIVE_TOKEN_MAPPING
import time

class CoinGeckoSyncService:
    """Service for syncing CoinGecko token data and prices"""

    def __init__(self):
        self.client = CoinGeckoClient()
    
    def sync_all(self):
        """
        Complete sync: market data first, then implementations
        """
        print("Starting complete CoinGecko sync...")
        market_result = self.sync_market_data()
        # multi_chain_result = self.sync_multi_chain_tokens()
        
        return f"Complete sync: {market_result}"

    def sync_market_data(self):
        """
        Process market data page by page to minimize memory usage
        """
        print("Starting memory-optimized CoinGecko market data sync...")
        # sync_start_time = timezone.now()

        try:
            success_count, error_count = self._process_market_data_chunked()
            # self._remove_stale_tokens(sync_start_time)
            
            print(f"Market sync completed: {success_count} successful, {error_count} errors")
            return f"Synced {success_count} tokens, {error_count} errors"

        except Exception as e:
            print(f"Market sync failed: {e}")
            raise

    def _process_market_data_chunked(self):
        """Process market data page by page to minimize memory usage"""
        total_success = 0
        total_errors = 0
        page = 1
        
        while True:
            print(f"Processing page {page}...")
            
            # Fetch one page at a time
            page_data = self.client.get_coins_markets_single_page(page=page)
            
            if not page_data:  # No more data
                print(f"No data on page {page}, ending pagination")
                break
                
            print(f"Got {len(page_data)} tokens on page {page}")
            
            # Process this page immediately
            success_count, error_count = self._process_market_data_page(page_data)
            total_success += success_count
            total_errors += error_count
            
            # If we got less than the full page size, we're done
            if len(page_data) < 250:
                del page_data
                break

            # Explicitly delete the page data to free memory
            del page_data
            
            print(f"Page {page} processed: {success_count} success, {error_count} errors")
            
                
            page += 1
            
            time.sleep(2.5)
        
        print(f"Total processed: {total_success} success, {total_errors} errors")
        return total_success, total_errors


    # @transaction.atomic  
    def _process_market_data_page(self, page_data):
        """
        Process a single page of market data
        This is similar to your existing _process_market_data but for one page
        """
        success_count = 0
        error_count = 0
        
        for coin_data in page_data:
            try:
                # Validate the API response structure
                serializer = CoinGeckoMarketDataSerializer(data=coin_data)
                
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    
                    # Create or update TokenMaster
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
                    
                    # Create or update price records
                    CoingeckoPrice.objects.update_or_create(
                        token_master=token_master,
                        defaults={
                            'price_usd': validated_data['current_price'], # type: ignore
                        }
                    )
                    
                    success_count += 1
                    
                else:
                    # Handle validation errors
                    print(f"Validation error for {coin_data.get('id', 'unknown')}: {serializer.errors}")
                    error_count += 1
                    
            except Exception as e:
                print(f"Database error processing {coin_data.get('id', 'unknown')}: {e}")
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
        
        stale_count = stale_tokens.count()
        if stale_count > 0:
            stale_tokens.delete()
            print(f"Removed {stale_count} stale tokens")

