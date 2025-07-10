from celery import shared_task
from django.utils import timezone
from .services import CoinGeckoSyncService

@shared_task
def sync_market_data_and_cleanup_task():
    """Market data sync + stale token removal"""
    try:
        sync_start_time = timezone.now()
        service = CoinGeckoSyncService()
        
        # Market sync
        market_result = service.sync_market_data()
        
        # Stale token cleanup
        deleted_count, _ = service._remove_stale_tokens(sync_start_time)
        
        return f"Market sync: {market_result}. Removed {deleted_count} stale tokens"
        
    except Exception as e:
        print(f"Market sync and cleanup failed: {e}")
        raise

@shared_task
def sync_multichain_tokens_task():
    """Multi-chain tokens sync"""
    try:
        service = CoinGeckoSyncService()
        result = service.sync_multi_chain_tokens()
        return f"Multi-chain sync: {result}"
    except Exception as e:
        print(f"Multi-chain sync failed: {e}")
        raise
