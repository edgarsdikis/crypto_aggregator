from decimal import Decimal
from ..models import WalletTokenBalance
from apps.prices.models import CoingeckoPrice
from apps.wallets.models import UserWallet
from config.chain_mapping import FRONTEND_TO_COINGECKO_MAPPING

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

    def get_wallet_detailed_assets(self, user, address, chain):
        """
        Get detailed token list with balances and USD values for a specific wallet
        
        Args:
            user: User instance
            address: Wallet address string
            chain: Chain name string (frontend variant)
            
        Returns:
            dict: Formatted wallet data with detailed token list
            
        Raises:
            ValueError: If wallet not found or doesn't belong to user
        """
        coingecko_chain_name = FRONTEND_TO_COINGECKO_MAPPING[chain]

        try:
            user_wallet = UserWallet.objects.select_related('wallet').get(
                user=user,
                wallet__address=address,
                wallet__chain=coingecko_chain_name
            )
            wallet = user_wallet.wallet
            
            # Get all token balances
            token_balances = WalletTokenBalance.objects.filter(
                wallet=wallet
            ).select_related(
                'token__master__coingecko_price'
            )
            
            tokens_data = []
            
            for token_balance in token_balances:
                usd_value = self.calculate_token_balance_usd(token_balance)

                token_data = {
                    "token_details": {
                        "address": token_balance.token.contract_address,
                        "chain": token_balance.token.chain,
                        "symbol": token_balance.token.master.symbol,
                        "name": token_balance.token.master.name,
                        "logo": token_balance.token.master.image
                    },
                    "token_balance": {
                        "token_balance_formatted": str(token_balance.balance),
                        "usd_value": str(usd_value)
                    }
                }
                
                tokens_data.append(token_data)
            
            return {
                "wallet_name": user_wallet.name,
                "wallet_address": wallet.address,
                "wallet_chain": wallet.chain,
                "tokens": tokens_data
            }
            
        except UserWallet.DoesNotExist:
            raise ValueError("Wallet not found or doesn't belong to user")

    def get_user_aggregated_portfolio(self, user):
        """
        Get aggregated portfolio across all user wallets
        
        Args:
            user: User instance
            
        Returns:
            dict: Aggregated portfolio with tokens list, sorted by USD value
        """
        try:
            # Get all user wallets
            user_wallets = UserWallet.objects.select_related('wallet').filter(user=user)
            
            # Check if user has any wallets
            if not user_wallets.exists():
                return {
                    "message": "User has no wallets",
                    "tokens": []
                }
            
            # Extract wallet instances
            wallet_instances = [uw.wallet for uw in user_wallets]
            
            # Get all token balances across all wallets
            all_token_balances = WalletTokenBalance.objects.filter(
                wallet__in=wallet_instances
            ).select_related(
                'token__master__coingecko_price'
            )
            
            # Aggregate tokens by (contract_address, chain)
            aggregated_tokens = self._aggregate_token_balances(all_token_balances)
            
            # Sort by USD value (highest first)
            aggregated_tokens.sort(
                key=lambda token: Decimal(token['token_balance']['usd_value']), 
                reverse=True
            )
            
            return {
                "tokens": aggregated_tokens
            }
            
        except Exception as e:
            print(f"Error getting aggregated portfolio: {e}")
            return {
                "message": "Error retrieving portfolio data",
                "tokens": []
            }

    def _aggregate_token_balances(self, token_balances):
        """
        Aggregate token balances by (contract_address, chain)
        Handles partial failures gracefully
        
        Args:
            token_balances: QuerySet of WalletTokenBalance instances
            
        Returns:
            list: Aggregated token data
        """
        # Dictionary to group tokens: key = (contract_address, chain)
        token_groups = {}
        
        for token_balance in token_balances:
            try:
                # Create unique key for this token
                key = (
                    token_balance.token.contract_address,
                    token_balance.token.chain
                )
                
                # Calculate USD value (might fail for tokens without prices)
                usd_value = self.calculate_token_balance_usd(token_balance)
                
                if key not in token_groups:
                    # First time seeing this token
                    token_groups[key] = {
                        'token_balance_sum': token_balance.balance,
                        'usd_value_sum': usd_value,
                        'token_details': {
                            "address": token_balance.token.contract_address,
                            "chain": token_balance.token.chain,
                            "symbol": token_balance.token.master.symbol,
                            "name": token_balance.token.master.name,
                            "logo": token_balance.token.master.image
                        }
                    }
                else:
                    # Add to existing token
                    token_groups[key]['token_balance_sum'] += token_balance.balance
                    token_groups[key]['usd_value_sum'] += usd_value
                    
            except Exception as e:
                # Log the error but continue processing other tokens
                print(f"Error processing token {token_balance.token}: {e}")
                continue
        
        # Convert to the response format
        aggregated_tokens = []
        for token_data in token_groups.values():
            aggregated_token = {
                "token_details": token_data['token_details'],
                "token_balance": {
                    "token_balance_formatted": str(token_data['token_balance_sum']),
                    "usd_value": str(token_data['usd_value_sum'])
                }
            }
            aggregated_tokens.append(aggregated_token)
        
        return aggregated_tokens
