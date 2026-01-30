from django.core.management.base import BaseCommand
from apps.integrations.models import Integration
from apps.integrations.services import TelegramService
import asyncio


class Command(BaseCommand):
    help = 'Configura el webhook de Telegram'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='URL del webhook (ej: https://tu-dominio.com/api/integrations/webhooks/telegram/)'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Eliminar webhook'
        )
        parser.add_argument(
            '--info',
            action='store_true',
            help='Ver información del webhook'
        )

    def handle(self, *args, **options):
        try:
            integration = Integration.objects.filter(
                type='telegram',
                is_enabled=True
            ).first()
            
            if not integration:
                self.stdout.write(self.style.ERROR(
                    'No hay integración de Telegram configurada'
                ))
                return
            
            bot_token = integration.config.get('bot_token')
            service = TelegramService(bot_token)
            
            if options['delete']:
                # Eliminar webhook
                result = asyncio.run(service.delete_webhook())
                if result.get('ok'):
                    self.stdout.write(self.style.SUCCESS(
                        '✅ Webhook eliminado exitosamente'
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'❌ Error: {result}'
                    ))
            
            elif options['info']:
                # Ver información del webhook
                result = asyncio.run(service.get_webhook_info())
                if result.get('ok'):
                    info = result.get('result', {})
                    self.stdout.write(self.style.SUCCESS(
                        '\n=== Información del Webhook ===\n'
                    ))
                    self.stdout.write(f"URL: {info.get('url', 'No configurado')}")
                    self.stdout.write(f"Pending updates: {info.get('pending_update_count', 0)}")
                    self.stdout.write(f"Max connections: {info.get('max_connections', 0)}")
                    if info.get('last_error_message'):
                        self.stdout.write(self.style.WARNING(
                            f"Último error: {info.get('last_error_message')}"
                        ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'❌ Error: {result}'
                    ))
            
            else:
                # Configurar webhook
                webhook_url = options.get('url')
                
                if not webhook_url:
                    self.stdout.write(self.style.ERROR(
                        'Debes proporcionar la URL del webhook con --url'
                    ))
                    return
                
                secret_token = integration.webhook_secret
                result = asyncio.run(service.set_webhook(webhook_url, secret_token))
                
                if result.get('ok'):
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Webhook configurado exitosamente: {webhook_url}'
                    ))
                    if secret_token:
                        self.stdout.write(f'Secret Token: {secret_token}')
                else:
                    self.stdout.write(self.style.ERROR(
                        f'❌ Error: {result}'
                    ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'❌ Error: {str(e)}'
            ))
