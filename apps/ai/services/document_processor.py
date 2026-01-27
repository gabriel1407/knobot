from typing import List, Dict, Optional
import PyPDF2
import docx
from io import BytesIO
import openpyxl
from pptx import Presentation
from PIL import Image
import json
import csv


class DocumentProcessor:
    """
    Procesador de documentos para extraer texto de diferentes formatos.
    """
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extrae texto de un archivo PDF.
        
        Args:
            file_content: Contenido del archivo PDF en bytes.
            
        Returns:
            Texto extraído.
        """
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_parts = []
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
            
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Error al procesar PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extrae texto de un archivo DOCX.
        
        Args:
            file_content: Contenido del archivo DOCX en bytes.
            
        Returns:
            Texto extraído.
        """
        try:
            docx_file = BytesIO(file_content)
            doc = docx.Document(docx_file)
            
            text_parts = []
            for paragraph in doc.paragraphs:
                text_parts.append(paragraph.text)
            
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Error al procesar DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """
        Extrae texto de un archivo TXT.
        
        Args:
            file_content: Contenido del archivo TXT en bytes.
            
        Returns:
            Texto extraído.
        """
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1')
            except Exception as e:
                raise ValueError(f"Error al procesar TXT: {str(e)}")
    
    @classmethod
    def process_document(
        cls,
        file_content: bytes,
        file_type: str
    ) -> str:
        """
        Procesa un documento según su tipo.
        
        Args:
            file_content: Contenido del archivo en bytes.
            file_type: Tipo de archivo ('pdf', 'docx', 'txt', 'xlsx', 'pptx', 'csv', 'json', 'jpg', 'png').
            
        Returns:
            Texto extraído.
        """
        processors = {
            'pdf': cls.extract_text_from_pdf,
            'docx': cls.extract_text_from_docx,
            'doc': cls.extract_text_from_docx,
            'txt': cls.extract_text_from_txt,
            'xlsx': cls.extract_text_from_excel,
            'xls': cls.extract_text_from_excel,
            'pptx': cls.extract_text_from_powerpoint,
            'ppt': cls.extract_text_from_powerpoint,
            'csv': cls.extract_text_from_csv,
            'json': cls.extract_text_from_json,
            'jpg': cls.extract_metadata_from_image,
            'jpeg': cls.extract_metadata_from_image,
            'png': cls.extract_metadata_from_image,
            'gif': cls.extract_metadata_from_image,
            'bmp': cls.extract_metadata_from_image,
        }
        
        processor = processors.get(file_type.lower())
        if not processor:
            raise ValueError(f"Tipo de archivo no soportado: {file_type}")
        
        return processor(file_content)
    
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """
        Divide un texto largo en chunks más pequeños con overlap.
        
        Args:
            text: Texto a dividir.
            chunk_size: Tamaño de cada chunk en caracteres.
            overlap: Número de caracteres de overlap entre chunks.
            
        Returns:
            Lista de chunks de texto.
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Intentar cortar en un punto natural (espacio, punto, etc.)
            if end < len(text):
                last_space = chunk.rfind(' ')
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                
                cut_point = max(last_space, last_period, last_newline)
                if cut_point > chunk_size * 0.7:  # Solo si no está muy atrás
                    chunk = chunk[:cut_point + 1]
                    end = start + len(chunk)
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
