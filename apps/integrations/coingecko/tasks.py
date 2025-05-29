from celery import shared_task
from .services import CoinGeckoSyncService

@shared_task
def sync_coingecko_tokenmaster_token_coingeckoprices_models():
    """
    Celery task to sync TokenMaster, Token and CoingeckoPrices models using CoinGecko "Market Data" and "Coins List (ID map)" endpoints

    This task should be run as frequently as possible based on API plan to store the fresh token data
    """

    try:
        service = CoinGeckoSyncService()
        service.sync_all()
        return "CoinGecko TokenMaster, Token, CoingeckoPrices sync completed successfully"

    except Exception as e:
        print(f"CoinGecko TokenMaster, Token, CoingeckoPrices sync failed: {e}")
