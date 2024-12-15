import pytest

from ..models import Message, TextMessage, AudioMessage, VideoMessage, ImageMessage


@pytest.fixture
def message_factory(db, user_factory):
    def create_message(content, message_type=Message.TEXT, sender=None, receiver=None):
        sender = user_factory() if sender is None else sender
        receiver = user_factory() if receiver is None else receiver

        message = Message.objects.create(
            sender=sender, receiver=receiver, message_type=message_type)
        message.save()

        message.content = content

        return message
    return create_message
