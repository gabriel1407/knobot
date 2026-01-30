# ✅ Instalación de Dependencias de AI en Progreso

## Estado Actual

Las dependencias de AI están siendo instaladas en el contenedor Docker:

- ✅ **PyTorch 2.10.0+cpu** - Instalado (188 MB)
- ✅ **torchvision 0.25.0+cpu** - Instalado
- 🔄 **sentence-transformers 2.2.2** - Instalando
- 🔄 **chromadb 0.4.22** - Instalando

## Archivos Actualizados

### ✅ `requirements/base.txt`
```txt
# AI/ML - PyTorch CPU-only (más ligero)
--index-url https://download.pytorch.org/whl/cpu
torch==2.10.0+cpu
torchvision==0.25.0+cpu
--index-url https://pypi.org/simple

# AI/ML - Embeddings y Vector Store
sentence-transformers==2.2.2
chromadb==0.4.22
```

### ✅ `apps/ai/services/__init__.py`
- Importaciones opcionales con fallback
- Sistema funciona con o sin dependencias de AI

### ✅ `apps/integrations/services/message_handler.py`
- Modo dual: RAG completo o Gemini directo
- Detección automática de dependencias disponibles

---

## Una Vez Termine la Instalación

### 1. Verificar que todo funciona:
```bash
docker-compose exec web python manage.py check
```

### 2. Probar servicios de AI:
```bash
docker-compose exec web python manage.py shell
```

```python
# En el shell de Django
from apps.ai.services import EmbeddingService, VectorStore, ChatOrchestrator

# Probar embeddings
embedding_service = EmbeddingService()
embeddings = embedding_service.generate_embeddings(["Hola mundo"])
print(f"Embeddings generados: {len(embeddings[0])} dimensiones")

# Probar vector store
vector_store = VectorStore()
print("Vector store inicializado correctamente")

# Probar chat orchestrator
orchestrator = ChatOrchestrator()
print("Chat orchestrator listo")
```

### 3. Indexar documentos de prueba:
```bash
# Crear directorio de docs
mkdir -p /app/docs

# Crear documento de prueba
echo "Internet lento puede deberse a varios factores: saturación de red, problemas con el router, interferencias WiFi, o problemas con el proveedor." > /app/docs/soporte_internet.txt

# Indexar
docker-compose exec web python manage.py index_knowledge /app/docs --category soporte
```

### 4. Probar RAG:
```bash
docker-compose exec web python manage.py test_chat
```

### 5. Crear superusuario:
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Configurar integraciones:
```bash
docker-compose exec web python scripts/setup_integrations.py
```

---

## Comandos Útiles

### Ver logs de instalación:
```bash
docker-compose logs -f web
```

### Verificar paquetes instalados:
```bash
docker-compose exec web pip list | grep -E "torch|sentence|chroma"
```

### Reiniciar servicios:
```bash
docker-compose restart web
```

---

## Funcionalidades Disponibles Después de la Instalación

### ✅ RAG Completo:
- Búsqueda semántica en base de conocimiento
- Embeddings con sentence-transformers
- Vector store con ChromaDB
- Respuestas contextualizadas con Gemini

### ✅ Procesamiento de Documentos:
- PDF, DOCX, XLSX, PPTX
- TXT, CSV, JSON
- Imágenes (con OCR)
- Audio (con transcripción)

### ✅ Integraciones:
- WhatsApp Business API
- Telegram Bot API
- Webhooks seguros
- Respuestas automáticas con RAG

### ✅ API REST:
- Users CRUD (15 endpoints)
- Autenticación JWT (8 endpoints)
- Documentación Swagger
- Filtros y búsqueda

---

## Troubleshooting

### Si la instalación falla:

**Opción 1: Reintentar**
```bash
docker-compose exec web pip install --no-cache-dir sentence-transformers==2.2.2 chromadb==0.4.22
```

**Opción 2: Instalar por separado**
```bash
docker-compose exec web pip install --no-cache-dir sentence-transformers==2.2.2
docker-compose exec web pip install --no-cache-dir chromadb==0.4.22
```

**Opción 3: Reconstruir imagen**
```bash
docker-compose down
docker-compose build web --no-cache
docker-compose up -d
```

### Si hay problemas de conexión:

El sistema funciona perfectamente sin RAG usando Gemini directo. Puedes:
1. Usar el sistema ahora con Gemini
2. Instalar dependencias de AI más tarde cuando tengas mejor conexión

---

## Próximos Pasos Recomendados

1. ✅ Esperar a que termine la instalación
2. ✅ Verificar servicios de AI
3. ✅ Indexar documentos de prueba
4. ✅ Probar RAG con test_chat
5. ✅ Crear superusuario
6. ✅ Configurar integraciones WhatsApp/Telegram
7. ✅ Probar webhooks con ngrok
8. ✅ Documentar casos de uso específicos

---

**Última actualización:** 29 de enero de 2026  
**Estado:** Instalación en progreso 🔄
