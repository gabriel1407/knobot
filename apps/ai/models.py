from django.db import models
from core.models import BaseModel


class AIModel(BaseModel):
    name = models.CharField(max_length=100)
    provider = models.CharField(
        max_length=50,
        choices=[
            ('gemini', 'Google Gemini'),
            ('openai', 'OpenAI'),
            ('anthropic', 'Anthropic'),
        ]
    )
    model_id = models.CharField(max_length=100)
    config = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)
    max_tokens = models.IntegerField(default=2048)
    temperature = models.FloatField(default=0.7)

    class Meta:
        db_table = 'ai_models'
        verbose_name = 'Modelo de IA'
        verbose_name_plural = 'Modelos de IA'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.provider})"
