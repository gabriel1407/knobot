# Importar servicios core de RAG
try:
    from .embedding_service import EmbeddingService
    from .vector_store import VectorStore
    from .rag_service import RAGService
    from .chat_orchestrator import ChatOrchestrator
    RAG_AVAILABLE = True
except ImportError as e:
    import warnings
    warnings.warn(f"RAG services not available: {e}. Install: pip install sentence-transformers chromadb")
    
    class EmbeddingService:
        def __init__(self, *args, **kwargs):
            raise ImportError("RAG dependencies not installed. Run: pip install sentence-transformers chromadb")
    
    class VectorStore:
        def __init__(self, *args, **kwargs):
            raise ImportError("RAG dependencies not installed. Run: pip install sentence-transformers chromadb")
    
    class RAGService:
        def __init__(self, *args, **kwargs):
            raise ImportError("RAG dependencies not installed. Run: pip install sentence-transformers chromadb")
    
    class ChatOrchestrator:
        def __init__(self, *args, **kwargs):
            raise ImportError("RAG dependencies not installed. Run: pip install sentence-transformers chromadb")
    
    RAG_AVAILABLE = False

# Importar procesadores de archivos (opcionales)
try:
    from .document_processor import DocumentProcessor
    from .file_processor import FileProcessor
    PROCESSORS_AVAILABLE = True
except ImportError:
    class DocumentProcessor:
        def __init__(self, *args, **kwargs):
            raise ImportError("Document processors not installed. Run: pip install PyPDF2 python-docx openpyxl python-pptx")
    
    class FileProcessor:
        def __init__(self, *args, **kwargs):
            raise ImportError("File processors not installed. Run: pip install PyPDF2 python-docx openpyxl python-pptx")
    
    PROCESSORS_AVAILABLE = False

# Importar procesador de audio (opcional)
try:
    from .audio_processor import AudioProcessor
    AUDIO_AVAILABLE = True
except ImportError:
    class AudioProcessor:
        def __init__(self, *args, **kwargs):
            raise ImportError("Audio processor not installed. Run: pip install pydub SpeechRecognition")
    
    AUDIO_AVAILABLE = False

__all__ = [
    'EmbeddingService',
    'VectorStore',
    'RAGService',
    'ChatOrchestrator',
    'DocumentProcessor',
    'AudioProcessor',
    'FileProcessor',
    'RAG_AVAILABLE',
    'PROCESSORS_AVAILABLE',
    'AUDIO_AVAILABLE',
]
