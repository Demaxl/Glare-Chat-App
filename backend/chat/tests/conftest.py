import pytest

from ..models import Message, TextMessage, AudioMessage, VideoMessage, ImageMessage


@pytest.fixture
def message_factory(db, user_factory):
    def create_message(content, message_type=Message.TEXT):
        sender = user_factory()
        receiver = user_factory()

        message = Message.objects.create(
            sender=sender, receiver=receiver, message_type=message_type)
        message.save()

        message.content = content

        return message
    return create_message
