import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db.models import Q


from .models import Message, ChatRoom
from .serializers import MessageSerializer


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.room_group_name = f'chat_{self.chat_room_id}'
        self.channel_layer = get_channel_layer()


        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.handle_chat_message(data)

    async def handle_chat_message(self, data):
        message = data["message"]

        message_obj = await self.save_message(self.user, message)
        message_data = MessageSerializer(message_obj).data


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_data
            }
        )


    @database_sync_to_async
    def save_message(self, sender, content):

        chat_room = ChatRoom.objects.get(uuid=self.chat_room_id)
        receiver = chat_room.friendship.user1 if chat_room.friendship.user1 != sender else chat_room.friendship.user2
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
