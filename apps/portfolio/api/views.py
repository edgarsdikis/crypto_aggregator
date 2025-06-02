from apps.portfolio.services.service import PortfolioService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import WalletListSerializer

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
