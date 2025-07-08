from django.db import transaction
from django.utils import timezone
from apps.tokens.models import Token, TokenMaster
from apps.prices.models import CoingeckoPrice
from .client import CoinGeckoClient
from .serializers import CoinGeckoCoinsListSerializer, CoinGeckoMarketDataSerializer
from config.chain_mapping import COINGECKO_NATIVE_TOKEN_MAPPING
import time
import psutil
import os
import gc
import logging
from django.db import connection
from django.utils import timezone

# Get Django logger
logger = logging.getLogger(__name__)

class CoinGeckoSyncService:
    def __init__(self):
        self.client = CoinGeckoClient()
        self.process = psutil.Process(os.getpid())
    
    def _log_memory(self, context):
        """Memory logging that works with DEBUG = False"""
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        db_queries = len(connection.queries) if hasattr(connection, 'queries') else 0
        
        logger.warning(f"🔍 MEMORY [{context}]: {memory_mb:.1f} MB | DB: {db_queries} | Growth: {self._memory_growth(memory_mb)}")
        return memory_mb
    
    def _memory_growth(self, current_mb):
        """Track memory growth"""
        if not hasattr(self, '_initial_memory'):
            self._initial_memory = current_mb
            return "BASELINE"
        
        growth = current_mb - self._initial_memory
        if growth > 300:
            return f"+{growth:.1f}MB 🚨CRITICAL"
        elif growth > 200:
            return f"+{growth:.1f}MB ⚠️WARNING" 
        elif growth > 100:
            return f"+{growth:.1f}MB 📈HIGH"
        else:
            return f"+{growth:.1f}MB ✅OK"

    def sync_all(self):
        """Complete sync with logging"""
        logger.warning("🚀 COINGECKO SYNC STARTING")
        self._log_memory("SYNC_START")
        
        market_result = self.sync_market_data()
        self._log_memory("MARKET_COMPLETE")
        
        logger.warning(f"✅ COINGECKO SYNC COMPLETE: {market_result}")
        return f"Market sync: {market_result}"

    def sync_market_data(self):
        """Market data sync with detailed logging"""
        logger.warning("📊 MARKET DATA SYNC STARTING")
        self._log_memory("MARKET_SYNC_START")
        
        try:
            success_count, error_count = self._process_market_data_chunked()
            self._log_memory("MARKET_SYNC_END")
            
            logger.warning(f"📊 Market sync completed: {success_count} successful, {error_count} errors")
            return f"Synced {success_count} tokens, {error_count} errors"

        except Exception as e:
            self._log_memory(f"MARKET_SYNC_ERROR")
            logger.error(f"💥 Market sync failed: {e}")
            raise

    def _process_market_data_chunked(self):
        """Chunked processing with detailed logging"""
        total_success = 0
        total_errors = 0
        page = 1
        
        self._log_memory("CHUNKED_START")
        
        while True:
            self._log_memory(f"PAGE_{page}_FETCH_START")
            
            page_data = self.client.get_coins_markets_single_page(page=page)
            
            if not page_data:
                self._log_memory(f"PAGE_{page}_NO_DATA")
                break
            
            self._log_memory(f"PAGE_{page}_FETCH_END_({len(page_data)}_tokens)")
            
            # Process page
            success_count, error_count = self._process_market_data_page(page_data)
            total_success += success_count
            total_errors += error_count
            
            self._log_memory(f"PAGE_{page}_PROCESS_END")
            
            # Check if last page
            is_last_page = len(page_data) < 250
            
            # Delete page data
            del page_data
            self._log_memory(f"PAGE_{page}_DELETE_END")
            
            # Garbage collect every 5 pages
            if page % 5 == 0:
                collected = gc.collect()
                logger.warning(f"🗑️ PAGE {page} GC: freed {collected} objects")
                self._log_memory(f"PAGE_{page}_GC_END")
            
            logger.warning(f"📄 PAGE {page} COMPLETE: {success_count} success, {error_count} errors")
            
            if is_last_page:
                self._log_memory(f"PAGE_{page}_LAST_PAGE_EXIT")
                break
                
            page += 1
            time.sleep(2.5)
        
        self._log_memory("CHUNKED_COMPLETE")
        logger.warning(f"📊 TOTAL: {total_success} success, {total_errors} errors")
        return total_success, total_errors

    def _process_market_data_page(self, page_data):
        """Process page with batch logging - FIXED TokenMaster issue"""
        success_count = 0
        error_count = 0
        
        # Process in batches of 50
        for i in range(0, len(page_data), 50):
            batch = page_data[i:i + 50]
            batch_num = (i // 50) + 1
            
            for coin_data in batch:
                try:
                    serializer = CoinGeckoMarketDataSerializer(data=coin_data)
                    
                    if serializer.is_valid():
                        validated_data = serializer.validated_data
                        
                        # FIXED: Capture the token_master from update_or_create
                        token_master, created = TokenMaster.objects.update_or_create(
                            coingecko_id=validated_data['id'],
                            defaults={
                                'symbol': validated_data['symbol'],
                                'name': validated_data['name'],
                                'image': validated_data['image'],
                                'coingecko_rank': validated_data['market_cap_rank'],
                                'coingecko_updated_at': timezone.now(),
                            }
                        )
                        
                        # FIXED: Now token_master is properly defined
                        CoingeckoPrice.objects.update_or_create(
                            token_master=token_master,
                            defaults={
                                'price_usd': validated_data['current_price'],
                            }
                        )
                        
                        success_count += 1
                        
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
            
            # Log every batch
            self._log_memory(f"BATCH_{batch_num}_END")
            del batch
        
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

