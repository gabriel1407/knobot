from typing import List, Dict, Optional
from .embedding_service import EmbeddingService
from .vector_store import VectorStore


class RAGService:
    """
    Servicio de Retrieval-Augmented Generation (RAG).
    Combina búsqueda semántica con generación de respuestas.
    """
    
    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        vector_store: Optional[VectorStore] = None
    ):
        """
        Inicializa el servicio RAG.
        
        Args:
            embedding_service: Servicio de embeddings.
            vector_store: Base de datos vectorial.
        """
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store = vector_store or VectorStore()
    
    def index_document(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Indexa un documento en la base vectorial.
        
        Args:
            document_id: ID del documento.
            content: Contenido del documento.
            metadata: Metadatos adicionales.
            
        Returns:
            ID del documento indexado.
        """
        embedding = self.embedding_service.encode(content)
        
        self.vector_store.add_documents(
            documents=[content],
            embeddings=[embedding.tolist()],
            metadatas=[metadata or {}],
            ids=[document_id]
        )
        
        return document_id
    
    def index_documents_batch(
        self,
        documents: List[Dict[str, any]]
    ) -> List[str]:
        """
        Indexa múltiples documentos en batch.
        
        Args:
            documents: Lista de diccionarios con 'id', 'content' y 'metadata'.
            
        Returns:
            Lista de IDs de documentos indexados.
        """
        contents = [doc['content'] for doc in documents]
        embeddings = self.embedding_service.encode_documents(contents)
        
        ids = [doc['id'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]
        
        self.vector_store.add_documents(
            documents=contents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def retrieve_context(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Recupera contexto relevante para una consulta.
        
        Args:
            query: Consulta del usuario.
            n_results: Número de documentos a recuperar.
            filters: Filtros opcionales de metadatos.
            
        Returns:
            Lista de documentos relevantes con sus scores.
        """
        # Ajustar n_results según documentos disponibles
        try:
            total_docs = self.vector_store.collection.count()
            n_results = min(n_results, total_docs) if total_docs > 0 else n_results
        except:
            pass  # Si falla, usar n_results original
        
        query_embedding = self.embedding_service.encode_query(query)
        
        results = self.vector_store.search(
            query_embedding=query_embedding.tolist(),
            n_results=n_results,
            where=filters
        )
        
        context_docs = []
        for i, doc in enumerate(results['documents']):
            context_docs.append({
                'content': doc,
                'score': 1 - results['distances'][i],  # Convertir distancia a similitud
                'metadata': results['metadatas'][i],
                'id': results['ids'][i]
            })
        
        return context_docs
    
    def build_context_prompt(
        self,
        query: str,
        context_docs: List[Dict],
        max_context_length: int = 2000
    ) -> str:
        """
        Construye un prompt con contexto para el LLM.
        
        Args:
            query: Consulta del usuario.
            context_docs: Documentos de contexto recuperados.
            max_context_length: Longitud máxima del contexto.
            
        Returns:
            Prompt formateado con contexto.
        """
        context_parts = []
        current_length = 0
        
        for doc in context_docs:
            content = doc['content']
            if current_length + len(content) > max_context_length:
                break
            context_parts.append(f"- {content}")
            current_length += len(content)
        
        context = "\n".join(context_parts)
        
        prompt = f"""Contexto relevante:
{context}

Pregunta del usuario: {query}

Por favor, responde la pregunta usando el contexto proporcionado. Si el contexto no contiene información suficiente, indícalo claramente."""
        
        return prompt
    
    def delete_document(self, document_id: str) -> None:
        """
        Elimina un documento de la base vectorial.
        
        Args:
            document_id: ID del documento a eliminar.
        """
        self.vector_store.delete_documents([document_id])
    
    def update_document(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Actualiza un documento en la base vectorial.
        
        Args:
            document_id: ID del documento.
            content: Nuevo contenido.
            metadata: Nuevos metadatos.
        """
        embedding = self.embedding_service.encode(content)
        
        self.vector_store.update_document(
            id=document_id,
            document=content,
            embedding=embedding.tolist(),
            metadata=metadata
        )
