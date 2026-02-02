import asyncio
from typing import Dict, Optional
from django.utils import timezone
try:
    from apps.ai.services import ChatOrchestrator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    import google.generativeai as genai
    from django.conf import settings
from apps.chat.models import Conversation, Message
from apps.users.models import User
from .whatsapp_service import WhatsAppService
from .telegram_service import TelegramService


class MessageHandler:
    """
    Handler centralizado para procesar mensajes de WhatsApp y Telegram.
    Integra con ChatOrchestrator y RAG para generar respuestas.
    """
    
    def __init__(self):
        self.chat_orchestrator = ChatOrchestrator()
    
    async def handle_whatsapp_message(
        self,
        message_data: Dict,
        whatsapp_service: WhatsAppService
    ) -> Dict:
        """
        Procesa un mensaje de WhatsApp.
        
        Args:
            message_data: Datos del mensaje parseados
            whatsapp_service: Instancia del servicio de WhatsApp
            
        Returns:
            Resultado del procesamiento
        """
        phone_number = message_data['from']
        message_text = message_data['text']
        message_id = message_data['message_id']
        contact_name = message_data.get('contact_name', '')
        
        # Obtener o crear usuario
        user = await self._get_or_create_user_from_phone(
            phone_number,
            contact_name,
            'whatsapp'
        )
        
        # Obtener o crear conversación
        conversation = await self._get_or_create_conversation(
            user,
            f"WhatsApp - {contact_name or phone_number}",
            platform='whatsapp',
            platform_user_id=phone_number
        )
        
        # Marcar mensaje como leído
        try:
            await whatsapp_service.mark_as_read(message_id)
        except Exception:
            pass  # No crítico si falla
        
        # Procesar mensaje con RAG
        response = await self._process_with_rag(
            conversation_id=str(conversation.id),
            user_message=message_text
        )
        
        # Enviar respuesta por WhatsApp
        await whatsapp_service.send_message(
            to=phone_number,
            message=response['content']
        )
        
        return {
            'success': True,
            'conversation_id': str(conversation.id),
            'message_id': response['message_id'],
            'platform': 'whatsapp'
        }
    
    async def handle_telegram_message(
        self,
        message_data: Dict,
        telegram_service: TelegramService
    ) -> Dict:
        """
        Procesa un mensaje de Telegram.
        
        Args:
            message_data: Datos del mensaje parseados
            telegram_service: Instancia del servicio de Telegram
            
        Returns:
            Resultado del procesamiento
        """
        chat_id = str(message_data['chat_id'])
        message_text = message_data['text']
        from_username = message_data.get('from_username', '')
        from_first_name = message_data.get('from_first_name', '')
        from_last_name = message_data.get('from_last_name', '')
        
        # Nombre completo
        full_name = f"{from_first_name} {from_last_name}".strip()
        
        # Obtener o crear usuario
        user = await self._get_or_create_user_from_telegram(
            chat_id,
            from_username,
            full_name
        )
        
        # Obtener o crear conversación
        conversation = await self._get_or_create_conversation(
            user,
            f"Telegram - {from_username or full_name}",
            platform='telegram',
            platform_user_id=chat_id
        )
        
        # Enviar acción de "escribiendo..."
        try:
            await telegram_service.send_typing_action(chat_id)
        except Exception:
            pass
        
        # Procesar mensaje con RAG
        response = await self._process_with_rag(
            conversation_id=str(conversation.id),
            user_message=message_text
        )
        
        # Enviar respuesta por Telegram
        await telegram_service.send_message(
            chat_id=chat_id,
            text=response['content'],
            parse_mode='Markdown'
        )
        
        return {
            'success': True,
            'conversation_id': str(conversation.id),
            'message_id': response['message_id'],
            'platform': 'telegram'
        }
    
    async def _process_with_rag(
        self,
        conversation_id: str,
        user_message: str
    ) -> Dict:
        """
        Procesa un mensaje con RAG.
        ChatOrchestrator se encarga de guardar los mensajes.
        
        Args:
            conversation_id: ID de la conversación
            user_message: Mensaje del usuario
            
        Returns:
            Diccionario con la respuesta y metadata
        """
        loop = asyncio.get_event_loop()
        
        def _process():
            # ChatOrchestrator ya guarda los mensajes internamente
            if AI_AVAILABLE:
                result = self.chat_orchestrator.process_message(
                    conversation_id=conversation_id,
                    user_message=user_message,
                    use_rag=True,
                    n_context_docs=5
                )
                return result
            else:
                # Fallback: guardar manualmente y usar Gemini
                from apps.chat.models import Conversation, Message
                conversation = Conversation.objects.get(id=conversation_id)
                
                # Guardar mensaje del usuario
                Message.objects.create(
                    conversation=conversation,
                    content=user_message,
                    role='user'
                )
                
                # Generar respuesta con Gemini
                response_text = asyncio.run(
                    self._generate_response_with_gemini_only(user_message)
                )
                
                # Guardar respuesta del bot
                bot_msg = Message.objects.create(
                    conversation=conversation,
                    content=response_text,
                    role='assistant'
                )
                
                return {
                    'content': response_text,
                    'message_id': str(bot_msg.id),
                    'conversation_id': conversation_id
                }
        
        return await loop.run_in_executor(None, _process)
    
    async def _generate_response_with_gemini_only(self, message: str) -> str:
        """Genera respuesta usando solo Gemini sin RAG."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""Eres un asistente virtual de soporte técnico para un ISP (proveedor de internet).
Responde de manera amigable, profesional y concisa.

Usuario: {message}

Asistente:"""
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating response with Gemini: {e}")
            return "Lo siento, estoy experimentando dificultades técnicas. Por favor, intenta de nuevo en unos momentos."
    
    async def _generate_response(self, message: str, conversation_id: int) -> str:
        """
        Genera una respuesta usando ChatOrchestrator con RAG o Gemini directo.
        
        Args:
            message: Mensaje del usuario
            conversation_id: ID de la conversación
            
        Returns:
            Respuesta generada
        """
        try:
            if AI_AVAILABLE:
                orchestrator = ChatOrchestrator()
                response = await orchestrator.process_message(
                    message=message,
                    conversation_id=conversation_id,
                    use_rag=True,
                    n_results=5
                )
                return response
            else:
                # Usar Gemini directo sin RAG
                logger.warning("AI services not available, using Gemini without RAG")
                return await self._generate_response_with_gemini_only(message)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Lo siento, estoy experimentando dificultades técnicas. Por favor, intenta de nuevo en unos momentos."
    
    async def _get_or_create_user_from_phone(
        self,
        phone_number: str,
        name: str,
        platform: str
    ) -> User:
        """
        Obtiene o crea un usuario desde un número de teléfono.
        """
        loop = asyncio.get_event_loop()
        
        def _get_or_create():
            # Buscar por teléfono
            user = User.objects.filter(phone=phone_number).first()
            
            if not user:
                # Crear usuario
                username = f"{platform}_{phone_number}"
                email = f"{username}@knowbot.local"
                
                user = User.objects.create(
                    username=username,
                    email=email,
                    phone=phone_number,
                    first_name=name or phone_number,
                    role='customer'
                )
            
            return user
        
        return await loop.run_in_executor(None, _get_or_create)
    
    async def _get_or_create_user_from_telegram(
        self,
        chat_id: str,
        username: str,
        full_name: str
    ) -> User:
        """
        Obtiene o crea un usuario desde Telegram.
        """
        loop = asyncio.get_event_loop()
        
        def _get_or_create():
            # Usar chat_id como identificador único
            username_base = f"tg_{chat_id}"
            email = f"{username_base}@knowbot.local"
            
            # Usar get_or_create para evitar duplicados
            user, created = User.objects.get_or_create(
                username=username_base,
                defaults={
                    'email': email,
                    'first_name': full_name or username or f"User {chat_id}",
                    'role': 'customer'
                }
            )
            
            return user
        
        return await loop.run_in_executor(None, _get_or_create)
    
    async def _get_or_create_conversation(
        self,
        user: User,
        title: str,
        platform: str,
        platform_user_id: str
    ) -> Conversation:
        """
        Obtiene o crea una conversación para un usuario.
        """
        loop = asyncio.get_event_loop()
        
        def _get_or_create():
            # Buscar conversación activa del usuario en esta plataforma
            conversation = Conversation.objects.filter(
                user=user,
                status='active',
                metadata__platform=platform,
                metadata__platform_user_id=platform_user_id
            ).first()
            
            if not conversation:
                # Crear nueva conversación
                conversation = Conversation.objects.create(
                    user=user,
                    title=title,
                    status='active',
                    metadata={
                        'platform': platform,
                        'platform_user_id': platform_user_id,
                        'created_via': platform
                    }
                )
            
            return conversation
        
        return await loop.run_in_executor(None, _get_or_create)
