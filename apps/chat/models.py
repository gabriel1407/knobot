from django.db import models
from django.conf import settings
from core.models import BaseModel


class Conversation(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Activa'),
            ('resolved', 'Resuelta'),
            ('pending', 'Pendiente'),
        ],
        default='active'
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversación {self.id} - {self.user.username}"


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'Usuario'),
            ('assistant', 'Asistente'),
            ('system', 'Sistema'),
        ]
    )
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    tokens_used = models.IntegerField(default=0)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
