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
        multichain_result = self.sync_multi_chain_tokens()
        return f"Market sync: {market_result}.  Removed {deleted_count} stale tokens. Multichain sync: {multichain_result}"

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
        """Memory-efficient multi-chain sync"""
        print("Starting CoinGecko token multi-chain sync...")
        try:
            coins_list = self.client.get_coins_list(include_platform=True)

            total_success = 0
            total_errors = 0
            chunk_size = 100  # Process 100 tokens at a time

            # Process in chunks
            for i in range(0, len(coins_list), chunk_size):
                chunk = coins_list[i:i + chunk_size]
                success_count, error_count = self._process_multi_chain_tokens_chunk(chunk)
                
                total_success += success_count
                total_errors += error_count
                
                # Clean up chunk
                del chunk
                
                # Garbage collect every 5 chunks
                if (i // chunk_size + 1) % 5 == 0:
                    gc.collect()

            print(f"Multi-chain sync completed: {total_success} successful, {total_errors} errors")
            return f"Created {total_success} token implementations, {total_errors} errors"

        except Exception as e:
            print(f"Multi-chain sync failed: {e}")
            raise

    @transaction.atomic
    def _process_multi_chain_tokens_chunk(self, chunk):
        """Process a chunk of coins with batch database lookups"""
        success_count = 0
        error_count = 0
        
        # Batch lookup TokenMasters for this chunk
        coingecko_ids = [coin['id'] for coin in chunk if 'id' in coin]
        token_masters = {
            tm.coingecko_id: tm 
            for tm in TokenMaster.objects.filter(coingecko_id__in=coingecko_ids)
        }
        
        for coin_data in chunk:
            try:
                serializer = CoinGeckoCoinsListSerializer(data=coin_data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    coingecko_id = validated_data['id'] # type: ignore

                    token_master = token_masters.get(coingecko_id)
                    if not token_master:
                        error_count += 1
                        continue

                    platforms = validated_data.get("platforms", {}) # type: ignore
                    if platforms:
                        if coingecko_id == "binancecoin":
                            platforms['binance-smart-chain'] = 'native'
                        
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
                        # Handle native tokens
                        if coingecko_id in COINGECKO_NATIVE_TOKEN_MAPPING:
                            chains = COINGECKO_NATIVE_TOKEN_MAPPING[coingecko_id]
                            for chain in chains:
                                Token.objects.update_or_create(
                                    master=token_master,
                                    chain=chain,
                                    defaults={
                                        'contract_address': 'native',
                                        'coingecko_updated_at': timezone.now(),
                                    }
                                )
                                success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                print(f"Error processing {coin_data.get('id', 'unknown')}: {e}")
                error_count += 1
        
        return success_count, error_count

    def _remove_stale_tokens(self, sync_start_time):
        stale_tokens = TokenMaster.objects.filter(
            coingecko_id__isnull=False,
            coingecko_updated_at__lt=sync_start_time
        )
        return stale_tokens.delete()

