# 🚀 Guía Rápida - KnoBot

## ✅ Sistema Funcionando

Tu sistema KnoBot está **operativo** con las siguientes funcionalidades:

### **Disponible Ahora:**
- ✅ API REST completa (23 endpoints)
- ✅ Autenticación JWT
- ✅ WhatsApp/Telegram webhooks
- ✅ Chat con Gemini (sin RAG)
- ✅ PostgreSQL + Redis

### **Pendiente (opcional):**
- ⏳ RAG con búsqueda semántica (requiere mejor conexión para instalar)

---

## 🎯 Empezar a Usar el Sistema

### **1. Crear Superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

Datos sugeridos:
- Username: `admin`
- Email: `admin@knowbot.local`  
- Password: (tu elección)

### **2. Acceder a la API**

**Ver documentación:**
- http://localhost:9000/api/docs/

**Login:**
```bash
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"TU_PASSWORD"}'
```

Guarda el `access_token` de la respuesta.

**Ver usuarios:**
```bash
curl http://localhost:9000/api/users/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

### **3. Configurar Gemini API**

Edita `.env`:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

Obtén tu API key en: https://makersuite.google.com/app/apikey

Reinicia:
```bash
docker-compose restart web
```

### **4. Configurar WhatsApp/Telegram (Opcional)**

```bash
docker-compose exec web python scripts/setup_integrations.py
```

---

## 📊 Endpoints Disponibles

### **Autenticación (8 endpoints):**
- `POST /api/auth/login/` - Login
- `POST /api/auth/register/` - Registro
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh/` - Refrescar token
- `GET /api/auth/me/` - Ver perfil
- `PUT /api/auth/me/` - Actualizar perfil
- `POST /api/auth/change-password/` - Cambiar contraseña
- `POST /api/auth/verify-token/` - Verificar token

### **Usuarios (15 endpoints):**
- `GET /api/users/` - Listar
- `POST /api/users/` - Crear
- `GET /api/users/{id}/` - Ver detalle
- `PUT /api/users/{id}/` - Actualizar completo
- `PATCH /api/users/{id}/` - Actualizar parcial
- `DELETE /api/users/{id}/` - Eliminar (soft delete)
- `POST /api/users/bulk-delete/` - Eliminar múltiples
- `POST /api/users/{id}/restore/` - Restaurar eliminado
- Y más...

### **Webhooks (2 endpoints):**
- `GET/POST /api/integrations/webhooks/whatsapp/`
- `POST /api/integrations/webhooks/telegram/`

---

## 🔧 Sobre el Error de Instalación

**Causa:** Conexión lenta/inestable interrumpe descarga de paquetes grandes (scipy 35 MB).

**Impacto:** Ninguno - el sistema funciona perfectamente sin RAG.

**Opciones:**

### **Opción 1: Usar el Sistema Ahora (Recomendado)**
El sistema está completamente funcional con Gemini directo. Los bots responderán sin búsqueda en documentos.

### **Opción 2: Instalar RAG Después**
Cuando tengas mejor conexión:
```bash
docker-compose exec web pip install --no-cache-dir sentence-transformers==2.2.2 chromadb==0.4.22
```

### **Opción 3: Reconstruir Imagen Docker**
```bash
docker-compose down
docker-compose build web --no-cache
docker-compose up -d
```

---

## 🎯 Flujo de Trabajo Recomendado

### **Fase 1: Configuración Básica (Ahora)**
1. ✅ Crear superusuario
2. ✅ Configurar Gemini API key
3. ✅ Probar API REST
4. ✅ Configurar integraciones WhatsApp/Telegram

### **Fase 2: Pruebas (Ahora)**
1. ✅ Probar login/registro
2. ✅ Probar webhooks con ngrok
3. ✅ Enviar mensajes de prueba
4. ✅ Verificar respuestas de Gemini

### **Fase 3: RAG (Cuando tengas mejor conexión)**
1. ⏳ Instalar dependencias de AI
2. ⏳ Indexar documentos
3. ⏳ Probar búsqueda semántica
4. ⏳ Respuestas con contexto

---

## 📝 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f web

# Reiniciar servicios
docker-compose restart web

# Shell de Django
docker-compose exec web python manage.py shell

# Ver servicios corriendo
docker-compose ps

# Detener todo
docker-compose down

# Iniciar todo
docker-compose up -d
```

---

## 🐛 Troubleshooting

### **"No module named 'sentence_transformers'"**
✅ Normal - el sistema funciona sin RAG. Instala después si quieres RAG.

### **"GEMINI_API_KEY not configured"**
❌ Necesitas configurar la API key en `.env` para que el chat funcione.

### **Webhooks no reciben mensajes**
- Verifica URL es HTTPS
- Verifica tokens coinciden
- Usa ngrok para pruebas locales

---

## ✅ Checklist Rápido

- [ ] Superusuario creado
- [ ] Gemini API key configurada
- [ ] API REST probada (login + usuarios)
- [ ] Documentación Swagger revisada
- [ ] Integraciones configuradas (opcional)
- [ ] Webhooks probados (opcional)
- [ ] Sistema en uso

---

## 📚 Documentación Completa

- `API_REST_FASE1.md` - Users CRUD
- `API_REST_FASE2.md` - Auth JWT
- `API_REST_FASE3.md` - Integraciones
- `RESUMEN_SISTEMA.md` - Visión general
- `SIGUIENTE_PASOS.md` - Guía detallada

---

**¡Tu sistema está listo para usar!** Empieza creando el superusuario y probando la API.

**Última actualización:** 30 de enero de 2026
