import httpx
from typing import Dict, Optional, List


class TelegramService:
    """
    Servicio para integración con Telegram Bot API.
    
    Documentación: https://core.telegram.org/bots/api
    """
    
    def __init__(self, bot_token: str):
        """
        Inicializa el servicio de Telegram.
        
        Args:
            bot_token: Token del bot de Telegram
        """
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: str = 'Markdown',
        reply_markup: Optional[Dict] = None
    ) -> Dict:
        """
        Envía un mensaje de texto.
        
        Args:
            chat_id: ID del chat
            text: Texto del mensaje
            parse_mode: Modo de parseo (Markdown, HTML)
            reply_markup: Teclado inline o reply keyboard
            
        Returns:
            Respuesta de la API de Telegram
        """
        url = f"{self.base_url}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def send_typing_action(self, chat_id: str) -> Dict:
        """
        Envía acción de "escribiendo...".
        
        Args:
            chat_id: ID del chat
            
        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/sendChatAction"
        
        payload = {
            "chat_id": chat_id,
            "action": "typing"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def get_me(self) -> Dict:
        """
        Obtiene información del bot.
        
        Returns:
            Información del bot
        """
        url = f"{self.base_url}/getMe"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def set_webhook(self, webhook_url: str, secret_token: Optional[str] = None) -> Dict:
        """
        Configura el webhook del bot.
        
        Args:
            webhook_url: URL del webhook
            secret_token: Token secreto para validar requests
            
        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/setWebhook"
        
        payload = {
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query"]
        }
        
        if secret_token:
            payload["secret_token"] = secret_token
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def delete_webhook(self) -> Dict:
        """
        Elimina el webhook del bot.
        
        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/deleteWebhook"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    async def get_webhook_info(self) -> Dict:
        """
        Obtiene información del webhook configurado.
        
        Returns:
            Información del webhook
        """
        url = f"{self.base_url}/getWebhookInfo"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def parse_webhook_message(payload: Dict) -> Optional[Dict]:
        """
        Parsea el payload del webhook de Telegram para extraer el mensaje.
        
        Args:
            payload: Payload del webhook
            
        Returns:
            Diccionario con información del mensaje o None
        """
        try:
            message = payload.get('message')
            if not message:
                return None
            
            chat = message.get('chat', {})
            from_user = message.get('from', {})
            
            return {
                'message_id': message.get('message_id'),
                'chat_id': chat.get('id'),
                'chat_type': chat.get('type'),
                'from_id': from_user.get('id'),
                'from_username': from_user.get('username'),
                'from_first_name': from_user.get('first_name'),
                'from_last_name': from_user.get('last_name'),
                'text': message.get('text', ''),
                'date': message.get('date'),
            }
        except (KeyError, TypeError):
            return None
    
    @staticmethod
    def create_inline_keyboard(buttons: List[List[Dict]]) -> Dict:
        """
        Crea un teclado inline.
        
        Args:
            buttons: Lista de filas de botones
                    Ejemplo: [[{"text": "Botón 1", "callback_data": "btn1"}]]
            
        Returns:
            Markup del teclado inline
        """
        return {
            "inline_keyboard": buttons
        }
    
    @staticmethod
    def create_reply_keyboard(
        buttons: List[List[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> Dict:
        """
        Crea un teclado de respuesta.
        
        Args:
            buttons: Lista de filas de botones (texto)
            resize_keyboard: Ajustar tamaño del teclado
            one_time_keyboard: Ocultar después de usar
            
        Returns:
            Markup del teclado de respuesta
        """
        keyboard = [[{"text": btn} for btn in row] for row in buttons]
        
        return {
            "keyboard": keyboard,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard
        }
