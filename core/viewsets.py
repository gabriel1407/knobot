from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base reutilizable con funcionalidad común.
    
    Características:
    - Soporte para 2 serializers: list_serializer_class y write_serializer_class
    - Soft delete por defecto
    - Filtrado por is_active
    - Acciones bulk (bulk_delete, bulk_restore)
    """
    
    # Serializers
    list_serializer_class = None  # Para GET (detallado)
    write_serializer_class = None  # Para POST/PUT/PATCH
    
    # Configuración
    filter_active_by_default = True
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción.
        """
        # Para acciones de lectura, usar list_serializer
        if self.action in ['list', 'retrieve']:
            if self.list_serializer_class is not None:
                return self.list_serializer_class
        
        # Para acciones de escritura, usar write_serializer
        if self.action in ['create', 'update', 'partial_update']:
            if self.write_serializer_class is not None:
                return self.write_serializer_class
        
        # Fallback al serializer_class estándar
        return super().get_serializer_class()
    
    def get_queryset(self):
        """
        Filtra por is_active por defecto.
        """
        queryset = super().get_queryset()
        
        # Filtrar por is_active si está configurado
        if self.filter_active_by_default and hasattr(queryset.model, 'is_active'):
            # Permitir ver inactivos con parámetro ?show_inactive=true
            show_inactive = self.request.query_params.get('show_inactive', 'false')
            if show_inactive.lower() != 'true':
                queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def perform_destroy(self, instance):
        """
        Soft delete en lugar de eliminación física.
        """
        if hasattr(instance, 'soft_delete'):
            instance.soft_delete()
        else:
            instance.delete()
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """
        Elimina (soft delete) múltiples objetos.
        
        Body: {"ids": ["uuid1", "uuid2", ...]}
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'Se requiere una lista de IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.count()
        
        with transaction.atomic():
            for obj in queryset:
                if hasattr(obj, 'soft_delete'):
                    obj.soft_delete()
                else:
                    obj.delete()
        
        return Response({
            'message': f'{count} objetos eliminados',
            'count': count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_restore(self, request):
        """
        Restaura múltiples objetos eliminados (soft delete).
        
        Body: {"ids": ["uuid1", "uuid2", ...]}
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'Se requiere una lista de IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener objetos inactivos
        queryset = self.queryset.filter(id__in=ids, is_active=False)
        count = queryset.count()
        
        with transaction.atomic():
            for obj in queryset:
                if hasattr(obj, 'restore'):
                    obj.restore()
        
        return Response({
            'message': f'{count} objetos restaurados',
            'count': count
        })
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaura un objeto eliminado (soft delete).
        """
        obj = self.queryset.get(pk=pk)
        
        if hasattr(obj, 'restore'):
            obj.restore()
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Este objeto no soporta restauración'},
            status=status.HTTP_400_BAD_REQUEST
        )
