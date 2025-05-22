from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from spectacular.schema import validation_error_response

@extend_schema_view(
    post=extend_schema(
        summary="Register new user",
        description="Create a new user account with email and password",
        request=UserRegistrationSerializer,
        responses={
            201: {
                "type": "object", 
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"}
                }
            },
            400: validation_error_response
        },
        tags=["User"]
    )
)


class RegisterView(APIView):
    """Handle user registration"""
    permission_classes = [AllowAny]
    def post(self, request):
        print(f"Registration request data: {request.data}")  # Log the incoming data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Return user information after successful registration
            return Response({
                'id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
            
        print(f"Registration validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        summary="Get current user profile",
        description="Returns the authenticated user's profile information",
        responses={200: UserSerializer},
        tags=["User"]
    ),
    put=extend_schema(
        summary="Update user profile",
        description="Update the authenticated user's profile information",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: validation_error_response
        },
        tags=["User"]
    )
)

class UserDetailView(APIView):
    """Get authenticated user details or update user information"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Return the authenticated user's details"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update the authenticated user's information"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
