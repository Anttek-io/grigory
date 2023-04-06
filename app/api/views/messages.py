from app.models import Message
from rest_framework import viewsets
from rest_framework.decorators import action

from app.serializers.messages import MessageSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    @action(['post'], False, url_name='send_message', url_path='send_message')
    def send_message(self, request):
        data = request.data.copy()
        
