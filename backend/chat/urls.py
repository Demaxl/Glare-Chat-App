from django.urls import path
from . import views

urlpatterns = [
    path('upload-image', views.upload_image_view, name='upload-image'),
]
