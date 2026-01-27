from django.core.management.base import BaseCommand
from apps.ai.services import RAGService
from apps.knowledge.models import Document


class Command(BaseCommand):
    help = 'Muestra estadísticas del vector store y la base de conocimiento'

    def handle(self, *args, **options):
        rag_service = RAGService()

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('ESTADÍSTICAS DEL SISTEMA'))
        self.stdout.write('='*50)

        # Estadísticas del vector store
        try:
            vector_count = rag_service.vector_store.count()
            self.stdout.write(f'\n📊 Vector Store:')
            self.stdout.write(f'   Documentos indexados: {vector_count}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   Error al obtener stats: {str(e)}')
            )

        # Estadísticas de la base de datos
        total_docs = Document.objects.count()
        active_docs = Document.objects.filter(is_active=True).count()
        indexed_docs = Document.objects.filter(
            embedding__isnull=False,
            is_active=True
        ).count()

        self.stdout.write(f'\n📚 Base de Conocimiento:')
        self.stdout.write(f'   Total de documentos: {total_docs}')
        self.stdout.write(f'   Documentos activos: {active_docs}')
        self.stdout.write(f'   Documentos indexados: {indexed_docs}')
        
        if active_docs > 0:
            percentage = (indexed_docs / active_docs) * 100
            self.stdout.write(f'   Porcentaje indexado: {percentage:.1f}%')

        # Documentos pendientes de indexar
        pending = active_docs - indexed_docs
        if pending > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  Hay {pending} documentos pendientes de indexar'
                )
            )
            self.stdout.write(
                '   Ejecuta: python manage.py index_knowledge'
            )

        self.stdout.write('\n' + '='*50 + '\n')
