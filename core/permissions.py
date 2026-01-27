from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: solo el propietario puede editar.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permitir lectura a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escritura solo al propietario
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: solo admins pueden editar.
    """
    
    def has_permission(self, request, view):
        # Permitir lectura a todos autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escritura solo a admins
        return request.user and request.user.role == 'admin'


class IsAgentOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado: solo agentes o admins.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['agent', 'admin']
        )
