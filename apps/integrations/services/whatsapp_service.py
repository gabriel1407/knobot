import httpx
from typing import Dict, Optional
from django.conf import settings


class WhatsAppService:
    """
    Servicio para integración con WhatsApp Business API.
    
    Documentación: https://developers.facebook.com/docs/whatsapp/cloud-api
    """
    
    def __init__(self, phone_number_id: str, access_token: str):
        """
        Inicializa el servicio de WhatsApp.
        
        Args:
            phone_number_id: ID del número de teléfono de WhatsApp Business
            access_token: Token de acceso de la API de WhatsApp
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.base_url = f"https://graph.facebook.com/v18.0/{phone_number_id}"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    async def send_message(
        self,
        to: str,
        message: str,
        message_type: str = 'text'
    ) -> Dict:
        """
        Envía un mensaje de texto a un número de WhatsApp.
        
        Args:
            to: Número de teléfono del destinatario (formato: 57300123456)
            message: Contenido del mensaje
            message_type: Tipo de mensaje (text, template, etc.)
            
        Returns:
            Respuesta de la API de WhatsApp
        """
        url = f"{self.base_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": message_type,
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = 'es',
        components: Optional[list] = None
    ) -> Dict:
        """
        Envía un mensaje usando una plantilla aprobada.
        
        Args:
            to: Número de teléfono del destinatario
            template_name: Nombre de la plantilla
            language_code: Código de idioma (es, en, etc.)
            components: Componentes de la plantilla (parámetros)
            
        Returns:
            Respuesta de la API de WhatsApp
        """
        url = f"{self.base_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def mark_as_read(self, message_id: str) -> Dict:
        """
        Marca un mensaje como leído.
        
        Args:
            message_id: ID del mensaje a marcar como leído
            
        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def parse_webhook_message(payload: Dict) -> Optional[Dict]:
        """
        Parsea el payload del webhook de WhatsApp para extraer el mensaje.
        
        Args:
            payload: Payload del webhook
            
        Returns:
            Diccionario con información del mensaje o None
        """
        try:
            entry = payload.get('entry', [])[0]
            changes = entry.get('changes', [])[0]
            value = changes.get('value', {})
            
            # Verificar que sea un mensaje
            messages = value.get('messages', [])
            if not messages:
                return None
            
            message = messages[0]
            
            # Extraer información del contacto
            contacts = value.get('contacts', [])
            contact = contacts[0] if contacts else {}
            
            return {
                'message_id': message.get('id'),
                'from': message.get('from'),
                'timestamp': message.get('timestamp'),
                'type': message.get('type'),
                'text': message.get('text', {}).get('body', ''),
                'contact_name': contact.get('profile', {}).get('name', ''),
                'metadata': value.get('metadata', {})
            }
        except (IndexError, KeyError) as e:
            return None
    
    @staticmethod
    def verify_webhook(mode: str, token: str, verify_token: str) -> Optional[str]:
        """
        Verifica el webhook de WhatsApp.
        
        Args:
            mode: Modo de verificación
            token: Token recibido
            verify_token: Token esperado
            
        Returns:
            Challenge si es válido, None si no
        """
        if mode == "subscribe" and token == verify_token:
            return token
        return None
