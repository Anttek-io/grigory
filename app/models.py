from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    slug = models.SlugField(max_length=32, unique=True, blank=True, null=True, default=None,
                            validators=[MinLengthValidator(3), MaxLengthValidator(32),
                                        RegexValidator(r'^[a-zA-Z_]{3,32}$', _('Enter a valid slug.'))])
    members = models.JSONField(encoder=DjangoJSONEncoder, default=list)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ('-id', 'slug', 'chat_type')

    def __str__(self):
        return self.slug


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
