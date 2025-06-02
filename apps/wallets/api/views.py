from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AddWalletSerializer
from ..services.services import WalletService
from drf_spectacular.utils import extend_schema
from config.chain_mapping import NETWORK_MAPPING
from apps.portfolio.services.service import PortfolioService

class AddWalletView(APIView):
    """Add a new wallet to user's portfolio"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add wallet to portfolio",
        description="Add a new cryptocurrency wallet to the authenticated user's portfolio",
        request=AddWalletSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "chain": {"type": "string"},
                    "name": {"type": "string"},
                    "status": {"type": "string"},
                    "token_count": {"type": "integer"}
                }
            },
            400: {
                "type": "object", 
                "properties": {
                    "address": {"type": "string"},
                    "chain": {"type": "string"},
                    "status": {"type": "string"},
                    "error": {"type": "string"}
                }
            }
        },
        tags=["Wallets"]
    )

    def post(self, request):
        """Add a new wallet"""
        # Validate input data
        serializer = AddWalletSerializer(
                data=request.data, 
                context={'request': request}
                )
        
        if not serializer.is_valid():
            return Response({
                "status": "Failure",
                "error": "Invalid input data",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.validated_data['address'] # type: ignore
        chain = serializer.validated_data['chain'] # type: ignore
        name = serializer.validated_data['name'] # type: ignore

        # Add the wallet
        try:
            wallet_serivce = WalletService()
            result = wallet_serivce.add_wallet(
                    user=request.user,
                    address=address,
                    chain=chain,
                    name=name
                    )

            # Success response
            return Response({
                "address": result['address'],
                "chain": result['chain'],
                "name": result['name'],
                "status": "Success",
                "token_count": result['token_count']
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            # User error (wallet already exists, etc.)
            return Response({
                "address": address,
                "chain": chain,
                "status": "Failure", 
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # External API error or other issues
            return Response({
                "address": address,
                "chain": chain, 
                "status": "Failure",
                "error": f"Failed to add wallet: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)


class RemoveWalletView(APIView):
    """Remove a wallet from user's portfolio"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Remove wallet from portfolio",
        description="Remove a cryptocurrency wallet from the authenticated user's portfolio",
        request=AddWalletSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "status": {"type": "string"}
                }
            },
            400: {
                "type": "object", 
                "properties": {
                    "error": {"type": "string"},
                    "status": {"type": "string"}
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "status": {"type": "string"}
                }
            }
        },
        tags=["Wallets"]
    )
    def post(self, request):
        """Remove a wallet"""
        # Validate input data
        serializer = AddWalletSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "Failure",
                "error": "Invalid input data",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.validated_data['address'] # type: ignore
        chain = serializer.validated_data['chain'] # type: ignore

        # Remove the wallet
        wallet_service = WalletService()
        success, message = wallet_service.remove_wallet(
            user=request.user,
            address=address,
            chain=chain
        )

        if success:
            return Response({
                "status": "Success",
                "message": message
            }, status=status.HTTP_200_OK)
        else:
            # Check if it's a "not found" error or server error
            if "not found" in message.lower():
                return Response({
                    "status": "Failure", 
                    "error": message
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "status": "Failure",
                    "error": message
                }, status=status.HTTP_400_BAD_REQUEST)


class SupportedChainsView(APIView):
    """Get supported blockchain networks"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Get supported chains",
        description="Returns list of supported blockchain networks",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "supported_chains": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        },
        tags=["Wallets"]
    )
    def get(self, request):
        """
        Get a list of supported blockchain networks
        
        Returns:
            list: List of supported chains
        """
        return Response({
            "supported_chains": list(NETWORK_MAPPING.keys())
        })

class UpdateWalletNameView(APIView):
    """Update custom name for a wallet"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update wallet custom name",
        description="Update or remove the custom name for a wallet in the authenticated user's portfolio",
        request=AddWalletSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            },
            400: {
                "type": "object", 
                "properties": {
                    "error": {"type": "string"}
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        },
        tags=["Wallets"]
    )
    def put(self, request):
        """Update wallet custom name"""
        # Validate input data
        serializer = AddWalletSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "error": "Invalid input data",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.validated_data['address'] # type: ignore
        chain = serializer.validated_data['chain'] # type: ignore
        new_name = serializer.validated_data.get('name', '') # type: ignore

        wallet_service = WalletService()
        success, message = wallet_service.update_wallet_name(
            user=request.user,
            address=address,
            chain=chain,
            new_name=new_name
        )

        if success:
            return Response({
                "message": message
            }, status=status.HTTP_200_OK)
        else:
            # Determine if it's a not found error or server error
            if "not found" in message.lower():
                return Response({
                    "error": message
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "error": message
                }, status=status.HTTP_400_BAD_REQUEST)


class SyncWalletsView(APIView):
    """Sync all user wallets with fresh balance data"""
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Sync all user wallets", 
        description="Fetch fresh balance data for all user wallets from Alchemy API",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "wallet_address": {"type": "string"},
                                "chain": {"type": "string"}, 
                                "token_count": {"type": "integer"},
                                "status": {"type": "string"},
                                "error": {"type": "string", "nullable": True}
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total_wallets": {"type": "integer"},
                            "successful": {"type": "integer"},
                            "failed": {"type": "integer"}
                        }
                    }
                }
            }
        },
        tags=["Wallets"]
    )
    def get(self, request):
        """Sync all wallets for the authenticated user"""
        try:
            wallet_service = WalletService()
            sync_results = wallet_service.sync_user_wallets(request.user)
            
            return Response(sync_results, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Sync failed: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
