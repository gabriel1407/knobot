import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from django.conf import settings


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
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
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
        
        Args:
            documents: Lista de textos de documentos.
            embeddings: Lista de embeddings correspondientes.
            metadatas: Metadatos opcionales para cada documento.
            ids: IDs opcionales para cada documento.
            
        Returns:
            Lista de IDs de los documentos agregados.
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
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
