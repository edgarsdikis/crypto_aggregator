from django.db import transaction

from apps.tokens.models import TokenExternalId

from .client import CoinMarketCapClient
from .serializers import CoinMarketCapTokenMapSerializer


class CoinMarketCapSyncService:
    """
    Service for syncing CoinMarketCap token IDs and metadata
    """

    def __init__(self):
        self.client = CoinMarketCapClient()

    def sync_token_ids(self):
        """
        Fetch and sync all token IDs from CoinMarketCap
        """

        print("Starting CoinMarketCap token IDs sync...")

        # TODO: implement pagination to get all the tokens

        tokens_data = self.client.get_cmc_crypto_map(start=1, limit=5000)
        self._process_and_save_tokens(tokens_data)

        print(f"Sync completed. Processed {len(tokens_data)} tokens")

    @transaction.atomic
    def _process_and_save_tokens(self, tokens_data):
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
                            coinmarketcap_id=serializer.validated_data["id"], # type: ignore
                            name=serializer.validated_data["name"], # type: ignore
                            symbol=serializer.validated_data["symbol"], # type: ignore
                    )
                    success_count += 1
                except Exception as e:
                    print(f"Database error for token {serializer.validated_data['id']}: {e}")  # type: ignore
                    error_count += 1
            else:
                print(f"Validation error for token: {serializer.errors}")
                error_count += 1

        print(f"Sync completed: {success_count} successful, {error_count} errors")
