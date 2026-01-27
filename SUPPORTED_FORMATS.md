# Formatos de Archivos Soportados - KnoBot

## 📄 Documentos

| Formato | Extensión | Procesador | Estado |
|---------|-----------|------------|--------|
| PDF | `.pdf` | DocumentProcessor | ✅ Completo |
| Word | `.docx`, `.doc` | DocumentProcessor | ✅ Completo |
| Excel | `.xlsx`, `.xls` | DocumentProcessor | ✅ Completo |
| PowerPoint | `.pptx`, `.ppt` | DocumentProcessor | ✅ Completo |
| Texto plano | `.txt` | DocumentProcessor | ✅ Completo |
| CSV | `.csv` | DocumentProcessor | ✅ Completo |
| JSON | `.json` | DocumentProcessor | ✅ Completo |

## 🖼️ Imágenes

| Formato | Extensión | Procesador | Estado |
|---------|-----------|------------|--------|
| JPEG | `.jpg`, `.jpeg` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |
| PNG | `.png` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |
| GIF | `.gif` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |
| BMP | `.bmp` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |
| WebP | `.webp` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |
| SVG | `.svg` | DocumentProcessor | ⚠️ Metadatos (OCR pendiente) |

**Nota:** Actualmente extrae metadatos de imágenes. OCR (extracción de texto) se puede agregar con `pytesseract`.

## 🎵 Audio

| Formato | Extensión | Procesador | Estado |
|---------|-----------|------------|--------|
| WAV | `.wav` | AudioProcessor | ✅ Transcripción completa |
| MP3 | `.mp3` | AudioProcessor | ✅ Transcripción completa |
| OGG | `.ogg` | AudioProcessor | ✅ Transcripción completa |
| M4A | `.m4a` | AudioProcessor | ✅ Transcripción completa |
| FLAC | `.flac` | AudioProcessor | ✅ Transcripción completa |
| AAC | `.aac` | AudioProcessor | ✅ Transcripción completa |
| WMA | `.wma` | AudioProcessor | ✅ Transcripción completa |

**Características:**
- Transcripción automática a texto usando Google Speech Recognition
- Soporte para archivos largos (división en chunks)
- Multiidioma (español por defecto)
- Extracción de metadatos (duración, canales, etc.)

## 🎬 Video

| Formato | Extensión | Procesador | Estado |
|---------|-----------|------------|--------|
| MP4 | `.mp4` | - | 🚧 Pendiente |
| AVI | `.avi` | - | 🚧 Pendiente |
| MOV | `.mov` | - | 🚧 Pendiente |
| WMV | `.wmv` | - | 🚧 Pendiente |
| FLV | `.flv` | - | 🚧 Pendiente |
| MKV | `.mkv` | - | 🚧 Pendiente |

**Nota:** Extracción de audio de video pendiente de implementación.

---

## 🔧 Uso del FileProcessor

### Procesamiento Automático

```python
from apps.ai.services import FileProcessor

processor = FileProcessor()

# Procesar cualquier archivo automáticamente
result = processor.process_file(
    file_content=file_bytes,
    file_extension='pdf',  # o 'mp3', 'xlsx', etc.
    language='es-ES'  # para audio
)

print(result['text'])  # Texto extraído
print(result['category'])  # 'document', 'audio', 'image', etc.
print(result['success'])  # True/False
```

### Procesamiento con Chunking

```python
# Para archivos grandes, divide el texto en chunks
result = processor.process_and_chunk(
    file_content=file_bytes,
    file_extension='pdf',
    chunk_size=500,
    overlap=50
)

for i, chunk in enumerate(result['chunks']):
    print(f"Chunk {i+1}: {chunk[:100]}...")
```

### Verificar Formato Soportado

```python
# Verificar si un formato está soportado
is_supported = FileProcessor.is_supported('mp3')  # True

# Obtener todos los formatos soportados
formats = FileProcessor.get_supported_formats()
print(formats['audio'])  # ['mp3', 'wav', 'ogg', ...]
```

---

## 📊 Procesadores Específicos

### DocumentProcessor

```python
from apps.ai.services import DocumentProcessor

processor = DocumentProcessor()

# PDF
text = processor.extract_text_from_pdf(pdf_bytes)

# Word
text = processor.extract_text_from_docx(docx_bytes)

# Excel
text = processor.extract_text_from_excel(xlsx_bytes)

# PowerPoint
text = processor.extract_text_from_powerpoint(pptx_bytes)

# CSV
text = processor.extract_text_from_csv(csv_bytes)

# JSON
text = processor.extract_text_from_json(json_bytes)

# Imagen (metadatos)
text = processor.extract_metadata_from_image(jpg_bytes)
```

### AudioProcessor

```python
from apps.ai.services import AudioProcessor

processor = AudioProcessor()

# Transcribir audio
transcription = processor.transcribe_audio(
    file_content=audio_bytes,
    file_format='mp3',
    language='es-ES'
)

# Para archivos largos (>5 min)
transcription = processor.transcribe_audio_chunks(
    file_content=audio_bytes,
    file_format='mp3',
    chunk_duration_ms=60000  # 60 segundos por chunk
)

# Obtener metadatos
metadata = processor.get_audio_metadata(audio_bytes, 'mp3')
print(metadata['duration_seconds'])
print(metadata['channels'])
```

---

## 🔄 Integración con RAG

```python
from apps.ai.services import RAGService, FileProcessor

rag_service = RAGService()
file_processor = FileProcessor()

# Procesar y indexar cualquier archivo
result = file_processor.process_and_chunk(
    file_content=file_bytes,
    file_extension='mp3',  # o cualquier formato soportado
    chunk_size=500
)

if result['success']:
    # Indexar cada chunk
    for i, chunk in enumerate(result['chunks']):
        rag_service.index_document(
            document_id=f"doc-{doc_id}-chunk-{i}",
            content=chunk,
            metadata={
                'format': result['format'],
                'category': result['category'],
                'chunk_index': i
            }
        )
```

---

## 🎯 Próximas Mejoras

### OCR para Imágenes
```bash
# Agregar a requirements
pip install pytesseract
```

```python
# Implementar en DocumentProcessor
import pytesseract
from PIL import Image

def extract_text_from_image_ocr(file_content: bytes) -> str:
    image = Image.open(BytesIO(file_content))
    text = pytesseract.image_to_string(image, lang='spa')
    return text
```

### Extracción de Audio de Video
```bash
# Agregar a requirements
pip install moviepy
```

```python
# Implementar VideoProcessor
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_bytes: bytes) -> bytes:
    # Extraer audio y convertir a formato procesable
    pass
```

---

## 📝 Dependencias Requeridas

```txt
# Documentos
PyPDF2==3.0.1
python-docx==1.1.0
openpyxl==3.1.2
python-pptx==0.6.23

# Imágenes
Pillow==10.1.0

# Audio
pydub==0.25.1
SpeechRecognition==3.10.1

# Utilidades
python-magic==0.4.27
```

---

## ⚙️ Configuración

### Variables de Entorno

No se requieren variables adicionales. El AudioProcessor usa Google Speech Recognition (gratuito con límites).

### Requisitos del Sistema

Para procesamiento de audio, se requiere `ffmpeg`:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Docker (ya incluido en Dockerfile.dev)
RUN apt-get install -y ffmpeg
```

---

## 🧪 Testing

```python
# Test completo de formatos
from apps.ai.services import FileProcessor

processor = FileProcessor()

# Test documento
with open('test.pdf', 'rb') as f:
    result = processor.process_file(f.read(), 'pdf')
    assert result['success'] == True

# Test audio
with open('test.mp3', 'rb') as f:
    result = processor.process_file(f.read(), 'mp3', language='es-ES')
    assert result['success'] == True
    assert len(result['text']) > 0

# Test imagen
with open('test.jpg', 'rb') as f:
    result = processor.process_file(f.read(), 'jpg')
    assert result['success'] == True
```
