from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from .validators import validate_audio, validate_video


class Message(models.Model):
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
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPES, default=TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender} -> {self.receiver}: {self.content}"

    @property
    def content(self):
        return getattr(self, f"{self.message_type}_content")

    @content.setter
    def content(self, value):
        match self.message_type:
            case Message.TEXT:
                TextMessage.objects.create(message=self, text=value)
            case Message.IMAGE:
                ImageMessage.objects.create(
                    message=self, image=value)
            case Message.VIDEO:
                VideoMessage.objects.create(
                    message=self, video=value)
            case Message.AUDIO:
                AudioMessage.objects.create(
                    message=self, audio=value)

    @classmethod
    def related_objects(cls):
        """
        Returns a queryset with all message content types prefetched.
        This optimizes database queries when accessing message content.
        """
        return cls.objects.prefetch_related(
            'text_content',
            'image_content',
            'video_content',
            'audio_content'
        ).select_related('sender', 'receiver')


class MessageTypeAbstract(models.Model):

    class Meta:
        abstract = True

    def clean(self):
       # Ensure the related 'message' exists before accessing its attributes
        if self.message_id is None:
            return
        if self.TYPE != self.message.message_type:
            raise ValidationError({"message": "Invalid message type"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TextMessage(MessageTypeAbstract):
    TYPE = Message.TEXT
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="text_content")
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.text[:20]}..."


class AudioMessage(MessageTypeAbstract):
    TYPE = Message.AUDIO
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="audio_content")
    audio = models.FileField(upload_to="audio/", validators=[validate_audio])

    def __str__(self) -> str:
        return f"{self.audio}"


class VideoMessage(MessageTypeAbstract):
    TYPE = Message.VIDEO
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="video_content")
    video = models.FileField(upload_to="video/", validators=[validate_video])

    def __str__(self) -> str:
        return str(self.video)


class ImageMessage(MessageTypeAbstract):
    TYPE = Message.IMAGE
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, primary_key=True, related_name="image_content")
    image = models.ImageField(upload_to="images/")

    def __str__(self) -> str:
        return str(self.image)
