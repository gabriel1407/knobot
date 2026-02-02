import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from django.conf import settings

# Importar configuración para silenciar warnings de ChromaDB
try:
    from . import chromadb_config
except ImportError:
    pass

class VectorStore:
    """
    Servicio para gestionar la base de datos vectorial usando ChromaDB.
    """
    
    def __init__(self, collection_name: str = "knowbot_knowledge"):
        """
        Inicializa el vector store.
        
        Args:
            collection_name: Nombre de la colección en ChromaDB.
        """
        # Usar la nueva API de ChromaDB con telemetría desactivada
        from chromadb.config import Settings
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Agrega documentos a la base vectorial.
        Verifica IDs existentes para evitar duplicados.
        
        Args:
            documents: Lista de documentos.
            embeddings: Lista de embeddings.
            metadatas: Metadatos opcionales.
            ids: IDs opcionales para los documentos.
            
        Returns:
            Lista de IDs de los documentos agregados.
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        # Verificar IDs existentes para evitar warnings
        try:
            existing = self.collection.get(ids=ids)
            existing_ids = set(existing['ids']) if existing and 'ids' in existing else set()
        except:
            existing_ids = set()
        
        # Filtrar solo documentos nuevos
        new_docs = []
        new_embeddings = []
        new_metadatas = []
        new_ids = []
        
        for doc, emb, meta, id in zip(documents, embeddings, metadatas, ids):
            if id not in existing_ids:
                new_docs.append(doc)
                new_embeddings.append(emb)
                new_metadatas.append(meta)
                new_ids.append(id)
        
        # Solo agregar si hay documentos nuevos
        if new_ids:
            self.collection.add(
                documents=new_docs,
                embeddings=new_embeddings,
                metadatas=new_metadatas,
                ids=new_ids
            )
        
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """
        Busca documentos similares a un embedding de consulta.
        
        Args:
            query_embedding: Embedding de la consulta.
            n_results: Número de resultados a retornar.
            where: Filtros opcionales de metadatos.
            
        Returns:
            Diccionario con documentos, distancias y metadatos.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'distances': results['distances'][0] if results['distances'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'ids': results['ids'][0] if results['ids'] else []
        }
    
    def delete_documents(self, ids: List[str]) -> None:
        """
        Elimina documentos de la base vectorial.
        
        Args:
            ids: Lista de IDs de documentos a eliminar.
        """
        self.collection.delete(ids=ids)
    
    def update_document(
        self,
        id: str,
        document: Optional[str] = None,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Actualiza un documento en la base vectorial.
        
        Args:
            id: ID del documento a actualizar.
            document: Nuevo texto del documento.
            embedding: Nuevo embedding.
            metadata: Nuevos metadatos.
        """
        self.collection.update(
            ids=[id],
            documents=[document] if document else None,
            embeddings=[embedding] if embedding else None,
            metadatas=[metadata] if metadata else None
        )
    
    def count(self) -> int:
        """
        Retorna el número de documentos en la colección.
        
        Returns:
            Número de documentos.
        """
        return self.collection.count()
    
    def clear(self) -> None:
        """
        Elimina todos los documentos de la colección.
        """
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
