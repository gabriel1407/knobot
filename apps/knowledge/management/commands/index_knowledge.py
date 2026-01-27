from django.core.management.base import BaseCommand
from django.db import transaction
from apps.knowledge.models import Document, KnowledgeBase
from apps.ai.services import RAGService, FileProcessor
from typing import Optional


class Command(BaseCommand):
    help = 'Indexa documentos de la base de conocimiento en el vector store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--knowledge-base',
            type=str,
            help='ID de la base de conocimiento específica a indexar'
        )
        parser.add_argument(
            '--document',
            type=str,
            help='ID del documento específico a indexar'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar el vector store antes de indexar'
        )
        parser.add_argument(
            '--chunk-size',
            type=int,
            default=500,
            help='Tamaño de los chunks de texto (default: 500)'
        )
        parser.add_argument(
            '--overlap',
            type=int,
            default=50,
            help='Overlap entre chunks (default: 50)'
        )

    def handle(self, *args, **options):
        rag_service = RAGService()
        file_processor = FileProcessor()

        # Limpiar vector store si se solicita
        if options['clear']:
            self.stdout.write(self.style.WARNING('Limpiando vector store...'))
            rag_service.vector_store.clear()
            self.stdout.write(self.style.SUCCESS('Vector store limpiado'))

        # Filtrar documentos según opciones
        if options['document']:
            documents = Document.objects.filter(
                id=options['document'],
                is_active=True
            )
        elif options['knowledge_base']:
            documents = Document.objects.filter(
                knowledge_base_id=options['knowledge_base'],
                is_active=True
            )
        else:
            documents = Document.objects.filter(is_active=True)

        total_docs = documents.count()
        self.stdout.write(f'Encontrados {total_docs} documentos para indexar')

        indexed_count = 0
        error_count = 0
        total_chunks = 0

        for doc in documents:
            try:
                self.stdout.write(f'\nProcesando: {doc.title}')

                # Determinar si es archivo o texto plano
                if doc.file_url:
                    # TODO: Descargar archivo desde URL
                    self.stdout.write(
                        self.style.WARNING(
                            f'  Archivo externo no soportado aún: {doc.file_url}'
                        )
                    )
                    continue

                # Procesar contenido de texto
                content = doc.content
                
                if not content or len(content.strip()) == 0:
                    self.stdout.write(
                        self.style.WARNING('  Documento sin contenido, omitiendo')
                    )
                    continue

                # Dividir en chunks si es necesario
                if len(content) > options['chunk_size']:
                    chunks = file_processor.document_processor.chunk_text(
                        content,
                        chunk_size=options['chunk_size'],
                        overlap=options['overlap']
                    )
                    
                    # Indexar cada chunk
                    for i, chunk in enumerate(chunks):
                        chunk_id = f"{doc.id}-chunk-{i}"
                        metadata = {
                            'document_id': str(doc.id),
                            'document_title': doc.title,
                            'knowledge_base_id': str(doc.knowledge_base_id),
                            'knowledge_base_title': doc.knowledge_base.title,
                            'category': doc.knowledge_base.category,
                            'chunk_index': i,
                            'total_chunks': len(chunks)
                        }
                        
                        rag_service.index_document(
                            document_id=chunk_id,
                            content=chunk,
                            metadata=metadata
                        )
                        total_chunks += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ Indexado en {len(chunks)} chunks'
                        )
                    )
                else:
                    # Indexar documento completo
                    metadata = {
                        'document_id': str(doc.id),
                        'document_title': doc.title,
                        'knowledge_base_id': str(doc.knowledge_base_id),
                        'knowledge_base_title': doc.knowledge_base.title,
                        'category': doc.knowledge_base.category,
                    }
                    
                    rag_service.index_document(
                        document_id=str(doc.id),
                        content=content,
                        metadata=metadata
                    )
                    total_chunks += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS('  ✓ Indexado como documento único')
                    )

                # Actualizar embedding en el modelo
                doc.embedding = {'indexed': True, 'chunks': total_chunks}
                doc.save(update_fields=['embedding'])
                
                indexed_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error: {str(e)}')
                )

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Indexación completada'))
        self.stdout.write(f'Documentos procesados: {indexed_count}/{total_docs}')
        self.stdout.write(f'Total de chunks creados: {total_chunks}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errores: {error_count}'))
        self.stdout.write('='*50)
