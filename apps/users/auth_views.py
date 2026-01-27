from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .auth_serializers import (
    CustomTokenObtainPairSerializer,
    LoginSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)
from .serializers import UserProfileSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT.
    Incluye información del usuario en la respuesta.
    """
    serializer_class = CustomTokenObtainPairSerializer


class LoginView(APIView):
    """
    Vista para login con username/email y password.
    Retorna tokens JWT y información del usuario.
    
    POST /auth/login/
    Body: {
        "username": "user@example.com",  // o username
        "password": "password123"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        # Agregar claims personalizados
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['role'] = user.role
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'company': user.company,
            }
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Vista para registro de nuevos usuarios.
    Retorna tokens JWT y información del usuario.
    
    POST /auth/register/
    Body: {
        "username": "newuser",
        "email": "user@example.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        # Agregar claims personalizados
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['role'] = user.role
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    Vista para logout.
    Blacklistea el refresh token para invalidarlo.
    
    POST /auth/logout/
    Body: {
        "refresh": "refresh_token_here"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response(
                    {'error': 'Se requiere el refresh token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Logout exitoso'
            }, status=status.HTTP_200_OK)
        
        except TokenError:
            return Response(
                {'error': 'Token inválido o expirado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenView(TokenRefreshView):
    """
    Vista para refrescar el access token usando el refresh token.
    
    POST /auth/refresh/
    Body: {
        "refresh": "refresh_token_here"
    }
    """
    pass


class MeView(APIView):
    """
    Vista para obtener información del usuario autenticado.
    
    GET /auth/me/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    """
    Vista para cambiar contraseña del usuario autenticado.
    
    POST /auth/change-password/
    Body: {
        "old_password": "current_password",
        "new_password": "new_password",
        "new_password_confirm": "new_password"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña actualizada exitosamente'
        }, status=status.HTTP_200_OK)


class VerifyTokenView(APIView):
    """
    Vista para verificar si un token es válido.
    
    POST /auth/verify/
    Body: {
        "token": "access_token_here"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Se requiere el token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Intentar decodificar el token
            from rest_framework_simplejwt.tokens import AccessToken
            AccessToken(token)
            
            return Response({
                'valid': True,
                'message': 'Token válido'
            }, status=status.HTTP_200_OK)
        
        except (TokenError, InvalidToken):
            return Response({
                'valid': False,
                'message': 'Token inválido o expirado'
            }, status=status.HTTP_401_UNAUTHORIZED)
