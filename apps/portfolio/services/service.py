from decimal import Decimal
from django.db.models import Sum
from ..models import WalletTokenBalance
from apps.prices.models import CoingeckoPrice
from apps.wallets.models import UserWallet

class PortfolioService:
    """Service for portfolio calculations and USD value computations"""

    def calculate_token_balance_usd(self, wallet_token_balance):
        """
        Calculate USD value for a single token balance
        
        Args:
            wallet_token_balance: WalletTokenBalance instance
            
        Returns:
            Decimal: USD value of the token balance
        """
        try:
            # WalletTokenBalance -> Token -> TokenMaster -> CoingeckoPrice
            price_usd = wallet_token_balance.token.master.coingecko_price.price_usd
            
            # Calculate USD value: balance × price
            usd_value = wallet_token_balance.balance * price_usd
            
            return usd_value
        except CoingeckoPrice.DoesNotExist:
            print(f"No CoinGecko price for token: {wallet_token_balance.token.master.name}")
            return Decimal('0')
        except AttributeError:
            print(f"Missing relationship data for token: {wallet_token_balance.token}")
            return Decimal('0')
        except Exception as e:
            print(f"Error calculating USD value: {e}")
            return Decimal('0')
        

    def calculate_wallet_total_usd(self, wallet):
        """
        Calculate total USD value for all tokens in a wallet
        
        Args:
            wallet: Wallet instance
            
        Returns:
            Decimal: Total USD value of the wallet
        """
        try:
            # Get all token balances for this wallet
            token_balances = WalletTokenBalance.objects.filter(wallet=wallet)
            
            total_usd = Decimal('0')
            
            # Calculate USD value for each token and sum them up
            for token_balance in token_balances:
                token_usd = self.calculate_token_balance_usd(token_balance)
                total_usd += token_usd
            
            return total_usd
            
        except Exception as e:
            print(f"Error calculating wallet total USD: {e}")
            return Decimal('0')

    def get_user_wallets_with_balances(self, user):
        """
        Get all wallets for a user with their USD balances
        
        Args:
            user: User instance
            
        Returns:
            List of dicts with wallet info and USD balance
        """
        try:
            # Get all wallets for this user through UserWallet relationship
            user_wallets = UserWallet.objects.select_related('wallet').filter(user=user)
            
            wallets_data = []
            
            for user_wallet in user_wallets:
                wallet = user_wallet.wallet
                
                # Calculate total USD balance for this wallet
                balance_usd = self.calculate_wallet_total_usd(wallet)
                
                # Create the response data
                wallet_data = {
                    'address': wallet.address,
                    'chain': wallet.chain,
                    'balance_usd': str(balance_usd)
                }
                
                wallets_data.append(wallet_data)
            
            return wallets_data
            
        except Exception as e:
            print(f"Error getting user wallets: {e}")
            return []

