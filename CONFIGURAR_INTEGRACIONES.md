# 🚀 Configurar Integraciones WhatsApp y Telegram

## 🤖 Opción 1: Telegram Bot (Recomendado - Más Fácil)

### **Paso 1: Crear el Bot**

1. Abre Telegram en tu teléfono o desktop
2. Busca **@BotFather**
3. Envía: `/newbot`
4. Nombre del bot: `KnoBot Support` (o el que prefieras)
5. Username: `tu_nombre_bot` (debe terminar en 'bot', ej: `knowbot_support_bot`)
6. BotFather te dará un **token** como:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   **¡Guarda este token!**

### **Paso 2: Configurar en KnoBot**

```bash
docker-compose exec web python scripts/setup_integrations.py
```

Selecciona opción **2** (Telegram) y pega:
- **Bot Token**: El token que te dio BotFather
- **Secret Token**: Deja vacío o pon algo como `mi_secret_123` (opcional)

### **Paso 3: Configurar Webhook**

Primero necesitas exponer tu servidor local con **ngrok**:

#### **Instalar ngrok:**
```bash
# Descarga desde: https://ngrok.com/download
# O con snap:
snap install ngrok

# Autenticar (regístrate gratis en ngrok.com):
ngrok authtoken TU_TOKEN_DE_NGROK
```

#### **Iniciar ngrok:**
```bash
ngrok http 9000
```

Verás algo como:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:9000
```

**Copia la URL HTTPS** (ej: `https://abc123.ngrok.io`)

#### **Configurar webhook de Telegram:**
```bash
docker-compose exec web python manage.py setup_telegram_webhook --url https://abc123.ngrok.io/api/integrations/webhooks/telegram/
```

### **Paso 4: Probar**

1. Busca tu bot en Telegram por el username
2. Envía `/start`
3. Envía cualquier pregunta: `¿Por qué mi internet está lento?`
4. El bot responderá usando RAG + Gemini 🎉

---

## 📱 Opción 2: WhatsApp Business API

### **Requisitos:**
- Cuenta de Meta for Developers
- WhatsApp Business App configurada
- Número de teléfono verificado

### **Paso 1: Crear App en Meta for Developers**

1. Ve a: https://developers.facebook.com/
2. Crea una cuenta o inicia sesión
3. Click en **"My Apps"** → **"Create App"**
4. Selecciona **"Business"**
5. Nombre: `KnoBot WhatsApp`
6. Email de contacto

### **Paso 2: Agregar WhatsApp al App**

1. En el dashboard del app, busca **"WhatsApp"**
2. Click en **"Set Up"**
3. Selecciona o crea una **Business Account**
4. Agrega un número de teléfono de prueba (o usa tu propio número)

### **Paso 3: Obtener Credenciales**

En la sección de WhatsApp:

1. **Phone Number ID**: 
   - Ve a "API Setup"
   - Copia el "Phone number ID"
   
2. **Access Token**:
   - En "API Setup" verás un "Temporary access token"
   - Para producción, genera un "Permanent token" en "Settings" → "System Users"

3. **Verify Token**:
   - Crea uno personalizado (ej: `mi_verify_token_seguro_123`)

### **Paso 4: Configurar en KnoBot**

```bash
docker-compose exec web python scripts/setup_integrations.py
```

Selecciona opción **1** (WhatsApp) y pega:
- **Phone Number ID**: El ID que copiaste
- **Access Token**: El token de acceso
- **Verify Token**: Tu token personalizado

### **Paso 5: Configurar Webhook en Meta**

1. Inicia ngrok:
   ```bash
   ngrok http 9000
   ```

2. Copia la URL HTTPS (ej: `https://abc123.ngrok.io`)

3. En Meta for Developers:
   - Ve a WhatsApp → "Configuration"
   - Click en "Edit" en Webhook
   - **Callback URL**: `https://abc123.ngrok.io/api/integrations/webhooks/whatsapp/`
   - **Verify Token**: El mismo que pusiste en KnoBot
   - Click "Verify and Save"

4. Suscríbete a eventos:
   - Marca: `messages`
   - Click "Subscribe"

### **Paso 6: Probar**

1. Envía un mensaje al número de WhatsApp configurado
2. El bot responderá usando RAG + Gemini 🎉

---

## 🔍 Ver Logs en Tiempo Real

```bash
docker-compose logs -f web
```

---

## 📊 Verificar Integraciones

```bash
docker-compose exec web python scripts/setup_integrations.py
```

Selecciona opción **3** para ver las integraciones configuradas.

---

## 🐛 Troubleshooting

### **Telegram no responde:**
- Verifica que ngrok esté corriendo
- Verifica que el webhook esté configurado:
  ```bash
  docker-compose exec web python manage.py setup_telegram_webhook --info
  ```
- Revisa logs: `docker-compose logs -f web`

### **WhatsApp no responde:**
- Verifica que el webhook esté verificado en Meta
- Verifica que estés suscrito a eventos "messages"
- Revisa que el Access Token no haya expirado
- Revisa logs: `docker-compose logs -f web`

### **Error "GEMINI_API_KEY not configured":**
- Verifica que `.env` tenga `GEMINI_API_KEY=tu_key`
- Reinicia servicios: `docker-compose restart web`

### **Respuestas sin contexto:**
- Indexa documentos primero:
  ```bash
  docker-compose exec web python manage.py index_knowledge /app/docs
  ```

---

## 📝 Comandos Útiles

### **Ver webhooks de Telegram:**
```bash
docker-compose exec web python manage.py setup_telegram_webhook --info
```

### **Eliminar webhook de Telegram:**
```bash
docker-compose exec web python manage.py setup_telegram_webhook --delete
```

### **Ver logs de webhooks:**
```bash
docker-compose exec web python manage.py shell
```
```python
from apps.integrations.models import WebhookLog
logs = WebhookLog.objects.order_by('-created_at')[:10]
for log in logs:
    print(f"{log.platform} - {log.event_type} - {log.response_status}")
```

---

## 🎯 Flujo Completo

```
Usuario envía mensaje
    ↓
Webhook recibe mensaje
    ↓
MessageHandler procesa
    ↓
ChatOrchestrator con RAG
    ↓
Búsqueda en ChromaDB
    ↓
Gemini genera respuesta
    ↓
Respuesta enviada al usuario
```

---

## ✅ Checklist

### **Telegram:**
- [ ] Bot creado en @BotFather
- [ ] Token obtenido
- [ ] Integración configurada en KnoBot
- [ ] ngrok corriendo
- [ ] Webhook configurado
- [ ] Mensaje de prueba enviado
- [ ] Bot responde correctamente

### **WhatsApp:**
- [ ] App creada en Meta for Developers
- [ ] WhatsApp agregado al app
- [ ] Credenciales obtenidas
- [ ] Integración configurada en KnoBot
- [ ] ngrok corriendo
- [ ] Webhook verificado en Meta
- [ ] Suscrito a eventos "messages"
- [ ] Mensaje de prueba enviado
- [ ] Bot responde correctamente

---

## 🚀 ¡Listo para Producción!

Para producción, en lugar de ngrok:
1. Despliega en un servidor con dominio (ej: AWS, DigitalOcean, Heroku)
2. Configura HTTPS con certificado SSL
3. Usa la URL de tu dominio en los webhooks
4. Genera tokens permanentes (no temporales)

---

**¿Necesitas ayuda? Revisa los logs y la documentación en `API_REST_FASE3.md`**
