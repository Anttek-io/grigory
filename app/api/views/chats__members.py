from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from app.models import ChatMember, Chat, CHAT_ROLE_ADMIN
from app.serializers.chats__members import ChatMemberSerializer


class IsChatAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        chat_id = view.kwargs.get('chat_id')
        obj = get_object_or_404(Chat, id=chat_id)
        return obj.members.filter(user=request.user, chatmember__role=CHAT_ROLE_ADMIN).exists()


class ChatMembersViewSet(viewsets.ModelViewSet):
    model = ChatMember
    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsChatAdmin)

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return super().get_queryset().filter(chat=chat)
