import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Session
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f'chat_{self.session_id}'

        if not await self._session_exists_for_user(self.session_id, self.user.id):
            await self.close(code=4004)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        body = json.loads(text_data)
        action = body.get('action')
        payload = body.get('payload', {})

        if action == 'send_message':
            message_data = await self._save_message(
                session_id=self.session_id,
                user_id=self.user.id,
                content=payload.get('content', ''),
                modality=payload.get('modality', 'text')
            )

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'payload': {
                        'type': 'message',
                        'data': message_data
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['payload']))

    @sync_to_async
    def _session_exists_for_user(self, session_id, user_id):
        return Session.objects.filter(id=session_id, created_by_id=user_id, is_active=True).exists()

    @sync_to_async
    def _save_message(self, session_id, user_id, content, modality):
        session = Session.objects.get(id=session_id)
        message = Message.objects.create(
            session=session,
            sender_id=user_id,
            content=content,
            modality=modality
        )
        return MessageSerializer(message).data
