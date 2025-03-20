from django.urls import path
from . import views

urlpatterns = [
    path('image-upload', views.upload_image_view, name='image-upload'),
]
