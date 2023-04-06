from app.models import Chat
from rest_framework import viewsets

from app.serializers.chats import ChatSerializer


class ChatsViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
