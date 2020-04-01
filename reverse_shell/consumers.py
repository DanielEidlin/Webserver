import json
from channels.db import database_sync_to_async
from reverse_shell.models import Attacker, Victim
from channels.generic.websocket import AsyncWebsocketConsumer


class AttackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        print(user)
        await self.set_channel_name(user)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def set_channel_name(self, user):
        attacker = Attacker.objects.get(owner=user)
        attacker.channel_name = self.channel_name
        attacker.save()
