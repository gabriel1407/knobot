from rest_framework import serializers
from .models import Document, KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    documents_count = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeBase
        fields = [
            'id', 'title', 'description', 'category', 
            'is_public', 'documents_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_documents_count(self, obj):
        return obj.documents.count()


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'knowledge_base', 'title', 'content', 'file',
            'file_type', 'file_url', 'metadata', 'is_indexed',
            'indexed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_type', 'is_indexed', 'indexed_at', 'created_at', 'updated_at']
    
    def validate_file(self, value):
        """Validar tipo de archivo."""
        if value:
            allowed_types = [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
                'application/msword',  # .doc
                'text/plain',
                'text/markdown',
            ]
            
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f"Tipo de archivo no soportado: {value.content_type}. "
                    f"Tipos permitidos: PDF, DOCX, DOC, TXT, MD"
                )
            
            # Limitar tamaño a 10MB
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El archivo es demasiado grande. Máximo 10MB."
                )
        
        return value


class DocumentUploadSerializer(serializers.Serializer):
    """Serializer para subir múltiples archivos."""
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )
    knowledge_base = serializers.PrimaryKeyRelatedField(
        queryset=KnowledgeBase.objects.all()
    )
    auto_index = serializers.BooleanField(default=True)
    category = serializers.CharField(required=False, allow_blank=True)
