# Servicios de IA - KnoBot

## 📦 Estructura de Servicios AI

La infraestructura AI/RAG está implementada en `apps/ai/services/`:

### 1. **EmbeddingService** (`embedding_service.py`)
Genera embeddings (vectores) de texto usando Sentence Transformers.

**Características:**
- Modelo multilingüe optimizado para español: `paraphrase-multilingual-MiniLM-L12-v2`
- Dimensión de embeddings: 384
- Métodos principales:
  - `encode(texts)` - Vectoriza uno o más textos
  - `encode_query(query)` - Vectoriza una consulta
  - `similarity(emb1, emb2)` - Calcula similitud coseno

**Uso:**
```python
from apps.ai.services import EmbeddingService

embedding_service = EmbeddingService()
embedding = embedding_service.encode("¿Cómo configuro mi router?")
```

### 2. **VectorStore** (`vector_store.py`)
Gestiona la base de datos vectorial usando ChromaDB.

**Características:**
- Almacenamiento persistente en `./chroma_db`
- Búsqueda por similitud coseno
- Soporte para metadatos y filtros
- Métodos principales:
  - `add_documents()` - Agrega documentos
  - `search()` - Busca documentos similares
  - `update_document()` - Actualiza un documento
  - `delete_documents()` - Elimina documentos

**Uso:**
```python
from apps.ai.services import VectorStore

vector_store = VectorStore()
vector_store.add_documents(
    documents=["Texto del documento"],
    embeddings=[[0.1, 0.2, ...]],
    metadatas=[{"category": "soporte"}],
    ids=["doc-1"]
)
```

### 3. **RAGService** (`rag_service.py`)
Implementa Retrieval-Augmented Generation (RAG).

**Características:**
- Indexación de documentos con embeddings
- Búsqueda semántica de contexto
- Construcción de prompts con contexto
- Métodos principales:
  - `index_document()` - Indexa un documento
  - `retrieve_context()` - Recupera contexto relevante
  - `build_context_prompt()` - Construye prompt con contexto

**Uso:**
```python
from apps.ai.services import RAGService

rag_service = RAGService()

# Indexar documento
rag_service.index_document(
    document_id="doc-123",
    content="El router se configura desde 192.168.1.1",
    metadata={"category": "configuracion"}
)

# Buscar contexto
context = rag_service.retrieve_context(
    query="¿Cómo configuro mi router?",
    n_results=5
)
```

### 4. **ChatOrchestrator** (`chat_orchestrator.py`)
Orquestador principal que integra RAG con Gemini LLM.

**Características:**
- Integración con Google Gemini
- Soporte para RAG opcional
- Gestión de historial de conversación
- Métodos principales:
  - `process_message()` - Procesa mensaje y genera respuesta
  - `create_conversation()` - Crea nueva conversación
  - `end_conversation()` - Finaliza conversación

**Uso:**
```python
from apps.ai.services import ChatOrchestrator

orchestrator = ChatOrchestrator()

# Procesar mensaje con RAG
response = orchestrator.process_message(
    conversation_id="conv-123",
    user_message="¿Cómo reinicio mi router?",
    use_rag=True,
    n_context_docs=5
)

print(response['content'])  # Respuesta del asistente
print(response['context_used'])  # Número de documentos usados
```

### 5. **DocumentProcessor** (`document_processor.py`)
Procesa documentos de diferentes formatos.

**Características:**
- Soporta PDF, DOCX, TXT
- Extracción de texto
- División en chunks con overlap
- Métodos principales:
  - `process_document()` - Procesa documento según tipo
  - `chunk_text()` - Divide texto en chunks

**Uso:**
```python
from apps.ai.services import DocumentProcessor

processor = DocumentProcessor()

# Procesar PDF
text = processor.process_document(file_content, 'pdf')

# Dividir en chunks
chunks = processor.chunk_text(text, chunk_size=500, overlap=50)
```

## 🔄 Flujo de Trabajo Típico

### 1. Indexar Base de Conocimiento

```python
from apps.ai.services import RAGService, DocumentProcessor
from apps.knowledge.models import Document

rag_service = RAGService()
processor = DocumentProcessor()

# Obtener documentos de la base de datos
documents = Document.objects.filter(is_active=True)

for doc in documents:
    # Procesar si es archivo
    if doc.file_url:
        text = processor.process_document(doc.file_content, doc.file_type)
    else:
        text = doc.content
    
    # Dividir en chunks si es muy largo
    if len(text) > 1000:
        chunks = processor.chunk_text(text)
        for i, chunk in enumerate(chunks):
            rag_service.index_document(
                document_id=f"{doc.id}-chunk-{i}",
                content=chunk,
                metadata={
                    "document_id": str(doc.id),
                    "chunk_index": i,
                    "category": doc.knowledge_base.category
                }
            )
    else:
        rag_service.index_document(
            document_id=str(doc.id),
            content=text,
            metadata={"category": doc.knowledge_base.category}
        )
```

### 2. Procesar Chat con RAG

```python
from apps.ai.services import ChatOrchestrator

orchestrator = ChatOrchestrator()

# Usuario envía mensaje
response = orchestrator.process_message(
    conversation_id="conv-uuid",
    user_message="Mi internet está lento, ¿qué puedo hacer?",
    use_rag=True,
    n_context_docs=5
)

# Respuesta incluye:
# - content: Texto de la respuesta
# - tokens_used: Tokens consumidos
# - context_used: Documentos de contexto utilizados
```

### 3. Chat sin RAG (solo conversación)

```python
# Para conversaciones generales sin necesidad de base de conocimiento
response = orchestrator.process_message(
    conversation_id="conv-uuid",
    user_message="Hola, ¿cómo estás?",
    use_rag=False
)
```

## ⚙️ Configuración

### Variables de Entorno

```env
# .env
GEMINI_API_KEY=your-gemini-api-key-here
```

### Modelos

- **Embeddings:** `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensiones)
- **LLM:** Google Gemini Pro
- **Vector DB:** ChromaDB con DuckDB backend

## 📊 Próximos Pasos

1. **Management Commands:**
   - `python manage.py index_knowledge` - Indexar toda la base de conocimiento
   - `python manage.py clear_vector_store` - Limpiar base vectorial

2. **Endpoints REST:**
   - `POST /api/chat/` - Enviar mensaje
   - `POST /api/knowledge/index/` - Indexar documento
   - `GET /api/knowledge/search/` - Búsqueda semántica

3. **Optimizaciones:**
   - Cache de embeddings
   - Batch processing
   - Async processing con Celery

## 🧪 Testing

```python
# Test básico
from apps.ai.services import EmbeddingService, VectorStore, RAGService

# 1. Test embeddings
embedding_service = EmbeddingService()
emb = embedding_service.encode("Hola mundo")
assert emb.shape == (384,)

# 2. Test vector store
vector_store = VectorStore()
vector_store.add_documents(
    documents=["Test doc"],
    embeddings=[emb.tolist()],
    ids=["test-1"]
)
assert vector_store.count() > 0

# 3. Test RAG
rag_service = RAGService()
rag_service.index_document("test-2", "Documento de prueba")
results = rag_service.retrieve_context("prueba")
assert len(results) > 0
```
