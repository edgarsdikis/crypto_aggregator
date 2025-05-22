from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailView

urlpatterns = [
    # Registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoint
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
