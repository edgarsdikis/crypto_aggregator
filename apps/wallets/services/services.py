from apps.integrations.alchemy.client import AlchemyClient
from apps.integrations.alchemy.service import AlchemyWalletService
from ..models import Wallet, UserWallet
from ...portfolio.models import WalletTokenBalance
from ...tokens.models import Token, TokenMaster
from config.chain_mapping import ALCHEMY_NETWORK_MAPPING, NETWORK_MAPPING



class WalletService:
    """Service class for wallet operations"""

    def __init__(self):
        self.alchemy_client = AlchemyClient()
        self.alchemy_service = AlchemyWalletService()

    def add_wallet(self, user, address, chain, name=None):
        """
        Add a new wallet for an authenticated user

        Args:
            user: The user object
            address: Wallet address (str)
            chain: Blockchain network (str)
            name: Custom user wallet name (str)

        Returns:
            dict: Success response with wallet info
            
        Raises:
            ValueError: If wallet already exists or validation fails
            Exception: If external API fails
        """
        coingecko_chain_name = self._convert_chain_to_coingecko_name(chain)

        # Check if user has this wallet
        if self._wallet_exists_for_user(user, address, coingecko_chain_name):
            raise ValueError("You already have this wallet added")

        # Validate wallet with Alchemy and get token balances
        try:
            alchemy_network = self._convert_chain_to_alchemy_chain_name(chain)
            networks = [alchemy_network]
            response_data = self.alchemy_client.get_wallet_balances(address, networks)
            valid_tokens = self.alchemy_service.process_wallet_balances(response_data)
        except Exception as e:
            raise Exception(f"Failed to validate wallet with Alchemy: {str(e)}")

        # Create database records for Wallet, UserWallet models
        wallet = self._get_or_create_wallet(address, coingecko_chain_name)
        user_wallet = self._create_user_wallet(user, wallet, name)

        #  database records for WalletTokenBalance model
        self._create_token_balances(wallet, valid_tokens, coingecko_chain_name)

        return {
                'address': address,
                'chain': coingecko_chain_name,
                'name': name,
                'token_count': len(valid_tokens)
                }

    def _wallet_exists_for_user(self, user, address, chain):
        """Check if user already has this wallet"""
        return UserWallet.objects.filter(
                user=user,
                wallet__address=address,
                wallet__chain=chain
                ).exists()

    def _convert_chain_to_alchemy_chain_name(self, chain):
        """Convert our chain name to Alchemy network name"""
       # Create reverse mapping from your existing ALCHEMY_NETWORK_MAPPING
        return NETWORK_MAPPING[chain]

    def _convert_chain_to_coingecko_name(self, chain):
        """Convert our chain name to Coingecko name"""
        alchemy_network = self._convert_chain_to_alchemy_chain_name(chain)
        return ALCHEMY_NETWORK_MAPPING[alchemy_network]['coingecko_name']

    def _get_or_create_wallet(self, address, chain):
        """Get existing wallet or create new one"""
        wallet, created = Wallet.objects.get_or_create(
                address=address,
                chain=chain
                )
        return wallet

    def _create_user_wallet(self, user, wallet, name):
        """Create UserWallet record"""
        user_wallet = UserWallet.objects.create(
                user=user,
                wallet=wallet,
                name=name
                )
        return user_wallet

    def _create_token_balances(self, wallet, valid_tokens, chain):
        """Create WalletTokenBalance records"""
        for token_data in valid_tokens:
            try:
                contract_address = token_data['contract_address']
                
                if contract_address is None:
                    # Native token
                    token = Token.objects.get(
                        chain=chain,
                        contract_address="native"
                    )
                else:
                    # Contract token
                    token = Token.objects.get(
                        contract_address=contract_address,
                        chain=chain
                    )

                WalletTokenBalance.objects.create(
                        wallet=wallet,
                        token=token,
                        balance=token_data['decimal_balance']
                        )
            except Token.DoesNotExist:
                print(f"Token not found: {token_data['contract_address']} on {chain}")
                continue
            except Exception as e:
                print(f"Error creating balance record: {e}")
                continue

    def remove_wallet(self, user, address, chain):
        """
        Remove a wallet from a user's portfolio
        
        Args:
            user: The user object
            address (str): Wallet address
            chain (str): Blockchain network
            
        Returns:
            tuple: (success_bool, message_or_error)
        """
        try:
            # Find and delete the wallet-user relationship
            deleted_count, _ = UserWallet.objects.filter(
                user=user,
                wallet__address=address,
                wallet__chain=chain
            ).delete()
            
            # Check if any records were deleted
            if deleted_count == 0:
                return False, f"Wallet with address {address} on chain {chain} not found in your portfolio"
                
            return True, f"Wallet {address} ({chain}) has been removed from your portfolio"
            
        except Exception as e:
            return False, f"Failed to remove wallet: {str(e)}"

    def update_wallet_name(self, user, address, chain, new_name):
        """
        Update the custom name for a user's wallet
        
        Args:
            user: The user object  
            address (str): Wallet address
            chain (str): Blockchain network
            new_name (str): New custom name (can be empty to remove)
            
        Returns:
            tuple: (success_bool, message_or_error)
        """
        try:
            coingecko_chain_name = self._convert_chain_to_coingecko_name(chain)
            
            # Find the user wallet relationship
            user_wallet = UserWallet.objects.select_related('wallet').get(
                user=user,
                wallet__address=address,
                wallet__chain=coingecko_chain_name
            )
            
            # Update the name
            if new_name and new_name.strip():
                user_wallet.name = new_name.strip()
            else:
                user_wallet.name = None
            
            user_wallet.save()
            return True, f"Wallet name updated successfully"
            
        except UserWallet.DoesNotExist:
            return False, f"Wallet with address {address} on chain {chain} not found in your portfolio"
        except Exception as e:
            return False, f"Failed to update wallet name: {str(e)}"
