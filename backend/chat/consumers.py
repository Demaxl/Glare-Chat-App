# chat/consumers.py
import json

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print(self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps(
            {
                "user_id": 1,
                "carrier_id": 3,
                "transaction_type_id": 1040,
                "transaction_amount": 5,
                "mobile_number": "0998407604"
            }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))
