from apps.portfolio.services.service import PortfolioService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import WalletListSerializer, WalletAssetsSerializer, WalletAssetsRequestSerializer, UserPortfolioSerializer

class UserWalletsListView(APIView):
    """Get all wallets for authenticated user with USD balances"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List user wallets",
        description="Returns all wallets for the authenticated user with current USD balances",
        responses={
            200: WalletListSerializer(many=True),
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
            500: {"type": "object", "properties": {"error": {"type": "string"}}}
        },
        tags=["Portfolio"]
    )
    def get(self, request):
        """Get all user wallets with USD balances"""
        try:
            # Use the portfolio service to get wallets with balances
            portfolio_service = PortfolioService()
            wallets_data = portfolio_service.get_user_wallets_with_balances(request.user)
            
            # Serialize the response
            serializer = WalletListSerializer(wallets_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve wallets: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletAssetsView(APIView):
    """Get detailed token list for a specific wallet"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get wallet assets",
        description="Returns detailed token list with balances and USD values for a specific wallet",
        request=WalletAssetsRequestSerializer,
        responses={
            200: WalletAssetsSerializer,
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            403: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        },
        tags=["Portfolio"]
    )
    def post(self, request):
        # Validate input
        address = request.data.get('address')
        chain = request.data.get('chain')
        
        if not address or not chain:
            return Response({
                "error": "Both address and chain are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            portfolio_service = PortfolioService()
            wallet_data = portfolio_service.get_wallet_detailed_assets(
                user=request.user,
                address=address,
                chain=chain
            )
            
            serializer = WalletAssetsSerializer(wallet_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve wallet assets: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserPortfolioView(APIView):
    """Get aggregated portfolio across all user wallets"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get aggregated user portfolio",
        description="Returns aggregated tokens across all user wallets, sorted by USD value",
        responses={
            200: UserPortfolioSerializer,
            401: {"type": "object", "properties": {"error": {"type": "string"}}},
            500: {"type": "object", "properties": {"error": {"type": "string"}}}
        },
        tags=["Portfolio"]
    )
    def get(self, request):
        try:
            portfolio_service = PortfolioService()
            portfolio_data = portfolio_service.get_user_aggregated_portfolio(request.user)
            
            # Check if it's a "no wallets" response
            if "message" in portfolio_data and portfolio_data["message"] == "User has no wallets":
                return Response({
                    "message": "User has no wallets",
                    "tokens": []
                }, status=status.HTTP_200_OK)
            
            # Use serializer for normal response
            serializer = UserPortfolioSerializer(portfolio_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve portfolio: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
