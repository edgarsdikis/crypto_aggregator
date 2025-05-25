from celery import shared_task
from .services import CoinMarketCapSyncService

@shared_task
def sync_coinmarketcap_token_ids():
    """
    Celery task to sync CoinMarketCap token IDs

    This task should be run weekly to update our token ID mappings
    """
    try:
        service = CoinMarketCapSyncService()
        service.sync_token_ids()
        return "CoinMarketCap token ID sync completed successfully"
    except Exception as e:
        print(f"CoinMarketCap sync failed: {e}")

