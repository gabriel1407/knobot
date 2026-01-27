from typing import Dict, Optional
from .document_processor import DocumentProcessor
from .audio_processor import AudioProcessor


class FileProcessor:
    """
    Procesador unificado para todos los tipos de archivos.
    Determina automáticamente el tipo y usa el procesador apropiado.
    """
    
    # Mapeo de extensiones a categorías
    DOCUMENT_FORMATS = ['pdf', 'docx', 'doc', 'txt', 'xlsx', 'xls', 'pptx', 'ppt', 'csv', 'json']
    IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
    AUDIO_FORMATS = ['mp3', 'wav', 'ogg', 'm4a', 'flac', 'aac', 'wma']
    VIDEO_FORMATS = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']
    
    def __init__(self):
        """
        Inicializa el procesador de archivos.
        """
        self.document_processor = DocumentProcessor()
        self.audio_processor = AudioProcessor()
    
    @classmethod
    def get_file_category(cls, file_extension: str) -> str:
        """
        Determina la categoría de un archivo por su extensión.
        
        Args:
            file_extension: Extensión del archivo (sin punto).
            
        Returns:
            Categoría del archivo: 'document', 'image', 'audio', 'video', 'unknown'.
        """
        ext = file_extension.lower()
        
        if ext in cls.DOCUMENT_FORMATS:
            return 'document'
        elif ext in cls.IMAGE_FORMATS:
            return 'image'
        elif ext in cls.AUDIO_FORMATS:
            return 'audio'
        elif ext in cls.VIDEO_FORMATS:
            return 'video'
        else:
            return 'unknown'
    
    def process_file(
        self,
        file_content: bytes,
        file_extension: str,
        language: str = 'es-ES'
    ) -> Dict:
        """
        Procesa un archivo automáticamente según su tipo.
        
        Args:
            file_content: Contenido del archivo en bytes.
            file_extension: Extensión del archivo (sin punto).
            language: Idioma para procesamiento de audio.
            
        Returns:
            Diccionario con el texto extraído y metadatos.
        """
        category = self.get_file_category(file_extension)
        
        try:
            if category == 'document' or category == 'image':
                # Procesar documentos e imágenes
                text = self.document_processor.process_document(
                    file_content,
                    file_extension
                )
                return {
                    'text': text,
                    'category': category,
                    'format': file_extension,
                    'success': True
                }
            
            elif category == 'audio':
                # Procesar audio
                result = self.audio_processor.process_audio_file(
                    file_content,
                    file_extension,
                    language=language
                )
                return {
                    'text': result['transcription'],
                    'category': category,
                    'format': file_extension,
                    'metadata': result['metadata'],
                    'success': True
                }
            
            elif category == 'video':
                # TODO: Implementar extracción de audio de video
                return {
                    'text': f"Archivo de video ({file_extension}). Extracción de audio no implementada aún.",
                    'category': category,
                    'format': file_extension,
                    'success': False,
                    'error': 'Video processing not implemented'
                }
            
            else:
                return {
                    'text': f"Tipo de archivo no soportado: {file_extension}",
                    'category': 'unknown',
                    'format': file_extension,
                    'success': False,
                    'error': 'Unsupported file type'
                }
        
        except Exception as e:
            return {
                'text': '',
                'category': category,
                'format': file_extension,
                'success': False,
                'error': str(e)
            }
    
    def process_and_chunk(
        self,
        file_content: bytes,
        file_extension: str,
        chunk_size: int = 500,
        overlap: int = 50,
        language: str = 'es-ES'
    ) -> Dict:
        """
        Procesa un archivo y divide el texto en chunks.
        
        Args:
            file_content: Contenido del archivo en bytes.
            file_extension: Extensión del archivo.
            chunk_size: Tamaño de cada chunk.
            overlap: Overlap entre chunks.
            language: Idioma para audio.
            
        Returns:
            Diccionario con chunks y metadatos.
        """
        # Procesar archivo
        result = self.process_file(file_content, file_extension, language)
        
        if not result['success']:
            return result
        
        # Dividir en chunks si el texto es largo
        text = result['text']
        if len(text) > chunk_size:
            chunks = self.document_processor.chunk_text(
                text,
                chunk_size=chunk_size,
                overlap=overlap
            )
        else:
            chunks = [text]
        
        result['chunks'] = chunks
        result['num_chunks'] = len(chunks)
        
        return result
    
    @staticmethod
    def get_supported_formats() -> Dict[str, list]:
        """
        Retorna todos los formatos soportados por categoría.
        
        Returns:
            Diccionario con formatos soportados.
        """
        return {
            'documents': FileProcessor.DOCUMENT_FORMATS,
            'images': FileProcessor.IMAGE_FORMATS,
            'audio': FileProcessor.AUDIO_FORMATS,
            'video': FileProcessor.VIDEO_FORMATS
        }
    
    @staticmethod
    def is_supported(file_extension: str) -> bool:
        """
        Verifica si un formato de archivo está soportado.
        
        Args:
            file_extension: Extensión del archivo.
            
        Returns:
            True si está soportado, False en caso contrario.
        """
        category = FileProcessor.get_file_category(file_extension)
        return category != 'unknown'
