from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import logging

from .models import Document

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Document)
def auto_index_document(sender, instance, created, **kwargs):
    """
    Signal para auto-indexar documentos en ChromaDB cuando se crean o actualizan.
    """
    # Solo indexar si tiene contenido y no está indexado
    if instance.content and not instance.is_indexed:
        try:
            from apps.ai.services import RAGService
            
            rag = RAGService()
            
            # Preparar metadata
            metadata = instance.metadata.copy() if instance.metadata else {}
            metadata.update({
                'title': instance.title,
                'knowledge_base_id': str(instance.knowledge_base_id),
                'file_type': instance.file_type or 'text',
                'created_at': instance.created_at.isoformat() if instance.created_at else None,
            })
            
            # Indexar en ChromaDB
            rag.index_document(
                document_id=str(instance.id),
                content=instance.content,
                metadata=metadata
            )
            
            # Marcar como indexado
            Document.objects.filter(id=instance.id).update(
                is_indexed=True,
                indexed_at=timezone.now()
            )
            
            logger.info(f"Documento '{instance.title}' indexado exitosamente en ChromaDB")
            
        except Exception as e:
            logger.error(f"Error al indexar documento '{instance.title}': {e}")
