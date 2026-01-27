from django.urls import path
from .auth_views import (
    LoginView,
    RegisterView,
    LogoutView,
    RefreshTokenView,
    MeView,
    ChangePasswordView,
    VerifyTokenView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    # Autenticación JWT
    path('login/', LoginView.as_view(), name='auth-login'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('refresh/', RefreshTokenView.as_view(), name='auth-refresh'),
    path('verify/', VerifyTokenView.as_view(), name='auth-verify'),
    
    # Token JWT alternativo (usando TokenObtainPairView)
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    
    # Usuario autenticado
    path('me/', MeView.as_view(), name='auth-me'),
    path('change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
]
