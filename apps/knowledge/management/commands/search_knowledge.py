from django.core.management.base import BaseCommand
from apps.ai.services import RAGService


class Command(BaseCommand):
    help = 'Busca en la base de conocimiento usando búsqueda semántica'

    def add_arguments(self, parser):
        parser.add_argument(
            'query',
            type=str,
            help='Consulta de búsqueda'
        )
        parser.add_argument(
            '--n-results',
            type=int,
            default=5,
            help='Número de resultados a mostrar (default: 5)'
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Filtrar por categoría'
        )

    def handle(self, *args, **options):
        rag_service = RAGService()
        query = options['query']
        n_results = options['n_results']

        self.stdout.write(f'\nBuscando: "{query}"')
        self.stdout.write('='*50)

        # Preparar filtros
        filters = None
        if options['category']:
            filters = {'category': options['category']}

        # Realizar búsqueda
        try:
            results = rag_service.retrieve_context(
                query=query,
                n_results=n_results,
                filters=filters
            )

            if not results:
                self.stdout.write(
                    self.style.WARNING('No se encontraron resultados')
                )
                return

            # Mostrar resultados
            for i, result in enumerate(results, 1):
                self.stdout.write(f'\n{i}. Score: {result["score"]:.4f}')
                self.stdout.write(f'   ID: {result["id"]}')
                
                # Mostrar metadatos
                metadata = result.get('metadata', {})
                if metadata:
                    if 'document_title' in metadata:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'   Documento: {metadata["document_title"]}'
                            )
                        )
                    if 'category' in metadata:
                        self.stdout.write(f'   Categoría: {metadata["category"]}')
                    if 'chunk_index' in metadata:
                        self.stdout.write(
                            f'   Chunk: {metadata["chunk_index"] + 1}/'
                            f'{metadata.get("total_chunks", "?")}'
                        )
                
                # Mostrar contenido (primeros 200 caracteres)
                content = result['content']
                preview = content[:200] + '...' if len(content) > 200 else content
                self.stdout.write(f'   Contenido: {preview}')
                self.stdout.write('-'*50)

            self.stdout.write(
                self.style.SUCCESS(f'\n✓ Encontrados {len(results)} resultados')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error en la búsqueda: {str(e)}')
            )
