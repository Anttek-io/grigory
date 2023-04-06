from app.models import Message
from rest_framework import viewsets

from app.serializers.messages import MessageSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
