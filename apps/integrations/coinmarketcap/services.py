from django.db import transaction
from apps.prices.models import Price
from apps.tokens.models import Token, TokenExternalId
from .client import CoinMarketCapClient
from .serializers import CoinMarketCapTokenInfoSerializer, CoinMarketCapTokenMapSerializer, CoinMarketCapTokenPriceSerializer
import time


class CoinMarketCapSyncService:
    """
    Service for syncing CoinMarketCap token IDs and metadata
    """

    def __init__(self):
        self.client = CoinMarketCapClient()

    def sync_token_ids(self):
        """
        Fetch and sync all token IDs from CoinMarketCap
        Uses a complete replace strategy for data freshess
        """

        print("Starting CoinMarketCap token IDs sync...")

        # TODO: implement pagination to get all the tokens

        tokens_data = self.client.get_cmc_crypto_map(start=1, limit=5000)

        print("Clearing existing TokenExternalId records...")
        TokenExternalId.objects.all().delete()
        
        print("Creating fresh TokenExternalId records...")
        self._process_and_save_tokens_ids(tokens_data)

        print(f"Sync completed. Processed {len(tokens_data)} tokens")

    def sync_token_metadata(self):
        """
        Sync detailed token metadata from CoinMarketCap
        Uses a complete replace strategy for data freshness
        """
        print("Starting token metadata sync...")
        all_ids = self._get_all_coinmarketcap_ids()
        
        print("Clearing existing Token records...")
        Token.objects.all().delete()

        batches = self._create_batches(all_ids, batch_size=100)

        failed_batches = []
        for batch_num, batch_ids in enumerate(batches, 1):
            success = self._process_batch_metadata(batch_ids, batch_num, len(batches))
            if not success:
                failed_batches.append(batch_num)
        print(f"Token metadata sync completed. Failed batches: {failed_batches}")

    def sync_token_prices(self):
        """Sync token prices from CoinMarketCap"""
        print("Starting token price sync...")
        try:
            token_prices = self.client.get_token_prices(start=1, limit=5000)
            print(f"Fetched {len(token_prices)} from API")
            print("Updating price records...")
            
            success_count, error_count = self._process_and_save_token_prices(token_prices)
            print(f"Token price sync completed: {success_count} successful, {error_count} failed")

        except Exception as e:
            print(f"Failed to fetch token prices: {e}")


    @transaction.atomic
    def _process_and_save_tokens_ids(self, tokens_data):
        """
        Process token data and save to database
        """
        success_count = 0
        error_count = 0

        for token_data in tokens_data:
            serializer = CoinMarketCapTokenMapSerializer(data=token_data)
            if serializer.is_valid():
                try:
                    TokenExternalId.objects.update_or_create(
                        coinmarketcap_id=serializer.validated_data["id"],  # type: ignore
                        name=serializer.validated_data["name"],  # type: ignore
                        symbol=serializer.validated_data["symbol"],  # type: ignore
                    )
                    success_count += 1
                except Exception as e:
                    print(f"Database error for token {serializer.validated_data['id']}: {e}")  # type: ignore
                    error_count += 1
            else:
                print(f"Validation error for token: {serializer.errors}")
                error_count += 1

        print(f"Sync completed: {success_count} successful, {error_count} errors")


    def _get_all_coinmarketcap_ids(self):
        return list(TokenExternalId.objects.values_list('coinmarketcap_id', flat=True))
        
    def _create_batches(self, all_ids, batch_size):
        """Split list into chunks of batch_size"""
        batches = []
        for i in range(0, len(all_ids), batch_size):
            batch = all_ids[i:i + batch_size]
            batches.append(batch)
        return batches
        
    def _process_batch_metadata(self, batch_ids, batch_num, total_batches):
        """
        Process a batch of CoinMarketCap IDs to get token metadata

        Args:
            batch_ids: List of CoinMarketCap IDs
            batch_num: Current batch number (for logging)
            total_batches: Total number of batches (for logging)

        Returns:
            bool: True if successful, False if failed
        """
        if batch_num > 1:
            print(f"Waiting 4 seconds before batch number {batch_num}")
            time.sleep(4)

        success_count = 0
        error_count = 0
        
        try:
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch_ids)} tokens)")
            tokens_data = self.client.get_token_info(batch_ids)
        except Exception as e:
            print(f"API call failed for batch {batch_num}: {e}")
            return False
        
        for cmc_id, token_data in tokens_data.items():
            try:
                # Find the TokenExternalId record
                external_id_record = TokenExternalId.objects.get(coinmarketcap_id=int(cmc_id))
                
                # Validate API data
                serializer = CoinMarketCapTokenInfoSerializer(data=token_data)
                
                if serializer.is_valid():
                    # Create/update Token record with link
                    Token.objects.update_or_create(
                        token_id=external_id_record,
                        defaults={
                            'name': serializer.validated_data['name'], # type: ignore
                            'symbol': serializer.validated_data['symbol'], # type: ignore
                            'logo_url': serializer.validated_data['logo'], # type: ignore
                            'contract_address': serializer.get_contract_address(token_data),
                            'chain': serializer.get_chain(token_data) or 'native',
                        }
                    )
                    success_count += 1
                else:
                    print(f"Validation error for token {cmc_id}: {serializer.errors}")
                    error_count += 1
                    
            except TokenExternalId.DoesNotExist:
                print(f"No TokenExternalId found for CMC ID {cmc_id}")
                error_count += 1
            except Exception as e:
                print(f"Database error for token {cmc_id}: {e}")
                error_count += 1
        
        print(f"Batch {batch_num} completed: {success_count} successful, {error_count} errors")
        return error_count == 0

    @transaction.atomic
    def _process_and_save_token_prices(self, token_prices):
        """
        Process tokens prices and save to database
        Args:
            token_prices: List of token price data from API
        Returns:
            tuple: (success_count, error_count)
        """
        success_count = 0
        error_count = 0
        
        for token_price in token_prices:
            try:
                # Validate API structure
                serializer = CoinMarketCapTokenPriceSerializer(data=token_price)
                if not serializer.is_valid():
                    print(f"Token validation error: {serializer.errors}")
                    error_count += 1
                    continue
                
                cmc_id = serializer.validated_data['id']  # type: ignore
                
                # Find TokenExternalId
                try:
                    external_id_record = TokenExternalId.objects.get(coinmarketcap_id=cmc_id)
                except TokenExternalId.DoesNotExist:
                    print(f"Token with id: {cmc_id} does not exsist in TokenExternalId model")
                    error_count += 1
                    continue

                price = serializer.get_price(token_price)

                if price is None:
                    print(f"No price data for token {cmc_id}")
                    error_count += 1
                    continue

                # Create/Update Price record
                Price.objects.update_or_create(
                    token_id=external_id_record,
                    defaults={
                        'price': price
                    }
                )
                success_count += 1
                
            except Exception as e:
                print(f"Unexpected error processing token: {e}")
                error_count += 1
        
        return success_count, error_count
