"""
Utilidades para procesar archivos y extraer texto.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def extract_text_from_file(file) -> Optional[str]:
    """
    Extrae texto de diferentes tipos de archivos.
    
    Args:
        file: Archivo Django UploadedFile
        
    Returns:
        Texto extraído o None si falla
    """
    try:
        file_type = file.content_type
        
        # Texto plano
        if file_type == 'text/plain' or file_type == 'text/markdown':
            return file.read().decode('utf-8')
        
        # PDF
        elif file_type == 'application/pdf':
            try:
                from PyPDF2 import PdfReader
                import io
                
                pdf_file = io.BytesIO(file.read())
                reader = PdfReader(pdf_file)
                
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                
                return '\n'.join(text)
            except Exception as e:
                logger.error(f"Error extrayendo texto de PDF: {e}")
                return None
        
        # DOCX
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            try:
                from docx import Document
                import io
                
                docx_file = io.BytesIO(file.read())
                doc = Document(docx_file)
                
                text = []
                for paragraph in doc.paragraphs:
                    text.append(paragraph.text)
                
                return '\n'.join(text)
            except Exception as e:
                logger.error(f"Error extrayendo texto de DOCX: {e}")
                return None
        
        # DOC (más difícil, requiere antiword o similar)
        elif file_type == 'application/msword':
            logger.warning("Archivos .doc no soportados directamente. Convierte a .docx")
            return None
        
        else:
            logger.warning(f"Tipo de archivo no soportado: {file_type}")
            return None
            
    except Exception as e:
        logger.error(f"Error procesando archivo: {e}")
        return None


def get_file_type(file) -> str:
    """Obtiene el tipo de archivo de forma legible."""
    content_type = file.content_type
    
    type_map = {
        'text/plain': 'txt',
        'text/markdown': 'md',
        'application/pdf': 'pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/msword': 'doc',
    }
    
    return type_map.get(content_type, 'unknown')
