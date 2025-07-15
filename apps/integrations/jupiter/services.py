from django.db import transaction
from apps.tokens.models import Token, SolanaTokenDecimals
from .client import JupiterClient
from .serializers import JupiterTaggedCoinsSerializer
from django.utils import timezone

class JupiterSyncService:

    def __init__(self):
        self.client = JupiterClient()
    
    def sync_solana_decimals(self):
        """Sync Solana token decimals from Jupiter verified tokens"""
        print("Starting Jupiter Solana decimal sync...")
        try:
            jupiter_data = self.client.get_tagged_coins()
            print(f"Fetched {len(jupiter_data)} tokens from Jupiter")

            sync_start_time = timezone.now()
            success_count, error_count = self._process_jupiter_tokens(jupiter_data)
            self._remove_stale_tokens(sync_start_time)
            print(f"Decimals sync completed: {success_count} successful, {error_count} errors")
            return f"Synced {success_count} decimals, {error_count} errors"

        except Exception as e:
            print(f"Jupiter decimals sync failed: {e}")
            raise

    @transaction.atomic
    def _process_jupiter_tokens(self, jupiter_data):
        """Process Jupiter tokens and update/create decimals records"""
        success_count = 0
        error_count = 0

        # Get all Solana tokens
        solana_tokens = Token.objects.filter(chain='solana')
        print(f"Found {solana_tokens.count()} existing Solana tokens")

        # Create a lookup dict
        token_lookup = {token.contract_address: token for token in solana_tokens}

        for jupiter_token_data in jupiter_data:
            try:
                serializer = JupiterTaggedCoinsSerializer(data=jupiter_token_data)
                if serializer.is_valid():
                    # Use 'id' from Token API V2 (this is the mint address)
                    jupiter_address = serializer.validated_data['id']
                    jupiter_decimals = serializer.validated_data['decimals']
                else:
                    print(f"Invalid Jupiter data: {serializer.errors}")
                    error_count += 1
                    continue

                token = token_lookup.get(jupiter_address)
                if not token:
                    continue

                SolanaTokenDecimals.objects.update_or_create(
                    token=token,
                    defaults={
                        'decimals': jupiter_decimals,
                        'jupiter_updated': timezone.now()
                    }
                )
                success_count += 1
            
            except Exception as e:
                print(f"Error processing Jupiter token {jupiter_token_data.get('id', 'unknown')}: {e}")
                error_count += 1

        return success_count, error_count

    def _remove_stale_tokens(self, sync_start_time):
        stale_tokens = SolanaTokenDecimals.objects.filter(
            jupiter_updated__lt=sync_start_time
        )
        
        stale_count = stale_tokens.count()
        if stale_count > 0:
            stale_tokens.delete()
            print(f"Removed {stale_count} stale tokens")
