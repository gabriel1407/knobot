# ✅ Checklist de Configuración - KnoBot

## 📋 **Estado Actual del Sistema**

---

## ✅ **COMPLETADO**

### **1. Infraestructura Base**
- ✅ Docker Compose configurado
- ✅ PostgreSQL funcionando
- ✅ Redis funcionando
- ✅ Django corriendo en puerto 9000
- ✅ Migraciones aplicadas

### **2. Dependencias AI/ML**
- ✅ sentence-transformers 2.7.0
- ✅ ChromaDB 0.4.22
- ✅ PyTorch 2.10.0+cpu
- ✅ NumPy 1.26.4 (compatible)
- ✅ Gemini API configurada

### **3. Servicios RAG**
- ✅ EmbeddingService funcionando
- ✅ VectorStore operativo (3 documentos de prueba)
- ✅ RAGService con búsqueda semántica
- ✅ ChatOrchestrator con Gemini 2.5-flash

### **4. Integración Telegram**
- ✅ Bot configurado en BotFather
- ✅ Token guardado en base de datos
- ✅ Webhook configurado con ngrok
- ✅ MessageHandler procesando mensajes
- ✅ Respuestas con RAG funcionando
- ✅ Status: **200 OK**

### **5. Integración WhatsApp**
- ✅ Configuración guardada en base de datos
- ✅ Webhook URL generada
- ✅ Verificación webhook (GET) funcionando

---

## ⏳ **PENDIENTE**

### **6. WhatsApp - Configuración en Meta**
**Estado:** Webhook verificado localmente, falta configurar en Meta for Developers

**Pasos:**
1. Ir a https://developers.facebook.com/apps
2. Seleccionar tu app de WhatsApp
3. WhatsApp → Configuration → Webhook
4. **Callback URL:** `https://[tu-ngrok].ngrok-free.dev/api/integrations/webhooks/whatsapp/`
5. **Verify Token:** (el que configuraste en setup_integrations.py)
6. Click "Verify and Save"
7. Suscribirse a eventos: `messages`
8. Enviar mensaje de prueba

**Documentación:** `CONFIGURAR_INTEGRACIONES.md` líneas 200-250

---

### **7. Indexación de Documentos de Producción**
**Estado:** Solo 3 documentos de prueba indexados

**Opciones:**

**A. Indexar documentos manualmente:**
```python
docker-compose exec web python manage.py shell

from apps.ai.services import RAGService
from apps.knowledge.models import Document

rag = RAGService()

# Indexar un documento
doc = Document.objects.first()
rag.index_document(
    document_id=str(doc.id),
    content=doc.content,
    metadata={'title': doc.title, 'category': doc.category}
)
```

**B. Script de indexación masiva:**
```bash
docker-compose exec web python manage.py index_documents
```

**C. Subir documentos vía Admin:**
1. Ir a http://localhost:9000/admin/
2. Knowledge → Documents → Add Document
3. Los documentos se indexarán automáticamente (si configuras signals)

---

### **8. Variables de Entorno Opcionales**

**Revisar `.env` para:**
```bash
# Producción
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com

# Seguridad
SECRET_KEY=<generar-nuevo-key-para-produccion>

# Email (para notificaciones)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Sentry (monitoreo de errores)
SENTRY_DSN=https://...

# Almacenamiento (para archivos en producción)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

---

### **9. Configuración de Producción**

**Cuando vayas a producción:**

**A. Reemplazar ngrok con dominio real:**
```bash
# En settings.py
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Actualizar webhooks:
# Telegram: https://tu-dominio.com/api/integrations/webhooks/telegram/
# WhatsApp: https://tu-dominio.com/api/integrations/webhooks/whatsapp/
```

**B. Configurar HTTPS con Let's Encrypt:**
```bash
# Agregar a docker-compose.yml
certbot:
  image: certbot/certbot
  volumes:
    - ./certbot/conf:/etc/letsencrypt
    - ./certbot/www:/var/www/certbot
```

**C. Configurar Gunicorn + Nginx:**
```bash
# Reemplazar runserver con Gunicorn
gunicorn knowbot.wsgi:application --bind 0.0.0.0:9000 --workers 4
```

---

### **10. Monitoreo y Logs**

**Configurar:**
- ✅ Django logging (ya configurado)
- ⏳ Sentry para errores en producción
- ⏳ Prometheus + Grafana para métricas
- ⏳ ELK Stack para logs centralizados

---

## 🎯 **Próximos Pasos Inmediatos**

### **Opción A: Probar Sistema Actual**
1. ✅ Telegram bot funcionando
2. ⏳ Enviar varios mensajes de prueba
3. ⏳ Verificar respuestas con contexto RAG
4. ⏳ Revisar conversaciones en admin

### **Opción B: Completar WhatsApp**
1. ⏳ Configurar webhook en Meta for Developers
2. ⏳ Enviar mensaje de prueba desde WhatsApp
3. ⏳ Verificar respuesta del bot

### **Opción C: Indexar Documentos Reales**
1. ⏳ Crear documentos de soporte técnico
2. ⏳ Indexarlos en ChromaDB
3. ⏳ Probar búsquedas con preguntas reales

---

## 📊 **Resumen de Estado**

| Componente | Estado | Acción |
|------------|--------|--------|
| **Backend Django** | ✅ Funcionando | Ninguna |
| **Base de Datos** | ✅ Operativa | Ninguna |
| **RAG System** | ✅ Funcionando | Indexar más docs |
| **Telegram Bot** | ✅ Activo | Probar más |
| **WhatsApp Bot** | ⚠️ Configurado | Activar webhook en Meta |
| **Documentos** | ⚠️ Solo prueba | Indexar producción |
| **Producción** | ❌ No configurado | Dominio + HTTPS |

---

## 🚀 **Recomendación**

**Para desarrollo/pruebas:**
1. Probar Telegram bot con más mensajes
2. Configurar WhatsApp webhook en Meta
3. Indexar 10-20 documentos reales de soporte

**Para producción:**
1. Conseguir dominio
2. Configurar HTTPS
3. Actualizar webhooks
4. Configurar monitoreo
5. Indexar base de conocimiento completa

---

## 📞 **Soporte**

- **Documentación:** Ver archivos `.md` en el proyecto
- **Logs:** `docker-compose logs -f web`
- **Admin:** http://localhost:9000/admin/
- **API:** http://localhost:9000/api/

---

**Sistema listo para desarrollo y pruebas. ¿Qué quieres configurar ahora?**
