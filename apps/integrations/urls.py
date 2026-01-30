from django.urls import path
from .views import WhatsAppWebhookView, TelegramWebhookView

urlpatterns = [
    path('webhooks/whatsapp/', WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
    path('webhooks/telegram/', TelegramWebhookView.as_view(), name='telegram-webhook'),
]
