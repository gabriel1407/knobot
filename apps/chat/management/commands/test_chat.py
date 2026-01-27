from django.core.management.base import BaseCommand
from apps.ai.services import ChatOrchestrator
from apps.users.models import User
from apps.chat.models import Conversation


class Command(BaseCommand):
    help = 'Prueba el chat con RAG de forma interactiva'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=str,
            help='ID del usuario (se creará uno de prueba si no existe)'
        )
        parser.add_argument(
            '--no-rag',
            action='store_true',
            help='Desactivar RAG (solo conversación)'
        )
        parser.add_argument(
            '--n-context',
            type=int,
            default=5,
            help='Número de documentos de contexto (default: 5)'
        )

    def handle(self, *args, **options):
        orchestrator = ChatOrchestrator()

        # Obtener o crear usuario de prueba
        if options['user_id']:
            try:
                user = User.objects.get(id=options['user_id'])
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuario {options["user_id"]} no encontrado')
                )
                return
        else:
            user, created = User.objects.get_or_create(
                username='test_user',
                defaults={
                    'email': 'test@knowbot.com',
                    'role': 'customer'
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Usuario de prueba creado: {user.id}')
                )

        # Crear conversación
        conversation = orchestrator.create_conversation(
            user_id=str(user.id),
            title='Conversación de prueba'
        )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('CHAT INTERACTIVO - KnoBot'))
        self.stdout.write('='*60)
        self.stdout.write(f'Usuario: {user.username}')
        self.stdout.write(f'Conversación ID: {conversation.id}')
        self.stdout.write(f'RAG: {"Desactivado" if options["no_rag"] else "Activado"}')
        if not options['no_rag']:
            self.stdout.write(f'Documentos de contexto: {options["n_context"]}')
        self.stdout.write('\nEscribe "salir" para terminar')
        self.stdout.write('='*60 + '\n')

        # Loop de conversación
        while True:
            try:
                # Obtener mensaje del usuario
                user_message = input(self.style.SUCCESS('Tú: '))
                
                if user_message.lower() in ['salir', 'exit', 'quit']:
                    self.stdout.write('\nFinalizando conversación...')
                    orchestrator.end_conversation(str(conversation.id))
                    self.stdout.write(
                        self.style.SUCCESS('¡Hasta luego!')
                    )
                    break

                if not user_message.strip():
                    continue

                # Procesar mensaje
                self.stdout.write('Procesando...')
                
                response = orchestrator.process_message(
                    conversation_id=str(conversation.id),
                    user_message=user_message,
                    use_rag=not options['no_rag'],
                    n_context_docs=options['n_context']
                )

                # Mostrar respuesta
                self.stdout.write(
                    self.style.WARNING(f'\nAsistente: {response["content"]}\n')
                )

                # Mostrar metadatos
                if response.get('context_used', 0) > 0:
                    self.stdout.write(
                        self.style.HTTP_INFO(
                            f'[Contexto usado: {response["context_used"]} documentos]'
                        )
                    )
                if response.get('tokens_used', 0) > 0:
                    self.stdout.write(
                        self.style.HTTP_INFO(
                            f'[Tokens: {response["tokens_used"]}]'
                        )
                    )
                self.stdout.write('')

            except KeyboardInterrupt:
                self.stdout.write('\n\nInterrumpido por el usuario')
                orchestrator.end_conversation(str(conversation.id))
                break
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'\nError: {str(e)}\n')
                )
