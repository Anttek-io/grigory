from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from app.models import ChatMember, Chat, CHAT_ROLE_ADMIN, CHAT_TYPE_PRIVATE
from app.serializers.chat_members import ChatMemberSerializer


class IsChatAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        chat_id = view.kwargs.get('chat_id')
        obj = get_object_or_404(Chat, id=chat_id)
        if obj.chat_type == CHAT_TYPE_PRIVATE:
            return True
        return obj.members.filter(user=request.user, role=CHAT_ROLE_ADMIN).exists()


class ChatMembersViewSet(viewsets.ModelViewSet):
    model = ChatMember
    serializer_class = ChatMemberSerializer
    permission_classes = (permissions.IsAuthenticated, IsChatAdmin)

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return self.model.objects.filter(chat=chat)
