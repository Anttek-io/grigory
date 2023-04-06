from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender_id = models.JSONField(encoder=DjangoJSONEncoder)

    class Meta:
        abstract = True

    @property
    def sender(self):
        try:
            return User.objects.get(id=self.sender_id)
        except User.DoesNotExist:
            return None


class Chat(models.Model):
    chat_type_choices = (
        ('private', _('Private')),
        ('group', _('Group')),
    )
    chat_type = models.CharField(max_length=7, choices=chat_type_choices, default='private')

    slug = models.SlugField(max_length=32, unique=True, blank=True, null=True, default=None)
    users = models.JSONField(encoder=DjangoJSONEncoder, default=list)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ('-id', 'slug', 'chat_type')

    def __str__(self):
        return str(self.id)


class Message(BaseMessage):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    who_seen = models.JSONField(encoder=DjangoJSONEncoder, default=list)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-timestamp',)

    @property
    def seen(self):
        return len(self.who_seen) > 0

    def __str__(self):
        return str(self.id)

    async def send_to_websocket(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        try:
            user = await database_sync_to_async(User.objects.get)(id=self.sender_id)
        except User.DoesNotExist:
            return
        await channel_layer.group_send(
            self.chat.slug,
            {
                'type': 'chat_message',
                'sender': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message': self.text,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

