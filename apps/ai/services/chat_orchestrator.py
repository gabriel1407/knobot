import google.generativeai as genai
from typing import List, Dict, Optional
from django.conf import settings
from .rag_service import RAGService
from apps.chat.models import Conversation, Message


class ChatOrchestrator:
    """
    Orquestador principal del chat que integra RAG con LLM (Gemini).
    """
    
    def __init__(self, rag_service: Optional[RAGService] = None):
        """
        Inicializa el orquestador de chat.
        
        Args:
            rag_service: Servicio RAG para búsqueda de contexto.
        """
        self.rag_service = rag_service or RAGService()
        
        # Configurar Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process_message(
        self,
        conversation_id: str,
        user_message: str,
        use_rag: bool = True,
        n_context_docs: int = 5
    ) -> Dict:
        """
        Procesa un mensaje del usuario y genera una respuesta.
        
        Args:
            conversation_id: ID de la conversación.
            user_message: Mensaje del usuario.
            use_rag: Si debe usar RAG para contexto.
            n_context_docs: Número de documentos de contexto a recuperar.
            
        Returns:
            Diccionario con la respuesta y metadatos.
        """
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValueError(f"Conversación {conversation_id} no encontrada")
        
        # Guardar mensaje del usuario
        user_msg = Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Construir prompt con o sin RAG
        if use_rag:
            context_docs = self.rag_service.retrieve_context(
                query=user_message,
                n_results=n_context_docs
            )
            prompt = self._build_rag_prompt(user_message, context_docs, conversation)
            metadata = {
                'context_docs': [
                    {'id': doc['id'], 'score': doc['score']}
                    for doc in context_docs
                ]
            }
        else:
            prompt = self._build_conversation_prompt(user_message, conversation)
            metadata = {}
        
        # Generar respuesta con Gemini
        response = self._generate_response(prompt)
        
        # Guardar respuesta del asistente
        assistant_msg = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response['text'],
            metadata=metadata,
            tokens_used=response.get('tokens_used', 0)
        )
        
        return {
            'message_id': str(assistant_msg.id),
            'content': response['text'],
            'tokens_used': response.get('tokens_used', 0),
            'context_used': len(context_docs) if use_rag else 0
        }
    
    def _build_rag_prompt(
        self,
        user_message: str,
        context_docs: List[Dict],
        conversation: Conversation
    ) -> str:
        """
        Construye un prompt con contexto RAG.
        
        Args:
            user_message: Mensaje del usuario.
            context_docs: Documentos de contexto.
            conversation: Conversación actual.
            
        Returns:
            Prompt formateado.
        """
        # Obtener historial de conversación
        history = self._get_conversation_history(conversation, max_messages=5)
        
        # Construir contexto
        context_parts = []
        for doc in context_docs:
            context_parts.append(f"- {doc['content']} (relevancia: {doc['score']:.2f})")
        
        context = "\n".join(context_parts)
        
        prompt = f"""Eres un asistente virtual experto para un proveedor de servicios de Internet (ISP).

Contexto relevante de la base de conocimiento:
{context}

Historial de conversación:
{history}

Usuario: {user_message}

Instrucciones:
- Responde de manera clara, profesional y amigable
- Usa el contexto proporcionado cuando sea relevante
- Si no tienes información suficiente, sé honesto al respecto
- Mantén la coherencia con el historial de la conversación
- Ofrece soluciones prácticas cuando sea posible

Asistente:"""
        
        return prompt
    
    def _build_conversation_prompt(
        self,
        user_message: str,
        conversation: Conversation
    ) -> str:
        """
        Construye un prompt sin RAG, solo con historial.
        
        Args:
            user_message: Mensaje del usuario.
            conversation: Conversación actual.
            
        Returns:
            Prompt formateado.
        """
        history = self._get_conversation_history(conversation, max_messages=10)
        
        prompt = f"""Eres un asistente virtual experto para un proveedor de servicios de Internet (ISP).

Historial de conversación:
{history}

Usuario: {user_message}

Instrucciones:
- Responde de manera clara, profesional y amigable
- Mantén la coherencia con el historial de la conversación
- Ofrece soluciones prácticas cuando sea posible

Asistente:"""
        
        return prompt
    
    def _get_conversation_history(
        self,
        conversation: Conversation,
        max_messages: int = 10
    ) -> str:
        """
        Obtiene el historial de la conversación.
        
        Args:
            conversation: Conversación.
            max_messages: Número máximo de mensajes a incluir.
            
        Returns:
            Historial formateado.
        """
        messages = conversation.messages.filter(
            is_active=True
        ).order_by('-created_at')[:max_messages]
        
        history_parts = []
        for msg in reversed(list(messages)):
            role = "Usuario" if msg.role == "user" else "Asistente"
            history_parts.append(f"{role}: {msg.content}")
        
        return "\n".join(history_parts) if history_parts else "Sin historial previo"
    
    def _generate_response(self, prompt: str) -> Dict:
        """
        Genera una respuesta usando Gemini.
        
        Args:
            prompt: Prompt para el modelo.
            
        Returns:
            Diccionario con la respuesta y metadatos.
        """
        try:
            response = self.model.generate_content(prompt)
            
            return {
                'text': response.text,
                'tokens_used': 0  # Gemini no proporciona conteo de tokens directamente
            }
        except Exception as e:
            # Fallback en caso de error
            return {
                'text': f"Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.",
                'tokens_used': 0,
                'error': str(e)
            }
    
    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """
        Crea una nueva conversación.
        
        Args:
            user_id: ID del usuario.
            title: Título opcional de la conversación.
            
        Returns:
            Conversación creada.
        """
        from apps.users.models import User
        
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.create(
            user=user,
            title=title or "Nueva conversación",
            status='active'
        )
        
        return conversation
    
    def end_conversation(self, conversation_id: str) -> None:
        """
        Finaliza una conversación.
        
        Args:
            conversation_id: ID de la conversación.
        """
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.status = 'resolved'
        conversation.save()
