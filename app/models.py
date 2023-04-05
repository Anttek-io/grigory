from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder


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


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.JSONField(encoder=DjangoJSONEncoder)

    text = models.TextField()
    who_read = models.JSONField(encoder=DjangoJSONEncoder, default=list)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-timestamp',)

    @property
    def read(self):
        return len(self.who_read) > 0

    def __str__(self):
        return str(self.id)
