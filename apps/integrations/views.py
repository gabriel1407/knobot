from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import asyncio
import json
from .models import Integration, WebhookLog
from .services import WhatsAppService, TelegramService
from .services.message_handler import MessageHandler


@method_decorator(csrf_exempt, name='dispatch')
class WhatsAppWebhookView(APIView):
    """
    Webhook para recibir mensajes de WhatsApp Business API.
    
    GET: Verificación del webhook
    POST: Recepción de mensajes
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Verificación del webhook de WhatsApp.
        """
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        # Obtener verify_token de la integración
        try:
            integration = Integration.objects.filter(
                type='whatsapp',
                is_enabled=True
            ).first()
            
            if not integration:
                return Response(
                    {'error': 'Integración de WhatsApp no configurada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            verify_token = integration.config.get('verify_token')
            
            if mode == 'subscribe' and token == verify_token:
                return Response(int(challenge), status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Token de verificación inválido'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """
        Recepción de mensajes de WhatsApp.
        """
        payload = request.data
        
        # Obtener integración de WhatsApp
        try:
            integration = Integration.objects.filter(
                type='whatsapp',
                is_enabled=True
            ).first()
            
            if not integration:
                return Response(
                    {'error': 'Integración de WhatsApp no configurada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Log del webhook
            webhook_log = WebhookLog.objects.create(
                integration=integration,
                platform='whatsapp',
                event_type='message',
                payload=payload
            )
            
            # Parsear mensaje
            message_data = WhatsAppService.parse_webhook_message(payload)
            
            if not message_data:
                webhook_log.error_message = 'No se pudo parsear el mensaje'
                webhook_log.save()
                return Response({'status': 'ignored'}, status=status.HTTP_200_OK)
            
            # Procesar mensaje de forma asíncrona
            phone_number_id = integration.config.get('phone_number_id')
            access_token = integration.config.get('access_token')
            
            whatsapp_service = WhatsAppService(phone_number_id, access_token)
            message_handler = MessageHandler()
            
            # Ejecutar procesamiento asíncrono
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    message_handler.handle_whatsapp_message(
                        message_data,
                        whatsapp_service
                    )
                )
                
                webhook_log.response_status = 200
                webhook_log.response_data = result
                webhook_log.processed_at = timezone.now()
                webhook_log.save()
                
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            
            except Exception as e:
                webhook_log.error_message = str(e)
                webhook_log.response_status = 500
                webhook_log.save()
                
                return Response(
                    {'status': 'error', 'message': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                loop.close()
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(APIView):
    """
    Webhook para recibir mensajes de Telegram Bot API.
    
    POST: Recepción de mensajes
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Recepción de mensajes de Telegram.
        """
        payload = request.data
        
        # Verificar secret token si está configurado
        secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        
        try:
            integration = Integration.objects.filter(
                type='telegram',
                is_enabled=True
            ).first()
            
            if not integration:
                return Response(
                    {'error': 'Integración de Telegram no configurada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar secret token
            expected_secret = integration.webhook_secret
            if expected_secret and secret_token != expected_secret:
                return Response(
                    {'error': 'Secret token inválido'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Log del webhook
            webhook_log = WebhookLog.objects.create(
                integration=integration,
                platform='telegram',
                event_type='message',
                payload=payload
            )
            
            # Parsear mensaje
            message_data = TelegramService.parse_webhook_message(payload)
            
            if not message_data:
                webhook_log.error_message = 'No se pudo parsear el mensaje'
                webhook_log.save()
                return Response({'ok': True}, status=status.HTTP_200_OK)
            
            # Procesar mensaje de forma asíncrona
            bot_token = integration.config.get('bot_token')
            
            telegram_service = TelegramService(bot_token)
            message_handler = MessageHandler()
            
            # Ejecutar procesamiento asíncrono
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    message_handler.handle_telegram_message(
                        message_data,
                        telegram_service
                    )
                )
                
                webhook_log.response_status = 200
                webhook_log.response_data = result
                webhook_log.processed_at = timezone.now()
                webhook_log.save()
                
                return Response({'ok': True}, status=status.HTTP_200_OK)
            
            except Exception as e:
                webhook_log.error_message = str(e)
                webhook_log.response_status = 500
                webhook_log.save()
                
                return Response(
                    {'ok': False, 'description': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                loop.close()
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
