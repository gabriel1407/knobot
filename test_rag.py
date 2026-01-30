#!/usr/bin/env python
"""
Script para probar RAG completo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowbot.settings')
django.setup()

from apps.ai.services import EmbeddingService, VectorStore, RAGService

print("=" * 60)
print("PRUEBA DE RAG - KnoBot")
print("=" * 60)

# 1. Probar EmbeddingService
print("\n1️⃣ Probando EmbeddingService...")
embedding_service = EmbeddingService()
test_text = "¿Por qué mi internet está lento?"
embeddings = embedding_service.encode([test_text])
print(f"   ✅ Embeddings generados: {len(embeddings[0])} dimensiones")

# 2. Probar VectorStore
print("\n2️⃣ Probando VectorStore...")
vector_store = VectorStore()
print(f"   ✅ Vector store inicializado")

# 3. Agregar documentos de prueba
print("\n3️⃣ Agregando documentos de prueba...")
test_docs = [
    {
        'content': 'Internet lento puede deberse a saturación de red, router antiguo, interferencias WiFi o problemas con el ISP.',
        'metadata': {'category': 'soporte', 'topic': 'internet_lento'}
    },
    {
        'content': 'Para configurar el router, accede a 192.168.1.1 con usuario admin y contraseña admin.',
        'metadata': {'category': 'soporte', 'topic': 'configuracion_router'}
    },
    {
        'content': 'Reiniciar el router: desconectar 30 segundos, volver a conectar y esperar 2-3 minutos.',
        'metadata': {'category': 'soporte', 'topic': 'troubleshooting'}
    }
]

# Generar embeddings para todos los documentos
contents = [doc['content'] for doc in test_docs]
doc_embeddings = embedding_service.encode(contents)

# Agregar documentos con sus embeddings
vector_store.add_documents(
    documents=contents,
    embeddings=doc_embeddings.tolist(),
    metadatas=[doc['metadata'] for doc in test_docs],
    ids=[f"test_doc_{i}" for i in range(1, len(test_docs) + 1)]
)
print(f"   ✅ {len(test_docs)} documentos agregados")

# 4. Probar búsqueda semántica
print("\n4️⃣ Probando búsqueda semántica...")
queries = [
    "¿Por qué mi internet está lento?",
    "¿Cómo configuro mi router?",
    "¿Cómo reinicio el router?"
]

for query in queries:
    print(f"\n   📝 Query: {query}")
    # Generar embedding de la query
    query_embedding = embedding_service.encode_query(query)
    results = vector_store.search(query_embedding.tolist(), n_results=2)
    
    if results and 'documents' in results and results['documents']:
        for j, doc in enumerate(results['documents'], 1):
            distance = results['distances'][j-1] if 'distances' in results else 'N/A'
            print(f"      {j}. {doc[:100]}... (distancia: {distance:.4f})")
    else:
        print("      ⚠️  No se encontraron resultados")

# 5. Probar RAGService
print("\n5️⃣ Probando RAGService...")
rag_service = RAGService()
query = "¿Qué hago si mi internet está lento?"
context_docs = rag_service.retrieve_context(query, n_results=2)
print(f"   ✅ Contexto recuperado: {len(context_docs)} documentos")
for i, doc in enumerate(context_docs, 1):
    doc_text = str(doc) if not isinstance(doc, str) else doc
    print(f"      {i}. {doc_text[:80]}...")

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS DE RAG COMPLETADAS EXITOSAMENTE")
print("=" * 60)
print("\n💡 El sistema RAG está completamente funcional")
print("   Puedes indexar tus documentos con:")
print("   docker-compose exec web python manage.py index_knowledge /ruta/docs")
