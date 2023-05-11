from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from app.models import Message, Chat
from app.serializers.messages import MessageSerializer


class IsChatMember(permissions.BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get('chat_id')
        obj = get_object_or_404(Chat, id=chat_id)
        return obj.members.filter(user=request.user).exists()


class MessagesViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsChatMember)
    queryset = model.objects.none()

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return self.model.objects.filter(chat=chat)
