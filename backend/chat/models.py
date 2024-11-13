from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

    MESSAGE_TYPES = (
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
    )

    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPES, default=TEXT)

    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def content(self):
        return getattr(self, f"{self.message_type}_content")


class MessageTypeAbstract(models.Model):

    class Meta:
        abstract = True


class TextMessage(MessageTypeAbstract):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="text_content")
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.text[:20]}..."


class AudioMessage(MessageTypeAbstract):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="audio_content")
    audio = models.FileField(upload_to="audio/")

    def __str__(self) -> str:
        return f"{self.audio}"


class VideoMessage(MessageTypeAbstract):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="video_content")
    video = models.FileField(upload_to="video/")

    def __str__(self) -> str:
        return str(self.video)


class ImageMessage(MessageTypeAbstract):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="image_content")
    image = models.ImageField(upload_to="images/")

    def __str__(self) -> str:
        return str(self.image)
