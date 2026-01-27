from django.db import models
from django.conf import settings
from core.models import BaseModel


class KnowledgeBase(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='knowledge_bases'
    )

    class Meta:
        db_table = 'knowledge_bases'
        verbose_name = 'Base de Conocimiento'
        verbose_name_plural = 'Bases de Conocimiento'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Document(BaseModel):
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    file_url = models.URLField(blank=True, null=True)
    embedding = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'documents'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
