# chat/consumers.py
import json

from pprint import pprint
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get the user from the scope (requires authentication)
        self.user = self.scope["user"]

        await self.accept()

        if self.user.is_authenticated:
            # Create a unique channel group name for this user
            self.user_group = f"chat_{self.user.username}"

            # Join the user's personal group
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )

        else:
            await self.send_error("User not authenticated")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group'):
            # Leave the user's personal group
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )

    @database_sync_to_async
    def get_user(self, username) -> User:
        try:
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

    async def send_error(self, error):
        await self.send(text_data=json.dumps({
            "type": "chat.error",
            "error": error
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")
        message_id = text_data_json.get("messageId", None)

        match message_type:
            # Client requests for initial messages between the sender and receiver
            case "chat.initial_messages":
                receiver_username = text_data_json.get("receiver")
                receiver = await self.get_user(receiver_username)
                if receiver is None:
                    await self.send_error("User not found")
                    return

                messages = await self.get_messages(self.user, receiver)
                await self.send(text_data=json.dumps({
                    "messageId": message_id,
                    "type": message_type,
                    "initial_messages": messages
                }))

            # Client request for recent messages sent to/by them
            case "chat.recent_messages":
                messages = await self.get_recent_messages()
                await self.send(text_data=json.dumps({
                    "messageId": message_id,
                    "type": message_type,
                    "recent_messages": messages
                }))

            case "chat.message":
                # Client sends a message to the receiver

                receiver_username = text_data_json.get("receiver")
                message = text_data_json.get("message")

                receiver = await self.get_user(receiver_username)

                if receiver is None:
                    await self.send_error("User not found")
                    return

                message_obj = await self.save_message(message, receiver)

                # print(MessageSerializer(message_obj).data)
                # Send to the receiver's personal group
                await self.channel_layer.group_send(
                    f"chat_{receiver_username}",
                    {
                        "type": "chat.message",
                        **MessageSerializer(message_obj).data
                    }
                )

    @database_sync_to_async
    def get_messages(self, sender, receiver):
        # Get the messages between the sender and receiver
        queryset = Message.objects.filter(
            Q(sender=sender, receiver=receiver) |
            Q(sender=receiver, receiver=sender)
        ).order_by('timestamp')
        s = MessageSerializer(queryset, many=True)
        return s.data

    @database_sync_to_async
    def get_recent_messages(self):
        # Get the recent messages sent by or to the user
        queryset = Message.objects.filter(
            Q(sender=self.user) | Q(receiver=self.user)
        ).order_by('-timestamp')
        s = MessageSerializer(queryset, many=True)
        return s.data

    @database_sync_to_async
    def save_message(self, message, receiver):
        # Save the message to the database
        message_obj = Message.objects.create(
            sender=self.user,
            receiver=receiver,
            message_type=Message.TEXT
        )
        message_obj.content = message
        return message_obj

    async def chat_message(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(event))
