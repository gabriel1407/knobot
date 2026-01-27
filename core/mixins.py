from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class SoftDeleteMixin:
    """
    Mixin para soft delete en ViewSets.
    """
    
    def perform_destroy(self, instance):
        """
        Soft delete en lugar de eliminación física.
        """
        if hasattr(instance, 'soft_delete'):
            instance.soft_delete()
        else:
            instance.delete()
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaura un objeto eliminado.
        """
        obj = self.get_queryset().get(pk=pk)
        
        if hasattr(obj, 'restore'):
            obj.restore()
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Este objeto no soporta restauración'},
            status=status.HTTP_400_BAD_REQUEST
        )


class BulkActionsMixin:
    """
    Mixin para acciones en bulk (múltiples objetos).
    """
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """
        Elimina múltiples objetos.
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'Se requiere una lista de IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.count()
        
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
        Restaura múltiples objetos.
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'Se requiere una lista de IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(id__in=ids, is_active=False)
        count = queryset.count()
        
        for obj in queryset:
            if hasattr(obj, 'restore'):
                obj.restore()
        
        return Response({
            'message': f'{count} objetos restaurados',
            'count': count
        })
