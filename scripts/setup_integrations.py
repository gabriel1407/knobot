#!/usr/bin/env python
"""
Script para configurar integraciones de WhatsApp y Telegram.
Uso: docker-compose exec web python scripts/setup_integrations.py
"""

import os
import sys
import django

# Setup Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowbot.settings')
django.setup()

from apps.integrations.models import Integration


def setup_whatsapp():
    """Configura integración de WhatsApp."""
    print("\n=== Configuración de WhatsApp Business ===\n")
    
    phone_number_id = input("Phone Number ID: ").strip()
    access_token = input("Access Token: ").strip()
    verify_token = input("Verify Token (personalizado): ").strip()
    
    if not all([phone_number_id, access_token, verify_token]):
        print("❌ Todos los campos son requeridos")
        return
    
    integration, created = Integration.objects.update_or_create(
        type='whatsapp',
        defaults={
            'name': 'WhatsApp Business',
            'is_enabled': True,
            'config': {
                'phone_number_id': phone_number_id,
                'access_token': access_token,
                'verify_token': verify_token,
            }
        }
    )
    
    action = "creada" if created else "actualizada"
    print(f"\n✅ Integración de WhatsApp {action} exitosamente")
    print(f"\nWebhook URL: https://tu-dominio.com/api/integrations/webhooks/whatsapp/")
    print(f"Verify Token: {verify_token}")


def setup_telegram():
    """Configura integración de Telegram."""
    print("\n=== Configuración de Telegram Bot ===\n")
    
    bot_token = input("Bot Token (de @BotFather): ").strip()
    secret_token = input("Secret Token (opcional, para seguridad): ").strip() or None
    
    if not bot_token:
        print("❌ Bot Token es requerido")
        return
    
    integration, created = Integration.objects.update_or_create(
        type='telegram',
        defaults={
            'name': 'Telegram Bot',
            'is_enabled': True,
            'webhook_secret': secret_token,
            'config': {
                'bot_token': bot_token,
            }
        }
    )
    
    action = "creada" if created else "actualizada"
    print(f"\n✅ Integración de Telegram {action} exitosamente")
    print(f"\nWebhook URL: https://tu-dominio.com/api/integrations/webhooks/telegram/")
    if secret_token:
        print(f"Secret Token: {secret_token}")
    
    print("\n⚠️  Recuerda configurar el webhook usando:")
    print("docker-compose exec web python manage.py setup_telegram_webhook")


def list_integrations():
    """Lista todas las integraciones configuradas."""
    print("\n=== Integraciones Configuradas ===\n")
    
    integrations = Integration.objects.all()
    
    if not integrations:
        print("No hay integraciones configuradas")
        return
    
    for integration in integrations:
        status = "✅ Activa" if integration.is_enabled else "❌ Inactiva"
        print(f"\n{integration.name} ({integration.type})")
        print(f"  Estado: {status}")
        print(f"  ID: {integration.id}")
        print(f"  Creada: {integration.created_at.strftime('%Y-%m-%d %H:%M')}")


def main():
    """Menú principal."""
    while True:
        print("\n" + "="*50)
        print("CONFIGURACIÓN DE INTEGRACIONES")
        print("="*50)
        print("\n1. Configurar WhatsApp Business")
        print("2. Configurar Telegram Bot")
        print("3. Listar integraciones")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción: ").strip()
        
        if choice == '1':
            setup_whatsapp()
        elif choice == '2':
            setup_telegram()
        elif choice == '3':
            list_integrations()
        elif choice == '4':
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")


if __name__ == '__main__':
    main()
