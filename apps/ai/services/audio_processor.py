from typing import Optional
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
import tempfile


class AudioProcessor:
    """
    Procesador de archivos de audio para transcripción a texto.
    """
    
    def __init__(self):
        """
        Inicializa el procesador de audio.
        """
        self.recognizer = sr.Recognizer()
    
    @staticmethod
    def convert_to_wav(file_content: bytes, source_format: str) -> bytes:
        """
        Convierte un archivo de audio a formato WAV.
        
        Args:
            file_content: Contenido del archivo de audio en bytes.
            source_format: Formato del archivo fuente ('mp3', 'ogg', 'm4a', etc.).
            
        Returns:
            Contenido del archivo WAV en bytes.
        """
        try:
            # Cargar audio desde bytes
            audio_file = BytesIO(file_content)
            audio = AudioSegment.from_file(audio_file, format=source_format)
            
            # Convertir a WAV
            wav_buffer = BytesIO()
            audio.export(wav_buffer, format='wav')
            wav_buffer.seek(0)
            
            return wav_buffer.read()
        except Exception as e:
            raise ValueError(f"Error al convertir audio a WAV: {str(e)}")
    
    def transcribe_audio(
        self,
        file_content: bytes,
        file_format: str = 'wav',
        language: str = 'es-ES'
    ) -> str:
        """
        Transcribe un archivo de audio a texto usando Google Speech Recognition.
        
        Args:
            file_content: Contenido del archivo de audio en bytes.
            file_format: Formato del archivo ('wav', 'mp3', 'ogg', 'm4a').
            language: Código de idioma para la transcripción (default: español).
            
        Returns:
            Texto transcrito del audio.
        """
        try:
            # Convertir a WAV si no lo es
            if file_format.lower() != 'wav':
                wav_content = self.convert_to_wav(file_content, file_format)
            else:
                wav_content = file_content
            
            # Crear archivo temporal para procesamiento
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(wav_content)
                temp_path = temp_file.name
            
            try:
                # Cargar audio con speech_recognition
                with sr.AudioFile(temp_path) as source:
                    audio_data = self.recognizer.record(source)
                
                # Transcribir usando Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio_data,
                    language=language
                )
                
                return text
            finally:
                # Limpiar archivo temporal
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        except sr.UnknownValueError:
            return "No se pudo entender el audio"
        except sr.RequestError as e:
            raise ValueError(f"Error en el servicio de transcripción: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error al transcribir audio: {str(e)}")
    
    def transcribe_audio_chunks(
        self,
        file_content: bytes,
        file_format: str = 'wav',
        chunk_duration_ms: int = 60000,
        language: str = 'es-ES'
    ) -> str:
        """
        Transcribe archivos de audio largos dividiéndolos en chunks.
        
        Args:
            file_content: Contenido del archivo de audio en bytes.
            file_format: Formato del archivo.
            chunk_duration_ms: Duración de cada chunk en milisegundos (default: 60s).
            language: Código de idioma para la transcripción.
            
        Returns:
            Texto transcrito completo.
        """
        try:
            # Cargar audio
            audio_file = BytesIO(file_content)
            audio = AudioSegment.from_file(audio_file, format=file_format)
            
            # Dividir en chunks
            chunks = []
            for i in range(0, len(audio), chunk_duration_ms):
                chunk = audio[i:i + chunk_duration_ms]
                chunks.append(chunk)
            
            # Transcribir cada chunk
            transcriptions = []
            for i, chunk in enumerate(chunks):
                # Exportar chunk a WAV
                chunk_buffer = BytesIO()
                chunk.export(chunk_buffer, format='wav')
                chunk_buffer.seek(0)
                
                # Transcribir chunk
                try:
                    chunk_text = self.transcribe_audio(
                        chunk_buffer.read(),
                        file_format='wav',
                        language=language
                    )
                    transcriptions.append(chunk_text)
                except Exception as e:
                    transcriptions.append(f"[Error en chunk {i+1}: {str(e)}]")
            
            return " ".join(transcriptions)
        
        except Exception as e:
            raise ValueError(f"Error al transcribir audio en chunks: {str(e)}")
    
    def get_audio_metadata(self, file_content: bytes, file_format: str) -> dict:
        """
        Obtiene metadatos de un archivo de audio.
        
        Args:
            file_content: Contenido del archivo de audio en bytes.
            file_format: Formato del archivo.
            
        Returns:
            Diccionario con metadatos del audio.
        """
        try:
            audio_file = BytesIO(file_content)
            audio = AudioSegment.from_file(audio_file, format=file_format)
            
            return {
                'duration_seconds': len(audio) / 1000.0,
                'channels': audio.channels,
                'sample_width': audio.sample_width,
                'frame_rate': audio.frame_rate,
                'frame_width': audio.frame_width,
                'format': file_format
            }
        except Exception as e:
            raise ValueError(f"Error al obtener metadatos de audio: {str(e)}")
    
    @classmethod
    def process_audio_file(
        cls,
        file_content: bytes,
        file_format: str,
        language: str = 'es-ES',
        max_duration_seconds: int = 300
    ) -> dict:
        """
        Procesa un archivo de audio completo y retorna transcripción y metadatos.
        
        Args:
            file_content: Contenido del archivo de audio en bytes.
            file_format: Formato del archivo.
            language: Idioma para transcripción.
            max_duration_seconds: Duración máxima para procesar (default: 5 min).
            
        Returns:
            Diccionario con transcripción y metadatos.
        """
        processor = cls()
        
        # Obtener metadatos
        metadata = processor.get_audio_metadata(file_content, file_format)
        
        # Verificar duración
        if metadata['duration_seconds'] > max_duration_seconds:
            # Usar chunks para archivos largos
            transcription = processor.transcribe_audio_chunks(
                file_content,
                file_format,
                language=language
            )
        else:
            # Transcribir directamente
            transcription = processor.transcribe_audio(
                file_content,
                file_format,
                language=language
            )
        
        return {
            'transcription': transcription,
            'metadata': metadata,
            'language': language
        }
