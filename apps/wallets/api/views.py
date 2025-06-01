from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import AddWalletSerializer
from ..services.services import WalletService
from drf_spectacular.utils import extend_schema

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

