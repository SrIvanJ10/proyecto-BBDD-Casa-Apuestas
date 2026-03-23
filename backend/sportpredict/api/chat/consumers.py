"""
WebSocket consumer para chat en tiempo real entre amigos.

Flujo:
  1. Cliente conecta a ws://<host>/ws/chat/<other_user_id>/?token=<jwt>
  2. Consumer autentica el token y verifica que ambos son amigos.
  3. Ambos usuarios se unen al mismo group (chat_<min_id>_<max_id>).
  4. Cuando un usuario envía un mensaje, se guarda en PostgreSQL y se
     difunde al group → ambos lo reciben al instante.
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from sportpredict.api.utils.authentication import decode_jwt_token
from sportpredict.db.neo4j_utils import Neo4jClient
from sportpredict.models import ChatMessage, Usuario
from sportpredict.serializers import ChatMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def connect(self):
        self.other_user_id = int(self.scope['url_route']['kwargs']['other_user_id'])

        # Autenticar mediante el token JWT en los query params
        token = self._get_token()
        if not token:
            await self.close(code=4001)
            return

        self.user = await self.get_user_from_token(token)
        if not self.user:
            await self.close(code=4001)
            return

        if self.user.id == self.other_user_id:
            await self.close(code=4002)
            return

        # Solo amigos pueden chatear
        if not await self.check_friendship(self.user.id, self.other_user_id):
            await self.close(code=4003)
            return

        # Nombre de grupo consistente para ambos usuarios
        min_id = min(self.user.id, self.other_user_id)
        max_id = max(self.user.id, self.other_user_id)
        self.room_group_name = f'chat_{min_id}_{max_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # ------------------------------------------------------------------
    # Recibir mensaje del cliente
    # ------------------------------------------------------------------

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        content = (data.get('content') or '').strip()
        if not content or len(content) > 1000:
            return

        message = await self.save_message(content)
        if not message:
            return

        message_data = await self.serialize_message(message)

        # Difundir a todos los miembros del grupo (emisor y receptor)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            },
        )

    # ------------------------------------------------------------------
    # Handler del evento del group
    # ------------------------------------------------------------------

    async def chat_message(self, event):
        """Reenvía el mensaje al WebSocket del cliente."""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
        }))

    # ------------------------------------------------------------------
    # Helpers síncronos ejecutados en thread pool
    # ------------------------------------------------------------------

    def _get_token(self):
        query_string = self.scope.get('query_string', b'').decode()
        for param in query_string.split('&'):
            if '=' in param:
                k, v = param.split('=', 1)
                if k == 'token':
                    return v
        return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = decode_jwt_token(token)
            return Usuario.objects.get(id=payload['user_id'])
        except Exception:
            return None

    @database_sync_to_async
    def check_friendship(self, user_id, other_id):
        return Neo4jClient().are_friends(user_id, other_id)

    @database_sync_to_async
    def save_message(self, content):
        try:
            receiver = Usuario.objects.get(id=self.other_user_id)
            return ChatMessage.objects.create(
                sender=self.user,
                receiver=receiver,
                content=content,
            )
        except Usuario.DoesNotExist:
            return None

    @database_sync_to_async
    def serialize_message(self, message):
        return ChatMessageSerializer(message).data
