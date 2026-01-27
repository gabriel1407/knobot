from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np


class EmbeddingService:
    """
    Servicio para generar embeddings de texto usando Sentence Transformers.
    """
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Inicializa el servicio de embeddings.
        
        Args:
            model_name: Nombre del modelo de Sentence Transformers.
                       Por defecto usa un modelo multilingüe optimizado para español.
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Genera embeddings para uno o más textos.
        
        Args:
            texts: Texto o lista de textos a vectorizar.
            
        Returns:
            Array de embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        
        return embeddings
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Genera embedding para una consulta de búsqueda.
        
        Args:
            query: Texto de la consulta.
            
        Returns:
            Embedding de la consulta.
        """
        return self.encode(query)[0]
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """
        Genera embeddings para múltiples documentos.
        
        Args:
            documents: Lista de documentos.
            
        Returns:
            Array de embeddings.
        """
        return self.encode(documents)
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calcula la similitud coseno entre dos embeddings.
        
        Args:
            embedding1: Primer embedding.
            embedding2: Segundo embedding.
            
        Returns:
            Similitud coseno entre 0 y 1.
        """
        return float(np.dot(embedding1, embedding2) / 
                    (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
