from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.ImageField(upload_to="profile_photos", blank=True)

    def __str__(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @first_name.setter
    def first_name(self, value):
        self.user.first_name = value
        self.user.save()

    @last_name.setter
    def last_name(self, value):
        self.user.last_name = value
        self.user.save()
