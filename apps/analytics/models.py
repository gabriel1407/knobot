from django.db import models
from django.conf import settings
from core.models import BaseModel


class Analytics(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics',
        null=True,
        blank=True
    )
    event_type = models.CharField(max_length=100)
    event_data = models.JSONField(default=dict)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'analytics'
        verbose_name = 'Analítica'
        verbose_name_plural = 'Analíticas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
