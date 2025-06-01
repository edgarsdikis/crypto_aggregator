from celery import shared_task
from .services import JupiterSyncService

@shared_task
def sync_jupiter_solana_decimals_model():
    """
    Celery task to sync SolanaTokenDecimals model using Jupiter "Tagged Tokens" API endpoint

    This task should be run right after Coingeck tasks
    """

    try:
        service = JupiterSyncService()
        service.sync_solana_decimals()
        return "SolanaTokenDecimals sync completed successfully"

    except Exception as e:
        print(f"SolanaTokenDecimals sync failed: {e}")
