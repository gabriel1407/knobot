# 📄 API para Subir y Auto-Indexar Documentos

## 🎯 **¿Qué hace esta API?**

Permite **subir archivos** (PDF, DOCX, TXT, MD) y **automáticamente**:
1. Extrae el texto del archivo
2. Lo guarda en la base de datos
3. Lo indexa en ChromaDB
4. Queda disponible para el bot con RAG

---

## 🚀 **Endpoints Disponibles**

### **1. Subir Documentos (Múltiples archivos)**

```http
POST /api/knowledge/documents/upload/
Content-Type: multipart/form-data
```

**Parámetros:**
- `files` (required): Lista de archivos a subir
- `knowledge_base` (required): ID de la base de conocimiento
- `auto_index` (optional): Boolean, default `true`
- `category` (optional): String, categoría del documento

**Ejemplo con cURL:**
```bash
curl -X POST http://localhost:9000/api/knowledge/documents/upload/ \
  -F "files=@documento1.pdf" \
  -F "files=@documento2.txt" \
  -F "files=@guia.docx" \
  -F "knowledge_base=<KB_ID>" \
  -F "auto_index=true" \
  -F "category=soporte"
```

**Ejemplo con Python:**
```python
import requests

url = "http://localhost:9000/api/knowledge/documents/upload/"

files = [
    ('files', open('documento1.pdf', 'rb')),
    ('files', open('documento2.txt', 'rb')),
]

data = {
    'knowledge_base': 'uuid-de-knowledge-base',
    'auto_index': True,
    'category': 'soporte'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Respuesta:**
```json
{
  "success": true,
  "created": 2,
  "documents": [
    {
      "id": "uuid-1",
      "title": "documento1.pdf",
      "file_type": "pdf",
      "is_indexed": true
    },
    {
      "id": "uuid-2",
      "title": "documento2.txt",
      "file_type": "txt",
      "is_indexed": true
    }
  ],
  "errors": []
}
```

---

### **2. Crear Base de Conocimiento**

```http
POST /api/knowledge/knowledge-bases/
Content-Type: application/json
```

**Body:**
```json
{
  "title": "Soporte Técnico ISP",
  "description": "Base de conocimiento para soporte de internet",
  "category": "soporte",
  "is_public": true
}
```

**Respuesta:**
```json
{
  "id": "uuid-kb",
  "title": "Soporte Técnico ISP",
  "description": "Base de conocimiento para soporte de internet",
  "category": "soporte",
  "is_public": true,
  "documents_count": 0,
  "created_at": "2026-02-02T18:00:00Z",
  "updated_at": "2026-02-02T18:00:00Z"
}
```

---

### **3. Listar Bases de Conocimiento**

```http
GET /api/knowledge/knowledge-bases/
```

**Respuesta:**
```json
[
  {
    "id": "uuid-kb",
    "title": "Soporte Técnico ISP",
    "description": "...",
    "category": "soporte",
    "is_public": true,
    "documents_count": 15,
    "created_at": "2026-02-02T18:00:00Z",
    "updated_at": "2026-02-02T18:00:00Z"
  }
]
```

---

### **4. Listar Documentos**

```http
GET /api/knowledge/documents/
GET /api/knowledge/documents/?knowledge_base=<KB_ID>
```

**Respuesta:**
```json
[
  {
    "id": "uuid-doc",
    "knowledge_base": "uuid-kb",
    "title": "Problemas de velocidad.pdf",
    "content": "Texto extraído del PDF...",
    "file_type": "pdf",
    "file_url": "/media/documents/2026/02/02/problemas.pdf",
    "metadata": {"category": "soporte"},
    "is_indexed": true,
    "indexed_at": "2026-02-02T18:05:00Z",
    "created_at": "2026-02-02T18:00:00Z",
    "updated_at": "2026-02-02T18:05:00Z"
  }
]
```

---

### **5. Re-indexar un Documento**

```http
POST /api/knowledge/documents/{id}/reindex/
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Documento 'problemas.pdf' re-indexado exitosamente"
}
```

---

## 📝 **Tipos de Archivos Soportados**

| Tipo | Extensión | Content-Type | Estado |
|------|-----------|--------------|--------|
| PDF | `.pdf` | `application/pdf` | ✅ Soportado |
| Word | `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | ✅ Soportado |
| Texto | `.txt` | `text/plain` | ✅ Soportado |
| Markdown | `.md` | `text/markdown` | ✅ Soportado |
| Word antiguo | `.doc` | `application/msword` | ⚠️ No soportado (convertir a .docx) |

**Límites:**
- Tamaño máximo: **10 MB** por archivo
- Múltiples archivos: Sin límite (pero se procesan uno por uno)

---

## 🔄 **Flujo Automático**

```
1. Usuario sube archivo (PDF, DOCX, TXT)
   ↓
2. API extrae texto del archivo
   ↓
3. Guarda en base de datos (modelo Document)
   ↓
4. Signal detecta nuevo documento
   ↓
5. Auto-indexa en ChromaDB con embeddings
   ↓
6. Marca documento como indexado
   ↓
7. ✅ Disponible para búsqueda RAG
```

---

## 🧪 **Ejemplo Completo: Subir y Usar**

### **Paso 1: Crear Base de Conocimiento**
```bash
curl -X POST http://localhost:9000/api/knowledge/knowledge-bases/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FAQ ISP",
    "description": "Preguntas frecuentes",
    "category": "faq",
    "is_public": true
  }'
```

Respuesta: `{"id": "kb-123", ...}`

---

### **Paso 2: Subir Documentos**
```bash
curl -X POST http://localhost:9000/api/knowledge/documents/upload/ \
  -F "files=@faq_velocidad.pdf" \
  -F "files=@guia_router.docx" \
  -F "files=@soluciones.txt" \
  -F "knowledge_base=kb-123" \
  -F "category=soporte"
```

Respuesta:
```json
{
  "success": true,
  "created": 3,
  "documents": [
    {"id": "doc-1", "title": "faq_velocidad.pdf", "is_indexed": true},
    {"id": "doc-2", "title": "guia_router.docx", "is_indexed": true},
    {"id": "doc-3", "title": "soluciones.txt", "is_indexed": true}
  ],
  "errors": []
}
```

---

### **Paso 3: Probar con el Bot**

Usuario en Telegram: `"¿Por qué mi internet está lento?"`

Bot:
1. Busca en ChromaDB
2. Encuentra `faq_velocidad.pdf` (indexado)
3. Usa ese contexto para responder
4. Responde: "Según nuestra documentación, las causas más comunes son..."

---

## 🛠️ **Script de Ejemplo para Indexar Múltiples Archivos**

```python
import os
import requests

# Configuración
API_URL = "http://localhost:9000/api/knowledge"
KB_ID = "tu-knowledge-base-id"
DOCS_FOLDER = "./documentos_soporte"

# Crear knowledge base si no existe
kb_response = requests.post(
    f"{API_URL}/knowledge-bases/",
    json={
        "title": "Soporte Técnico",
        "description": "Documentación de soporte",
        "category": "soporte",
        "is_public": True
    }
)
kb_id = kb_response.json()['id']

# Subir todos los archivos de una carpeta
files_to_upload = []
for filename in os.listdir(DOCS_FOLDER):
    if filename.endswith(('.pdf', '.docx', '.txt', '.md')):
        filepath = os.path.join(DOCS_FOLDER, filename)
        files_to_upload.append(('files', open(filepath, 'rb')))

# Subir en batch
response = requests.post(
    f"{API_URL}/documents/upload/",
    files=files_to_upload,
    data={
        'knowledge_base': kb_id,
        'auto_index': True,
        'category': 'soporte'
    }
)

print(f"✅ Subidos: {response.json()['created']} documentos")
print(f"❌ Errores: {len(response.json()['errors'])}")
```

---

## 📊 **Verificar Indexación**

```bash
# Ver documentos indexados
curl http://localhost:9000/api/knowledge/documents/ | jq '.[] | {title, is_indexed, indexed_at}'

# Ver estadísticas de ChromaDB
docker-compose exec web python manage.py vector_store_stats
```

---

## 🎯 **Casos de Uso**

### **1. Indexar FAQ de tu empresa**
```bash
curl -X POST .../upload/ \
  -F "files=@faq_internet.pdf" \
  -F "files=@faq_router.pdf" \
  -F "knowledge_base=kb-id"
```

### **2. Indexar manuales técnicos**
```bash
curl -X POST .../upload/ \
  -F "files=@manual_router_tp_link.pdf" \
  -F "files=@manual_modem.docx" \
  -F "knowledge_base=kb-id"
```

### **3. Indexar guías de solución**
```bash
curl -X POST .../upload/ \
  -F "files=@solucion_lentitud.txt" \
  -F "files=@solucion_cortes.md" \
  -F "knowledge_base=kb-id"
```

---

## ✅ **Ventajas de esta API**

1. **Automática**: Solo subes el archivo, todo lo demás es automático
2. **Múltiples formatos**: PDF, DOCX, TXT, MD
3. **Batch upload**: Sube varios archivos a la vez
4. **Auto-indexación**: Se indexa en ChromaDB automáticamente
5. **Metadata**: Puedes agregar categorías y metadata personalizada
6. **Re-indexación**: Puedes re-indexar documentos si los actualizas

---

## 🚀 **Próximos Pasos**

1. Crear una base de conocimiento
2. Subir tus documentos de soporte
3. Probar el bot con preguntas relacionadas
4. Ver cómo responde con contexto de tus documentos

---

**¿Listo para probar? Sube tus primeros documentos y el bot los usará automáticamente!** 🎉
