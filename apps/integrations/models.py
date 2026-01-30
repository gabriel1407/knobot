from django.db import models
from core.models import BaseModel


class Integration(BaseModel):
    INTEGRATION_TYPES = [
        ('whatsapp', 'WhatsApp Business'),
        ('telegram', 'Telegram Bot'),
        ('email', 'Email'),
        ('slack', 'Slack'),
        ('api', 'API'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=INTEGRATION_TYPES)
    config = models.JSONField(
        default=dict,
        help_text='Configuración específica de la integración (tokens, webhooks, etc.)'
    )
    is_enabled = models.BooleanField(default=True)
    webhook_url = models.URLField(max_length=500, blank=True, null=True)
    webhook_secret = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'integrations'
        verbose_name = 'Integración'
        verbose_name_plural = 'Integraciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class WebhookLog(BaseModel):
    """
    Log de webhooks recibidos para debugging y auditoría.
    """
    integration = models.ForeignKey(
        Integration,
        on_delete=models.CASCADE,
        related_name='webhook_logs'
    )
    platform = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    response_status = models.IntegerField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'webhook_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['platform', 'event_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.platform} - {self.event_type} - {self.created_at}"
