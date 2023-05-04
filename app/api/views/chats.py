from app.models import Chat
from rest_framework import viewsets

from app.serializers.chats import ChatSerializer, ChatListSerializer


class ChatsViewSet(viewsets.ModelViewSet):
    model = Chat
    serializer_class = ChatSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        chats = self.model.objects.filter(members=self.request.user)
        return chats
