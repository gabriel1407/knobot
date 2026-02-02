# 🤖 Lógica de Integraciones - WhatsApp y Telegram

## 📋 Resumen

La lógica completa ya está implementada en tu sistema. Aquí te explico cómo funciona cada componente:

---

## 🏗️ Arquitectura del Sistema

```
Usuario (WhatsApp/Telegram)
    ↓
Webhook recibe mensaje
    ↓
WhatsAppWebhookView / TelegramWebhookView
    ↓
MessageHandler procesa mensaje
    ↓
ChatOrchestrator (RAG + Gemini)
    ↓
Respuesta enviada al usuario
```

---

## 📱 1. WhatsApp Business API

### **Archivo:** `apps/integrations/views.py`

#### **Verificación del Webhook (GET):**
```python
# Meta envía GET request para verificar el webhook
def get(self, request):
    mode = request.GET.get('hub.mode')
    token = request.GET.get('hub.verify_token')
    challenge = request.GET.get('hub.challenge')
    
    # Verifica que el token coincida
    if mode == 'subscribe' and token == integration.config['verify_token']:
        return HttpResponse(challenge)
```

#### **Recepción de Mensajes (POST):**
```python
async def post(self, request):
    # 1. Recibe webhook de WhatsApp
    data = request.data
    
    # 2. Extrae información del mensaje
    entry = data['entry'][0]
    changes = entry['changes'][0]
    value = changes['value']
    
    # 3. Obtiene mensaje y remitente
    message = value['messages'][0]
    from_number = message['from']
    text = message['text']['body']
    
    # 4. Procesa con MessageHandler
    handler = MessageHandler(integration)
    await handler.handle_message(from_number, text, 'whatsapp')
```

### **Envío de Respuestas:**

**Archivo:** `apps/integrations/services/whatsapp_service.py`

```python
async def send_message(self, to: str, message: str):
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Envía con httpx (async)
    response = await client.post(url, json=payload, headers=headers)
```

---

## 🤖 2. Telegram Bot API

### **Archivo:** `apps/integrations/views.py`

#### **Recepción de Mensajes (POST):**
```python
async def post(self, request):
    # 1. Recibe webhook de Telegram
    data = request.data
    
    # 2. Verifica secret token (opcional)
    secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    
    # 3. Extrae mensaje
    message = data.get('message', {})
    chat_id = message['chat']['id']
    text = message.get('text', '')
    
    # 4. Procesa con MessageHandler
    handler = MessageHandler(integration)
    await handler.handle_message(str(chat_id), text, 'telegram')
```

### **Envío de Respuestas:**

**Archivo:** `apps/integrations/services/telegram_service.py`

```python
async def send_message(self, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    # Envía con httpx (async)
    response = await client.post(url, json=payload)
```

---

## 🧠 3. MessageHandler (Lógica Central)

### **Archivo:** `apps/integrations/services/message_handler.py`

Este es el corazón del sistema que procesa todos los mensajes:

```python
async def handle_message(self, user_id: str, message: str, platform: str):
    # 1. Obtener o crear usuario
    user = await self._get_or_create_user(user_id, platform)
    
    # 2. Obtener o crear conversación
    conversation = await self._get_or_create_conversation(user)
    
    # 3. Guardar mensaje del usuario
    await self._save_message(conversation, message, 'user')
    
    # 4. Generar respuesta con RAG + Gemini
    response = await self._generate_response(message, conversation.id)
    
    # 5. Guardar respuesta del bot
    await self._save_message(conversation, response, 'assistant')
    
    # 6. Enviar respuesta al usuario
    await self._send_response(user_id, response, platform)
```

### **Generación de Respuesta con RAG:**

```python
async def _generate_response(self, message: str, conversation_id: int):
    if AI_AVAILABLE:
        # Usa RAG completo
        orchestrator = ChatOrchestrator()
        response = await orchestrator.process_message(
            message=message,
            conversation_id=conversation_id,
            use_rag=True,
            n_results=5
        )
    else:
        # Fallback a Gemini directo
        response = await self._generate_response_with_gemini_only(message)
    
    return response
```

---

## 🎯 4. ChatOrchestrator (RAG + Gemini)

### **Archivo:** `apps/ai/services/chat_orchestrator.py`

```python
async def process_message(self, message: str, conversation_id: int, use_rag: bool = True):
    # 1. Si RAG está habilitado, buscar contexto
    if use_rag:
        context_docs = self.rag_service.retrieve_context(message, n_results=5)
        context = "\n".join([doc['content'] for doc in context_docs])
    else:
        context = ""
    
    # 2. Construir prompt con contexto
    prompt = self._build_prompt(message, context, conversation_id)
    
    # 3. Generar respuesta con Gemini
    response = await self._generate_with_gemini(prompt)
    
    return response
```

### **Construcción del Prompt:**

```python
def _build_prompt(self, message: str, context: str, conversation_id: int):
    # Obtener historial de conversación
    history = self._get_conversation_history(conversation_id)
    
    prompt = f"""Eres un asistente virtual de soporte técnico para un ISP.

Contexto relevante de la base de conocimiento:
{context}

Historial de conversación:
{history}

Usuario: {message}

Asistente:"""
    
    return prompt
```

---

## 🗄️ 5. Modelos de Base de Datos

### **Integration:**
```python
class Integration(BaseModel):
    type = models.CharField(max_length=50)  # 'whatsapp' o 'telegram'
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)
    config = models.JSONField()  # Tokens, IDs, etc.
    webhook_secret = models.CharField(max_length=255, blank=True)
```

### **Conversation:**
```python
class Conversation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    platform_user_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
```

### **Message:**
```python
class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    role = models.CharField(max_length=20)  # 'user' o 'assistant'
    metadata = models.JSONField(default=dict)
```

### **WebhookLog:**
```python
class WebhookLog(BaseModel):
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    response_status = models.IntegerField()
    error_message = models.TextField(blank=True)
```

---

## 🔄 6. Flujo Completo de un Mensaje

### **Ejemplo: Usuario envía "¿Por qué mi internet está lento?"**

1. **Webhook recibe mensaje:**
   - WhatsApp/Telegram envía POST a `/api/integrations/webhooks/{platform}/`

2. **View procesa:**
   - Extrae datos del mensaje
   - Crea WebhookLog
   - Llama a MessageHandler

3. **MessageHandler:**
   - Obtiene/crea usuario con `platform_user_id`
   - Obtiene/crea conversación activa
   - Guarda mensaje del usuario en BD

4. **ChatOrchestrator:**
   - Genera embedding de la pregunta
   - Busca en ChromaDB documentos similares
   - Encuentra: "Internet lento puede deberse a..." (distancia: 0.27)
   - Construye prompt con contexto + historial

5. **Gemini:**
   - Recibe prompt con contexto
   - Genera respuesta contextualizada

6. **MessageHandler:**
   - Guarda respuesta del bot en BD
   - Envía respuesta vía WhatsApp/Telegram API

7. **Usuario recibe respuesta:**
   - Respuesta precisa basada en documentos indexados

---

## 📊 7. Logging y Monitoreo

### **Ver logs de webhooks:**
```python
from apps.integrations.models import WebhookLog

# Últimos 10 webhooks
logs = WebhookLog.objects.order_by('-created_at')[:10]
for log in logs:
    print(f"{log.platform} - {log.event_type} - Status: {log.response_status}")
```

### **Ver conversaciones:**
```python
from apps.chat.models import Conversation, Message

# Conversaciones activas
conversations = Conversation.objects.filter(is_active=True)
for conv in conversations:
    messages = conv.messages.count()
    print(f"Usuario: {conv.user.username} - Mensajes: {messages}")
```

### **Ver mensajes de una conversación:**
```python
conversation = Conversation.objects.get(id=1)
messages = conversation.messages.order_by('created_at')
for msg in messages:
    print(f"{msg.role}: {msg.content[:50]}...")
```

---

## 🔧 8. Configuración de Webhooks

### **WhatsApp:**

1. Ve a Meta for Developers
2. WhatsApp → Configuration → Webhook
3. **Callback URL:** `https://tu-ngrok.ngrok-free.dev/api/integrations/webhooks/whatsapp/`
4. **Verify Token:** El que configuraste en la integración
5. Suscríbete a eventos: `messages`

### **Telegram:**

```bash
docker-compose exec web python manage.py setup_telegram_webhook \
  --url https://tu-ngrok.ngrok-free.dev/api/integrations/webhooks/telegram/
```

Verifica:
```bash
docker-compose exec web python manage.py setup_telegram_webhook --info
```

---

## 🧪 9. Probar el Sistema

### **Opción 1: Enviar mensaje real**
- Envía mensaje a tu bot de WhatsApp/Telegram
- Verifica respuesta

### **Opción 2: Simular webhook (desarrollo)**

**WhatsApp:**
```bash
curl -X POST http://localhost:9000/api/integrations/webhooks/whatsapp/ \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "1234567890",
            "text": {"body": "Hola"}
          }]
        }
      }]
    }]
  }'
```

**Telegram:**
```bash
curl -X POST http://localhost:9000/api/integrations/webhooks/telegram/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "chat": {"id": 123456},
      "text": "Hola"
    }
  }'
```

---

## 🎯 10. Próximos Pasos

### **Ya está todo implementado:**
- ✅ Webhooks de WhatsApp y Telegram
- ✅ MessageHandler con lógica de conversación
- ✅ Integración con RAG
- ✅ Respuestas con Gemini
- ✅ Logging completo
- ✅ Base de datos de conversaciones

### **Solo falta:**
1. Configurar webhooks en Meta/Telegram
2. Probar con mensajes reales
3. Indexar más documentos si es necesario

---

## 📚 Archivos Clave

- `apps/integrations/views.py` - Webhooks
- `apps/integrations/services/message_handler.py` - Lógica central
- `apps/integrations/services/whatsapp_service.py` - API WhatsApp
- `apps/integrations/services/telegram_service.py` - API Telegram
- `apps/ai/services/chat_orchestrator.py` - RAG + Gemini
- `apps/chat/models.py` - Modelos de conversación

---

**¡El sistema está completo y listo para usar!** 🎉
