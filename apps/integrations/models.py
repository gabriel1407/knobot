from django.db import models
from core.models import BaseModel


class Integration(BaseModel):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=[
            ('billing', 'Sistema de Facturación'),
            ('crm', 'CRM'),
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('webhook', 'Webhook'),
        ]
    )
    config = models.JSONField(default=dict)
    is_enabled = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'integrations'
        verbose_name = 'Integración'
        verbose_name_plural = 'Integraciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.type})"
