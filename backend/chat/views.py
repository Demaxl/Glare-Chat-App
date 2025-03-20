# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


from .models import Message
from .serializers import MessageSerializer


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_image_view(request):
    image = request.FILES.get('image')
    receiver_username = request.data.get('receiver')

    receiver = get_object_or_404(
        get_user_model(), username=receiver_username)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        message_type=Message.IMAGE
    )
    message.content = image

    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
