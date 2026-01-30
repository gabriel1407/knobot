# API REST - Fase 3: Integraciones WhatsApp y Telegram

## ✅ Implementación Completada

### **Arquitectura de Integraciones**

En lugar de crear endpoints de chat propios, KnoBot se integra directamente con **WhatsApp Business API** y **Telegram Bot API** para que los usuarios interactúen a través de estos canales populares.

### **Componentes Implementados**

1. **Modelos Actualizados** (`apps/integrations/models.py`)
   - `Integration` - Configuración de integraciones
   - `WebhookLog` - Auditoría de webhooks recibidos

2. **Servicios de Integración** (`apps/integrations/services/`)
   - `WhatsAppService` - Cliente para WhatsApp Business API
   - `TelegramService` - Cliente para Telegram Bot API
   - `MessageHandler` - Procesador centralizado con RAG

3. **Webhooks** (`apps/integrations/views.py`)
   - `WhatsAppWebhookView` - Recibe mensajes de WhatsApp
   - `TelegramWebhookView` - Recibe mensajes de Telegram

---

## 🏗️ Arquitectura del Flujo

```
Usuario (WhatsApp/Telegram)
    ↓
Mensaje enviado
    ↓
Webhook recibido en KnoBot
    ↓
MessageHandler procesa mensaje
    ↓
ChatOrchestrator + RAG
    ↓
Respuesta generada con contexto
    ↓
Enviada por WhatsApp/Telegram
    ↓
Usuario recibe respuesta
```

---

## 📋 Endpoints de Webhooks

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/api/integrations/webhooks/whatsapp/` | Verificación webhook WhatsApp | Token |
| POST | `/api/integrations/webhooks/whatsapp/` | Recibir mensajes WhatsApp | Token |
| POST | `/api/integrations/webhooks/telegram/` | Recibir mensajes Telegram | Secret Token |

---

## 🔧 Configuración de WhatsApp Business

### **1. Crear App en Meta for Developers**

1. Ir a https://developers.facebook.com/
2. Crear una nueva app
3. Agregar producto "WhatsApp"
4. Obtener:
   - `phone_number_id` - ID del número de teléfono
   - `access_token` - Token de acceso
   - `verify_token` - Token de verificación (crear uno personalizado)

### **2. Configurar en KnoBot**

```python
# En Django Admin o via API
from apps.integrations.models import Integration

integration = Integration.objects.create(
    name='WhatsApp Business',
    type='whatsapp',
    is_enabled=True,
    config={
        'phone_number_id': 'TU_PHONE_NUMBER_ID',
        'access_token': 'TU_ACCESS_TOKEN',
        'verify_token': 'TU_VERIFY_TOKEN_PERSONALIZADO'
    }
)
```

### **3. Configurar Webhook en Meta**

1. En la consola de Meta, ir a WhatsApp > Configuration
2. Configurar webhook:
   - **URL:** `https://tu-dominio.com/api/integrations/webhooks/whatsapp/`
   - **Verify Token:** El mismo que configuraste en KnoBot
3. Suscribirse a eventos: `messages`

### **4. Probar Integración**

```bash
# Enviar mensaje de prueba desde WhatsApp al número configurado
# El bot responderá automáticamente usando RAG
```

---

## 🤖 Configuración de Telegram Bot

### **1. Crear Bot con BotFather**

1. Abrir Telegram y buscar `@BotFather`
2. Enviar `/newbot`
3. Seguir instrucciones para crear el bot
4. Obtener el `bot_token`

### **2. Configurar en KnoBot**

```python
# En Django Admin o via API
from apps.integrations.models import Integration

integration = Integration.objects.create(
    name='Telegram Bot',
    type='telegram',
    is_enabled=True,
    webhook_secret='TU_SECRET_TOKEN_PERSONALIZADO',  # Opcional pero recomendado
    config={
        'bot_token': 'TU_BOT_TOKEN'
    }
)
```

### **3. Configurar Webhook**

```python
# Usando el servicio de Telegram
from apps.integrations.services import TelegramService

service = TelegramService('TU_BOT_TOKEN')

# Configurar webhook
await service.set_webhook(
    webhook_url='https://tu-dominio.com/api/integrations/webhooks/telegram/',
    secret_token='TU_SECRET_TOKEN_PERSONALIZADO'
)

# Verificar webhook
info = await service.get_webhook_info()
print(info)
```

### **4. Probar Integración**

```bash
# Buscar tu bot en Telegram
# Enviar /start o cualquier mensaje
# El bot responderá automáticamente usando RAG
```

---

## 💬 Flujo de Mensajes

### **WhatsApp**

1. Usuario envía mensaje por WhatsApp
2. Meta envía webhook a KnoBot
3. `WhatsAppWebhookView` recibe el mensaje
4. `MessageHandler.handle_whatsapp_message()`:
   - Obtiene o crea usuario desde número de teléfono
   - Obtiene o crea conversación
   - Marca mensaje como leído
   - Procesa con `ChatOrchestrator` + RAG
   - Envía respuesta por WhatsApp

### **Telegram**

1. Usuario envía mensaje por Telegram
2. Telegram envía webhook a KnoBot
3. `TelegramWebhookView` recibe el mensaje
4. `MessageHandler.handle_telegram_message()`:
   - Obtiene o crea usuario desde chat_id
   - Obtiene o crea conversación
   - Envía acción "escribiendo..."
   - Procesa con `ChatOrchestrator` + RAG
   - Envía respuesta por Telegram

---

## 🔐 Seguridad

### **WhatsApp**

- Verificación de webhook con `verify_token`
- Validación de firma de Meta (opcional, recomendado para producción)
- HTTPS requerido

### **Telegram**

- Secret token en header `X-Telegram-Bot-Api-Secret-Token`
- Validación de origen
- HTTPS requerido

### **Logs de Auditoría**

Todos los webhooks se registran en `WebhookLog`:
- Payload recibido
- Respuesta enviada
- Errores (si los hay)
- Timestamp de procesamiento

```python
# Ver logs
from apps.integrations.models import WebhookLog

logs = WebhookLog.objects.filter(platform='whatsapp').order_by('-created_at')[:10]
for log in logs:
    print(f"{log.created_at}: {log.event_type} - Status: {log.response_status}")
```

---

## 📱 Servicios Disponibles

### **WhatsAppService**

```python
from apps.integrations.services import WhatsAppService

service = WhatsAppService(phone_number_id, access_token)

# Enviar mensaje de texto
await service.send_message(
    to='573001234567',
    message='Hola, ¿en qué puedo ayudarte?'
)

# Enviar mensaje con plantilla
await service.send_template_message(
    to='573001234567',
    template_name='bienvenida',
    language_code='es'
)

# Marcar como leído
await service.mark_as_read(message_id)
```

### **TelegramService**

```python
from apps.integrations.services import TelegramService

service = TelegramService(bot_token)

# Enviar mensaje
await service.send_message(
    chat_id='123456789',
    text='Hola, ¿en qué puedo ayudarte?',
    parse_mode='Markdown'
)

# Enviar acción de escribiendo
await service.send_typing_action(chat_id='123456789')

# Teclado inline
keyboard = TelegramService.create_inline_keyboard([
    [{"text": "Opción 1", "callback_data": "opt1"}],
    [{"text": "Opción 2", "callback_data": "opt2"}]
])

await service.send_message(
    chat_id='123456789',
    text='Elige una opción:',
    reply_markup=keyboard
)
```

---

## 🎯 Características del MessageHandler

### **Gestión Automática de Usuarios**

- Crea usuarios automáticamente desde WhatsApp/Telegram
- Username formato: `whatsapp_573001234567` o `telegram_username`
- Email temporal: `{username}@knowbot.local`
- Rol: `customer` por defecto

### **Gestión de Conversaciones**

- Una conversación activa por usuario y plataforma
- Metadata incluye:
  - `platform`: 'whatsapp' o 'telegram'
  - `platform_user_id`: Número de teléfono o chat_id
  - `created_via`: Canal de origen

### **Integración con RAG**

- Usa `ChatOrchestrator` para procesar mensajes
- RAG activado por defecto
- 5 documentos de contexto por defecto
- Respuestas personalizadas según la base de conocimiento

---

## 🧪 Testing Local

### **Usar ngrok para Webhooks**

```bash
# Instalar ngrok
# https://ngrok.com/

# Exponer puerto 9000
ngrok http 9000

# Usar la URL de ngrok en la configuración de webhooks
# Ejemplo: https://abc123.ngrok.io/api/integrations/webhooks/whatsapp/
```

### **Probar WhatsApp**

1. Configurar webhook con URL de ngrok
2. Enviar mensaje desde WhatsApp Sandbox (Meta)
3. Ver logs en Django:
```bash
docker-compose logs -f web
```

### **Probar Telegram**

1. Configurar webhook:
```python
from apps.integrations.services import TelegramService
service = TelegramService('TU_BOT_TOKEN')
await service.set_webhook('https://abc123.ngrok.io/api/integrations/webhooks/telegram/')
```

2. Enviar mensaje al bot
3. Ver logs en Django

---

## 📊 Monitoreo

### **Ver Logs de Webhooks**

```python
from apps.integrations.models import WebhookLog

# Últimos 10 webhooks de WhatsApp
logs = WebhookLog.objects.filter(
    platform='whatsapp'
).order_by('-created_at')[:10]

for log in logs:
    print(f"""
    ID: {log.id}
    Evento: {log.event_type}
    Status: {log.response_status}
    Error: {log.error_message or 'None'}
    Procesado: {log.processed_at}
    """)
```

### **Estadísticas**

```python
from django.db.models import Count
from apps.integrations.models import WebhookLog

# Mensajes por plataforma
stats = WebhookLog.objects.values('platform').annotate(
    total=Count('id')
)

for stat in stats:
    print(f"{stat['platform']}: {stat['total']} mensajes")
```

---

## 🚀 Despliegue en Producción

### **Requisitos**

1. **Dominio con HTTPS**
   - WhatsApp y Telegram requieren HTTPS
   - Usar certificado SSL válido

2. **Variables de Entorno**

```env
# .env
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_ACCESS_TOKEN=tu_access_token
WHATSAPP_VERIFY_TOKEN=tu_verify_token

TELEGRAM_BOT_TOKEN=tu_bot_token
TELEGRAM_SECRET_TOKEN=tu_secret_token
```

3. **Configurar Integraciones**

```python
# Script de configuración
from apps.integrations.models import Integration
import os

# WhatsApp
Integration.objects.get_or_create(
    type='whatsapp',
    defaults={
        'name': 'WhatsApp Business',
        'is_enabled': True,
        'config': {
            'phone_number_id': os.getenv('WHATSAPP_PHONE_NUMBER_ID'),
            'access_token': os.getenv('WHATSAPP_ACCESS_TOKEN'),
            'verify_token': os.getenv('WHATSAPP_VERIFY_TOKEN'),
        }
    }
)

# Telegram
Integration.objects.get_or_create(
    type='telegram',
    defaults={
        'name': 'Telegram Bot',
        'is_enabled': True,
        'webhook_secret': os.getenv('TELEGRAM_SECRET_TOKEN'),
        'config': {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        }
    }
)
```

---

## 📝 Próximas Mejoras

### **Fase 4: Funcionalidades Avanzadas**

- [ ] Soporte para mensajes multimedia (imágenes, audio, documentos)
- [ ] Botones interactivos en Telegram
- [ ] Plantillas de WhatsApp personalizadas
- [ ] Métricas y analytics de conversaciones
- [ ] Transferencia a agente humano
- [ ] Horarios de atención
- [ ] Respuestas automáticas fuera de horario
- [ ] Multi-idioma

---

## 🔗 Referencias

- **WhatsApp Business API:** https://developers.facebook.com/docs/whatsapp/cloud-api
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Webhooks Best Practices:** https://developers.facebook.com/docs/graph-api/webhooks

---

**Última actualización:** 27 de enero de 2026  
**Estado:** Fase 3 Completada ✅  
**Chat:** WhatsApp + Telegram con RAG integrado
