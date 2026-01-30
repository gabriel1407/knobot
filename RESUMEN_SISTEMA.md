# KnoBot - Sistema Completo de Chatbot con IA/RAG

## 🎯 Resumen Ejecutivo

KnoBot es un sistema de chatbot inteligente para ISPs que integra **WhatsApp Business** y **Telegram** con capacidades de **RAG (Retrieval-Augmented Generation)** usando **Gemini API** para respuestas contextualizadas basadas en una base de conocimiento.

---

## ✅ Fases Completadas

### **Fase 1: API REST - Users CRUD**
- ✅ Componentes core reutilizables (BaseModelViewSet, serializers, pagination, permissions)
- ✅ Sistema completo de usuarios con CRUD
- ✅ Soft delete y bulk operations
- ✅ 15 endpoints de usuarios

### **Fase 2: Autenticación JWT**
- ✅ JWT con Simple JWT
- ✅ Access token (1h) y Refresh token (7d)
- ✅ Token blacklist y rotación automática
- ✅ Login con username o email
- ✅ 8 endpoints de autenticación

### **Fase 3: Integraciones WhatsApp y Telegram**
- ✅ WhatsAppService - Cliente completo para WhatsApp Business API
- ✅ TelegramService - Cliente completo para Telegram Bot API
- ✅ MessageHandler - Procesador con integración RAG
- ✅ Webhooks para recibir mensajes
- ✅ Gestión automática de usuarios y conversaciones
- ✅ Logs de auditoría

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIOS FINALES                          │
│              (WhatsApp / Telegram)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  WEBHOOKS (KnoBot)                           │
│  /api/integrations/webhooks/whatsapp/                        │
│  /api/integrations/webhooks/telegram/                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              MESSAGE HANDLER                                 │
│  - Gestión de usuarios                                       │
│  - Gestión de conversaciones                                 │
│  - Procesamiento asíncrono                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           CHAT ORCHESTRATOR + RAG                            │
│  - Búsqueda semántica (ChromaDB)                             │
│  - Embeddings (sentence-transformers)                        │
│  - Generación de respuesta (Gemini API)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              BASE DE CONOCIMIENTO                            │
│  - Documentos indexados                                      │
│  - Vector Store (ChromaDB)                                   │
│  - Soporta: PDF, DOCX, XLSX, PPTX, TXT, CSV, JSON,         │
│    imágenes, audio                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Stack Tecnológico

### **Backend**
- Django 4.2.9
- Django REST Framework 3.14.0
- PostgreSQL (puerto 5435)
- Redis (puerto 6380)
- Celery + Celery Beat

### **IA/ML**
- Google Gemini API (LLM)
- Sentence Transformers (embeddings)
- ChromaDB (vector store)
- PyPDF2, python-docx, openpyxl (procesamiento de documentos)
- pydub, SpeechRecognition (procesamiento de audio)

### **Integraciones**
- WhatsApp Business API
- Telegram Bot API
- httpx (cliente HTTP asíncrono)

### **Autenticación**
- Simple JWT
- Token blacklist

---

## 📁 Estructura del Proyecto

```
knowbot/
├── apps/
│   ├── users/          # Gestión de usuarios y autenticación
│   ├── chat/           # Modelos de conversaciones y mensajes
│   ├── ai/             # Servicios de IA (RAG, embeddings, chat)
│   ├── knowledge/      # Base de conocimiento y documentos
│   ├── integrations/   # WhatsApp, Telegram, webhooks
│   ├── tickets/        # Sistema de tickets
│   └── analytics/      # Métricas y estadísticas
├── core/               # Componentes reutilizables
├── knowbot/            # Configuración Django
├── scripts/            # Scripts de gestión
├── requirements/       # Dependencias
└── docker-compose.yml  # Orquestación de servicios
```

---

## 🚀 Endpoints Disponibles

### **Autenticación**
- `POST /api/auth/login/` - Login
- `POST /api/auth/register/` - Registro
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh/` - Refrescar token
- `GET /api/auth/me/` - Ver perfil
- `POST /api/auth/change-password/` - Cambiar contraseña

### **Usuarios**
- `GET /api/users/` - Listar usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/{id}/` - Ver usuario
- `PUT/PATCH /api/users/{id}/` - Actualizar usuario
- `DELETE /api/users/{id}/` - Eliminar (soft delete)
- `POST /api/users/{id}/restore/` - Restaurar usuario

### **Webhooks**
- `GET/POST /api/integrations/webhooks/whatsapp/` - Webhook WhatsApp
- `POST /api/integrations/webhooks/telegram/` - Webhook Telegram

### **Documentación**
- `GET /api/docs/` - Swagger UI
- `GET /api/schema/` - OpenAPI Schema

---

## 🛠️ Management Commands

### **Base de Conocimiento**
```bash
# Indexar documentos
docker-compose exec web python manage.py index_knowledge /path/to/docs --category soporte

# Buscar en la base de conocimiento
docker-compose exec web python manage.py search_knowledge "internet lento" --n-results 5

# Ver estadísticas del vector store
docker-compose exec web python manage.py vector_store_stats

# Limpiar vector store
docker-compose exec web python manage.py clear_vector_store
```

### **Chat**
```bash
# Probar chat con RAG
docker-compose exec web python manage.py test_chat
```

### **Integraciones**
```bash
# Configurar integraciones (interactivo)
docker-compose exec web python scripts/setup_integrations.py

# Configurar webhook de Telegram
docker-compose exec web python manage.py setup_telegram_webhook --url https://tu-dominio.com/api/integrations/webhooks/telegram/

# Ver info del webhook de Telegram
docker-compose exec web python manage.py setup_telegram_webhook --info
```

---

## 🔧 Configuración Rápida

### **1. Variables de Entorno (.env)**
```env
# Django
SECRET_KEY=tu-secret-key
DEBUG=True

# Database
DB_NAME=knowbot_db
DB_USER=knowbot_user
DB_PASSWORD=knowbot_pass
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Gemini API
GEMINI_API_KEY=tu-gemini-api-key

# WhatsApp (opcional)
WHATSAPP_PHONE_NUMBER_ID=tu-phone-number-id
WHATSAPP_ACCESS_TOKEN=tu-access-token
WHATSAPP_VERIFY_TOKEN=tu-verify-token

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=tu-bot-token
TELEGRAM_SECRET_TOKEN=tu-secret-token
```

### **2. Iniciar Sistema**
```bash
# Build y start
./scripts/setup.sh

# O manualmente
docker-compose up -d

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### **3. Indexar Conocimiento**
```bash
# Indexar documentos
docker-compose exec web python manage.py index_knowledge /app/docs --category soporte
```

### **4. Configurar Integraciones**
```bash
# Configurar WhatsApp y Telegram
docker-compose exec web python scripts/setup_integrations.py
```

---

## 📱 Flujo de Usuario

### **WhatsApp**
1. Usuario envía mensaje por WhatsApp
2. Meta envía webhook a KnoBot
3. Sistema crea/obtiene usuario automáticamente
4. MessageHandler procesa con RAG (5 docs de contexto)
5. Gemini genera respuesta personalizada
6. Respuesta enviada por WhatsApp

### **Telegram**
1. Usuario envía mensaje al bot
2. Telegram envía webhook a KnoBot
3. Sistema crea/obtiene usuario automáticamente
4. Bot muestra "escribiendo..."
5. MessageHandler procesa con RAG
6. Gemini genera respuesta personalizada
7. Respuesta enviada por Telegram

---

## 📈 Características Principales

### **IA/RAG**
- ✅ Búsqueda semántica en base de conocimiento
- ✅ Generación de respuestas con contexto
- ✅ Soporte multi-formato (documentos, audio, imágenes)
- ✅ Chunking inteligente de documentos
- ✅ Embeddings con sentence-transformers

### **Integraciones**
- ✅ WhatsApp Business API completa
- ✅ Telegram Bot API completa
- ✅ Webhooks seguros con verificación
- ✅ Logs de auditoría
- ✅ Procesamiento asíncrono

### **Gestión**
- ✅ Usuarios automáticos desde WhatsApp/Telegram
- ✅ Conversaciones por plataforma
- ✅ Historial de mensajes
- ✅ Soft delete
- ✅ Filtros y búsqueda

---

## 📚 Documentación Completa

- `API_REST_FASE1.md` - Users CRUD
- `API_REST_FASE2.md` - Autenticación JWT
- `API_REST_FASE3.md` - Integraciones WhatsApp/Telegram
- `MANAGEMENT_COMMANDS.md` - Comandos de gestión
- `SUPPORTED_FORMATS.md` - Formatos soportados
- `AI_SERVICES_README.md` - Servicios de IA
- `scripts/README.md` - Scripts de gestión

---

## 🎯 Próximas Fases (Opcionales)

### **Fase 4: Knowledge Base API**
- Endpoints para gestionar documentos
- Upload de archivos
- Búsqueda semántica vía API

### **Fase 5: Tickets y Analytics**
- Sistema de tickets
- Métricas de conversaciones
- Dashboard de analytics

### **Fase 6: Funcionalidades Avanzadas**
- Mensajes multimedia
- Botones interactivos
- Transferencia a agente humano
- Multi-idioma
- Horarios de atención

---

## 🔐 Seguridad

- ✅ JWT con blacklist
- ✅ Tokens de verificación para webhooks
- ✅ Secret tokens para Telegram
- ✅ HTTPS requerido en producción
- ✅ Validación de contraseñas
- ✅ Soft delete para auditoría

---

## 📞 Soporte

Para más información, consulta la documentación en los archivos `API_REST_FASE*.md` o contacta al equipo de desarrollo.

---

**Última actualización:** 27 de enero de 2026  
**Versión:** 1.0.0  
**Estado:** Sistema completo y funcional ✅
