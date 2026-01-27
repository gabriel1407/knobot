from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.viewsets import BaseModelViewSet
from core.permissions import IsAdminOrReadOnly
from .models import User
from .serializers import UserListSerializer, UserWriteSerializer, UserProfileSerializer


class UserViewSet(BaseModelViewSet):
    """
    ViewSet para gestión de usuarios.
    
    Endpoints:
    - GET /users/ - Listar usuarios
    - POST /users/ - Crear usuario
    - GET /users/{id}/ - Ver detalle de usuario
    - PUT /users/{id}/ - Actualizar usuario
    - PATCH /users/{id}/ - Actualizar parcialmente usuario
    - DELETE /users/{id}/ - Eliminar usuario (soft delete)
    - POST /users/{id}/restore/ - Restaurar usuario
    - GET /users/me/ - Ver perfil del usuario autenticado
    - PUT /users/me/ - Actualizar perfil del usuario autenticado
    """
    
    queryset = User.objects.all()
    list_serializer_class = UserListSerializer
    write_serializer_class = UserWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    filterset_fields = ['role', 'is_active', 'company']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username', 'email']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Permisos personalizados por acción.
        """
        if self.action == 'create':
            # Permitir registro público
            return [AllowAny()]
        elif self.action in ['me', 'update_profile']:
            # Solo usuarios autenticados
            return [IsAuthenticated()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        Ver o actualizar el perfil del usuario autenticado.
        
        GET /users/me/ - Ver perfil
        PUT /users/me/ - Actualizar perfil completo
        PATCH /users/me/ - Actualizar perfil parcialmente
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = UserProfileSerializer(
                user,
                data=request.data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Cambiar contraseña del usuario autenticado.
        
        Body: {
            "old_password": "...",
            "new_password": "...",
            "new_password_confirm": "..."
        }
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        # Validaciones
        if not old_password or not new_password:
            return Response(
                {'error': 'Se requieren old_password y new_password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != new_password_confirm:
            return Response(
                {'error': 'Las contraseñas nuevas no coinciden'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Contraseña actual incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cambiar contraseña
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Contraseña actualizada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Desactivar un usuario (solo admins).
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activar un usuario (solo admins).
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
