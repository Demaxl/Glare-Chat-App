import pytest
import pytest_asyncio
from channels.testing import WebsocketCommunicator
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from django.urls import path

from ..consumers import ChatConsumer


@pytest.mark.django_db
class TestChatConsumer:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_communicator(self, user_factory):
        # Create test users using sync_to_async
        from asgiref.sync import sync_to_async
        self.sender = await sync_to_async(user_factory)()
        self.receiver = await sync_to_async(user_factory)()

        # Create application with authenticated scope
        application = AuthMiddlewareStack(URLRouter([
            path('ws/chat/', ChatConsumer.as_asgi())
        ]))

        # Create communicators
        self.sender_communicator = WebsocketCommunicator(
            application=application,
            path="/ws/chat/",
            headers=[(b"origin", b"http://localhost")]
        )
        self.receiver_communicator = WebsocketCommunicator(
            application=application,
            path="/ws/chat/",
            headers=[(b"origin", b"http://localhost")]
        )

        # Add users to scope
        self.sender_communicator.scope["user"] = self.sender
        self.receiver_communicator.scope["user"] = self.receiver

        # Connect both communicators
        connected, _ = await self.sender_communicator.connect()
        assert connected
        connected, _ = await self.receiver_communicator.connect()
        assert connected

        yield  # Add yield to make this a proper async fixture

        # Cleanup in the same fixture
        await self.sender_communicator.disconnect()
        await self.receiver_communicator.disconnect()

    @pytest.mark.asyncio
    async def test_message(self):
        # Send a test message from the sender
        await self.sender_communicator.send_json_to({
            "type": "chat.message",
            "receiver": self.receiver.username,
            "message": "Test"
        })

        # Get the response from the receiver
        response = await self.receiver_communicator.receive_json_from()

        # Assert the response matches expected format
        assert response['message'] == "Test"
        assert response['sender'] == self.sender.username
