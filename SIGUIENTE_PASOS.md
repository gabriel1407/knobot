# 🚀 Siguientes Pasos - KnoBot

## ✅ Estado Actual

### **Completado:**
- ✅ Django + DRF configurado
- ✅ PostgreSQL y Redis funcionando
- ✅ Migraciones aplicadas
- ✅ API REST Users + Auth JWT (23 endpoints)
- ✅ Integraciones WhatsApp/Telegram configuradas
- ✅ PyTorch 2.10.0+cpu instalado
- ✅ Requirements.txt actualizado
- 🔄 sentence-transformers + chromadb instalándose

### **Sistema Funcional:**
El sistema ya está operativo con Gemini directo. Una vez termine la instalación de AI, tendrás RAG completo.

---

## 📋 Checklist de Configuración

### 1. ✅ Verificar Instalación de AI (cuando termine)
```bash
docker-compose exec web python manage.py check
docker-compose exec web python -c "from apps.ai.services import EmbeddingService; print('AI OK')"
```

### 2. 🔲 Crear Superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

**Datos sugeridos:**
- Username: `admin`
- Email: `admin@knowbot.local`
- Password: (tu elección)

### 3. 🔲 Indexar Base de Conocimiento

**Crear documentos de prueba:**
```bash
docker-compose exec web mkdir -p /app/docs/soporte

docker-compose exec web bash -c 'cat > /app/docs/soporte/internet.txt << EOF
Problemas de Internet Lento

Causas comunes:
1. Saturación de red - Muchos dispositivos conectados
2. Router antiguo o mal configurado
3. Interferencias WiFi de vecinos
4. Problemas con el proveedor ISP
5. Cables dañados

Soluciones:
- Reiniciar el router (desconectar 30 segundos)
- Cambiar canal WiFi (usar 1, 6 u 11)
- Actualizar firmware del router
- Verificar velocidad con speedtest
- Contactar soporte técnico si persiste
EOF'

docker-compose exec web bash -c 'cat > /app/docs/soporte/router.txt << EOF
Configuración del Router

Pasos para configurar:
1. Conectar router a la corriente
2. Conectar cable de internet al puerto WAN
3. Acceder a 192.168.1.1 desde navegador
4. Usuario: admin, Contraseña: admin (cambiar después)
5. Configurar nombre de red WiFi (SSID)
6. Establecer contraseña WPA2 segura
7. Guardar cambios y reiniciar

Recomendaciones:
- Cambiar contraseña por defecto
- Usar WPA2 o WPA3
- Desactivar WPS
- Actualizar firmware regularmente
EOF'
```

**Indexar:**
```bash
docker-compose exec web python manage.py index_knowledge /app/docs/soporte --category soporte_tecnico
```

### 4. 🔲 Probar RAG
```bash
docker-compose exec web python manage.py test_chat
```

Preguntas de prueba:
- "¿Por qué mi internet está lento?"
- "¿Cómo configuro mi router?"
- "¿Qué hago si no tengo conexión?"

### 5. 🔲 Configurar Variables de Entorno

**Editar `.env`:**
```bash
# Gemini API (REQUERIDO para chat)
GEMINI_API_KEY=tu_api_key_de_gemini

# WhatsApp Business (opcional)
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_ACCESS_TOKEN=tu_access_token
WHATSAPP_VERIFY_TOKEN=tu_verify_token_personalizado

# Telegram Bot (opcional)
TELEGRAM_BOT_TOKEN=tu_bot_token_de_botfather
TELEGRAM_SECRET_TOKEN=tu_secret_token_personalizado
```

**Reiniciar servicios:**
```bash
docker-compose restart web
```

### 6. 🔲 Configurar Integraciones

**Opción A: Script interactivo**
```bash
docker-compose exec web python scripts/setup_integrations.py
```

**Opción B: Django Admin**
1. Ir a http://localhost:9000/admin/
2. Login con superusuario
3. Ir a "Integrations"
4. Crear nueva integración (WhatsApp o Telegram)

### 7. 🔲 Probar API REST

**Login:**
```bash
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_password"}'
```

**Guardar el access_token** de la respuesta.

**Ver usuarios:**
```bash
curl http://localhost:9000/api/users/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

**Ver documentación:**
- Swagger UI: http://localhost:9000/api/docs/
- OpenAPI Schema: http://localhost:9000/api/schema/

### 8. 🔲 Configurar Webhooks (para WhatsApp/Telegram)

**Opción A: Usar ngrok para pruebas locales**
```bash
# Instalar ngrok: https://ngrok.com/
ngrok http 9000
```

Usar la URL de ngrok (ej: `https://abc123.ngrok.io`) para configurar webhooks.

**WhatsApp:**
1. Ir a Meta for Developers
2. Configurar webhook: `https://abc123.ngrok.io/api/integrations/webhooks/whatsapp/`
3. Verify token: el que configuraste en la integración

**Telegram:**
```bash
docker-compose exec web python manage.py setup_telegram_webhook \
  --url https://abc123.ngrok.io/api/integrations/webhooks/telegram/
```

### 9. 🔲 Probar Chat End-to-End

**WhatsApp:**
1. Enviar mensaje al número configurado
2. Ver logs: `docker-compose logs -f web`
3. Verificar respuesta del bot

**Telegram:**
1. Buscar tu bot en Telegram
2. Enviar `/start` o cualquier mensaje
3. Verificar respuesta con contexto de RAG

---

## 🔧 Comandos Útiles

### **Ver logs:**
```bash
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f redis
```

### **Acceder al shell de Django:**
```bash
docker-compose exec web python manage.py shell
```

### **Acceder a PostgreSQL:**
```bash
docker-compose exec db psql -U knowbot_user -d knowbot_db
```

### **Ver estadísticas del vector store:**
```bash
docker-compose exec web python manage.py vector_store_stats
```

### **Buscar en la base de conocimiento:**
```bash
docker-compose exec web python manage.py search_knowledge "internet lento" --n-results 5
```

### **Limpiar vector store:**
```bash
docker-compose exec web python manage.py clear_vector_store
```

---

## 📊 Monitoreo

### **Ver integraciones activas:**
```bash
docker-compose exec web python manage.py shell
```
```python
from apps.integrations.models import Integration
for i in Integration.objects.filter(is_enabled=True):
    print(f"{i.name} ({i.type}): {i.config}")
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

### **Ver conversaciones:**
```bash
docker-compose exec web python manage.py shell
```
```python
from apps.chat.models import Conversation, Message
for conv in Conversation.objects.filter(is_active=True):
    msgs = conv.messages.count()
    print(f"Usuario: {conv.user.username} - Mensajes: {msgs}")
```

---

## 🎯 Casos de Uso Recomendados

### **1. Soporte Técnico ISP**
- Indexar manuales de routers
- Indexar guías de troubleshooting
- Indexar políticas de servicio
- Configurar respuestas automáticas 24/7

### **2. FAQ Automatizado**
- Indexar preguntas frecuentes
- Configurar horarios de atención
- Transferencia a agente humano si es necesario

### **3. Onboarding de Clientes**
- Guías de instalación
- Configuración de equipos
- Primeros pasos

---

## 📚 Documentación Disponible

- `README.md` - Visión general del proyecto
- `API_REST_FASE1.md` - Documentación Users CRUD
- `API_REST_FASE2.md` - Documentación Auth JWT
- `API_REST_FASE3.md` - Documentación Integraciones
- `RESUMEN_SISTEMA.md` - Resumen ejecutivo completo
- `ESTADO_ACTUAL.md` - Estado y opciones
- `INSTALACION_COMPLETADA.md` - Guía post-instalación
- `scripts/README.md` - Scripts de gestión

---

## 🐛 Troubleshooting

### **Si RAG no funciona:**
```bash
# Verificar que las dependencias están instaladas
docker-compose exec web pip list | grep -E "torch|sentence|chroma"

# Reiniciar servicios
docker-compose restart web

# Ver logs de errores
docker-compose logs web | grep -i error
```

### **Si webhooks no reciben mensajes:**
- Verificar que la URL es HTTPS (requerido)
- Verificar que los tokens coinciden
- Ver logs de webhooks en la base de datos
- Verificar que la integración está habilitada

### **Si Gemini no responde:**
- Verificar que `GEMINI_API_KEY` está configurado
- Verificar cuota de API en Google AI Studio
- Ver logs de errores en Django

---

## ✅ Checklist Final

- [ ] Instalación de AI completada
- [ ] Superusuario creado
- [ ] Base de conocimiento indexada
- [ ] RAG probado y funcionando
- [ ] Variables de entorno configuradas
- [ ] Integraciones configuradas (WhatsApp/Telegram)
- [ ] Webhooks configurados
- [ ] Chat end-to-end probado
- [ ] Documentación revisada
- [ ] Sistema en producción

---

**¡El sistema está casi listo!** Solo falta que termine la instalación de las dependencias de AI y podrás empezar a usar KnoBot con todas sus funcionalidades.

**Última actualización:** 29 de enero de 2026
