from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
import logging

from .models import Document, KnowledgeBase
from .serializers import DocumentSerializer, KnowledgeBaseSerializer, DocumentUploadSerializer
from .utils import extract_text_from_file, get_file_type

logger = logging.getLogger(__name__)


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar bases de conocimiento."""
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar documentos."""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """Filtrar por knowledge_base si se proporciona."""
        queryset = Document.objects.all()
        kb_id = self.request.query_params.get('knowledge_base', None)
        if kb_id:
            queryset = queryset.filter(knowledge_base_id=kb_id)
        return queryset
    
    def perform_create(self, serializer):
        """Procesar archivo al crear documento."""
        file = self.request.FILES.get('file')
        
        if file:
            # Extraer texto del archivo
            content = extract_text_from_file(file)
            file_type = get_file_type(file)
            
            if content:
                serializer.save(
                    content=content,
                    file_type=file_type
                )
            else:
                # Si no se pudo extraer texto, guardar sin contenido
                serializer.save(file_type=file_type)
                logger.warning(f"No se pudo extraer texto del archivo: {file.name}")
        else:
            serializer.save()
    
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_documents(self, request):
        """
        Endpoint para subir múltiples archivos.
        
        POST /api/knowledge/documents/upload/
        
        Body (multipart/form-data):
        - files: Lista de archivos
        - knowledge_base: ID de la base de conocimiento
        - auto_index: Boolean (default: true)
        - category: String (opcional)
        """
        serializer = DocumentUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        files = request.FILES.getlist('files')
        knowledge_base = serializer.validated_data['knowledge_base']
        auto_index = serializer.validated_data.get('auto_index', True)
        category = serializer.validated_data.get('category', '')
        
        created_documents = []
        errors = []
        
        for file in files:
            try:
                # Extraer texto
                content = extract_text_from_file(file)
                file_type = get_file_type(file)
                
                if not content:
                    errors.append({
                        'file': file.name,
                        'error': 'No se pudo extraer texto del archivo'
                    })
                    continue
                
                # Crear documento
                doc = Document.objects.create(
                    knowledge_base=knowledge_base,
                    title=file.name,
                    content=content,
                    file=file,
                    file_type=file_type,
                    metadata={'category': category} if category else {}
                )
                
                created_documents.append({
                    'id': str(doc.id),
                    'title': doc.title,
                    'file_type': doc.file_type,
                    'is_indexed': doc.is_indexed
                })
                
                logger.info(f"Documento '{file.name}' creado exitosamente")
                
            except Exception as e:
                errors.append({
                    'file': file.name,
                    'error': str(e)
                })
                logger.error(f"Error procesando archivo '{file.name}': {e}")
        
        return Response({
            'success': True,
            'created': len(created_documents),
            'documents': created_documents,
            'errors': errors
        }, status=status.HTTP_201_CREATED if created_documents else status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='reindex')
    def reindex(self, request, pk=None):
        """
        Re-indexar un documento en ChromaDB.
        
        POST /api/knowledge/documents/{id}/reindex/
        """
        document = self.get_object()
        
        try:
            from apps.ai.services import RAGService
            
            rag = RAGService()
            
            # Preparar metadata
            metadata = document.metadata.copy() if document.metadata else {}
            metadata.update({
                'title': document.title,
                'knowledge_base_id': str(document.knowledge_base_id),
                'file_type': document.file_type or 'text',
            })
            
            # Re-indexar
            rag.index_document(
                document_id=str(document.id),
                content=document.content,
                metadata=metadata
            )
            
            # Actualizar estado
            document.is_indexed = True
            document.indexed_at = timezone.now()
            document.save()
            
            return Response({
                'success': True,
                'message': f"Documento '{document.title}' re-indexado exitosamente"
            })
            
        except Exception as e:
            logger.error(f"Error re-indexando documento: {e}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
