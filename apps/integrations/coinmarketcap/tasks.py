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
        print(f"CoinMarketCap IDs sync failed: {e}")


@shared_task
def sync_coinmarketcap_token_metadata():
    """
    Celery task to sync CoinMarketCap token metadata

    This task should be run weekly to update our token metadata
    """
    try:
        service = CoinMarketCapSyncService()
        service.sync_token_metadata()
        return "CoinMarketCap token metadata sync completed successfully"
    except Exception as e:
        print(f"CoinMarketCap token metadata sync failed: {e}")


@shared_task
def sync_coinmarketcap_token_prices():
    """
    Celery task to sync CoinMarketCap token price data

    This tas should be run [PLACE HOLDER] to update our token prices
    """
    try:
        service = CoinMarketCapSyncService()
        service.sync_token_prices()
        return "CoinMarketCap token prices sync completed successfully"
    except Exception as e:
        print(f"CoinMarketCap token price sync failed: {e}")
