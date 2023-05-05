from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from app.models import ChatMember, Chat
from app.serializers.chats__members import ChatMemberSerializer


class ChatMembersViewSet(viewsets.ModelViewSet):
    model = ChatMember
    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return super().get_queryset().filter(chat=chat)
