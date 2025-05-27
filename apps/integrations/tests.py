from django.test import TestCase

# Simple test script for CoinMarketCap backgroud tasks
from apps.integrations.coinmarketcap.tasks import sync_coinmarketcap_token_ids, sync_coinmarketcap_token_metadata, sync_coinmarketcap_token_prices

# Run ID sync
print("=== ID SYNC ===")
result1 = sync_coinmarketcap_token_ids()
print(result1)

# Run metadata sync  
print("=== METADATA SYNC ===")
result2 = sync_coinmarketcap_token_metadata()
print(result2)

# Run price sync
print("=== PRICE SYNC ===")
result3 = sync_coinmarketcap_token_prices()
print(result3)

# Quick check
from apps.tokens.models import Token
print(f"Total tokens: {Token.objects.count()}")
