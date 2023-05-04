from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from app.models import Message, Chat
from app.serializers.messages import MessageSerializer


def allowed_chats(request):
    if not request:
        return Chat.objects.none()
    return Chat.objects.filter(members=request.user)


class ChatFilter(filters.FilterSet):
    chat_id = filters.ModelChoiceFilter(queryset=allowed_chats)

    class Meta:
        model = Message
        fields = ('chat_id',)


class MessagesViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    filterset_class = ChatFilter

    def get_queryset(self):
        return Message.objects.filter(chat__members=self.request.user)

    def list(self, request, *args, **kwargs):
        chat_id = request.query_params.get('chat_id')
        if not chat_id:
            raise ValidationError({'chat_id': [_('This field is required.')]})
        return super().list(request, *args, **kwargs)
