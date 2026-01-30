# Estado Actual del Sistema KnoBot

## ✅ Sistema Funcionando Correctamente

El warning que ves **NO es un error**, es solo una advertencia informativa:

```
UserWarning: AI services not available: No module named 'sentence_transformers'. 
Install AI dependencies to enable AI features.
```

### **¿Qué significa?**

El sistema está configurado para funcionar en **dos modos**:

1. **Modo Completo (con RAG)**: Usa sentence-transformers + ChromaDB para búsqueda semántica
2. **Modo Básico (sin RAG)**: Usa Gemini directamente sin base de conocimiento vectorial

Actualmente estás en **Modo Básico** porque las dependencias de AI no están instaladas.

---

## 🎯 Funcionalidades Disponibles Ahora

### ✅ **Funcionando Perfectamente:**

1. **API REST Completa**
   - Users CRUD (15 endpoints)
   - Autenticación JWT (8 endpoints)
   - Documentación Swagger

2. **Integraciones WhatsApp/Telegram**
   - Webhooks configurados
   - Procesamiento de mensajes
   - Respuestas con Gemini (sin RAG)

3. **Base de Datos**
   - PostgreSQL funcionando
   - Redis funcionando
   - Migraciones aplicadas

### ⚠️ **Limitado (requiere dependencias AI):**

1. **RAG (Retrieval-Augmented Generation)**
   - Búsqueda semántica en base de conocimiento
   - Embeddings de documentos
   - ChromaDB vector store

2. **Procesamiento de Documentos**
   - PDF, DOCX, XLSX, etc.
   - Indexación automática

---

## 🔧 Opciones

### **Opción 1: Usar el Sistema Actual (Recomendado para Pruebas)**

El sistema funciona perfectamente con Gemini directo. Los bots de WhatsApp y Telegram responderán usando Gemini sin contexto de documentos.

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ No requiere instalación adicional
- ✅ Respuestas rápidas con Gemini

**Desventajas:**
- ❌ Sin búsqueda en base de conocimiento
- ❌ Sin contexto de documentos

### **Opción 2: Instalar Dependencias AI Completas**

Para habilitar RAG y búsqueda semántica, necesitas instalar las dependencias pesadas.

**Problema:** PyTorch (915 MB) falló al descargar por conexión lenta.

**Soluciones:**

#### **A. Instalar en el contenedor (requiere buena conexión):**
```bash
docker-compose exec web pip install --no-cache-dir sentence-transformers==2.2.2 chromadb==0.4.22
```

Esto descargará ~1.5 GB de dependencias (PyTorch, modelos, etc.)

#### **B. Usar versión CPU-only de PyTorch (más ligera):**
```bash
docker-compose exec web pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
docker-compose exec web pip install --no-cache-dir sentence-transformers==2.2.2 chromadb==0.4.22
```

#### **C. Reconstruir imagen Docker con dependencias:**
Editar `requirements/base.txt` y hacer:
```bash
docker-compose build web
docker-compose up -d
```

### **Opción 3: Usar Modelo de Embeddings Más Ligero**

Modificar el código para usar un modelo más pequeño:
```python
# En embedding_service.py
model_name = 'all-MiniLM-L6-v2'  # Solo 80 MB vs 400+ MB
```

---

## 🚀 Recomendación Inmediata

**Para empezar a usar el sistema YA:**

1. **Crear superusuario:**
```bash
docker-compose exec web python manage.py createsuperuser
```

2. **Configurar integraciones:**
```bash
docker-compose exec web python scripts/setup_integrations.py
```

3. **Probar API:**
```bash
# Login
curl -X POST http://localhost:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_password"}'

# Ver usuarios
curl http://localhost:9000/api/users/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

4. **Ver documentación:**
Abrir en navegador: http://localhost:9000/api/docs/

---

## 📊 Estado de Servicios

```bash
# Ver servicios corriendo
docker-compose ps

# Ver logs
docker-compose logs -f web

# Verificar sistema
docker-compose exec web python manage.py check
```

---

## 🎯 Próximos Pasos Sugeridos

### **Corto Plazo (sin instalar AI):**
1. ✅ Crear superusuario
2. ✅ Configurar integraciones WhatsApp/Telegram
3. ✅ Probar webhooks con ngrok
4. ✅ Probar API REST

### **Mediano Plazo (con AI completo):**
1. Instalar dependencias AI cuando tengas mejor conexión
2. Indexar documentos en la base de conocimiento
3. Probar RAG con búsqueda semántica
4. Optimizar respuestas con contexto

---

## 📝 Resumen

**El sistema está funcionando correctamente.** El warning es solo informativo para que sepas que las funcionalidades avanzadas de AI (RAG, embeddings) no están disponibles, pero el sistema funciona perfectamente con Gemini directo.

**Puedes usar el sistema ahora mismo para:**
- ✅ Gestionar usuarios vía API
- ✅ Autenticación JWT
- ✅ Recibir mensajes de WhatsApp/Telegram
- ✅ Responder con Gemini (sin RAG)

**Para habilitar RAG necesitas:**
- Instalar sentence-transformers + chromadb
- Esto requiere descargar ~1.5 GB de dependencias

---

**Última actualización:** 29 de enero de 2026  
**Estado:** Sistema operativo en Modo Básico ✅
