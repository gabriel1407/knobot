from django.core.management.base import BaseCommand
from apps.ai.services import RAGService


class Command(BaseCommand):
    help = 'Limpia completamente el vector store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirmar la eliminación sin preguntar'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            confirm = input(
                '⚠️  Esto eliminará TODOS los documentos del vector store. '
                '¿Estás seguro? (yes/no): '
            )
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operación cancelada'))
                return

        try:
            rag_service = RAGService()
            
            # Obtener conteo antes de limpiar
            count_before = rag_service.vector_store.count()
            
            self.stdout.write(f'Documentos en vector store: {count_before}')
            self.stdout.write('Limpiando vector store...')
            
            # Limpiar
            rag_service.vector_store.clear()
            
            # Verificar
            count_after = rag_service.vector_store.count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Vector store limpiado. '
                    f'Eliminados {count_before} documentos'
                )
            )
            self.stdout.write(f'Documentos restantes: {count_after}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al limpiar vector store: {str(e)}')
            )
