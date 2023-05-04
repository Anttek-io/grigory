from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

CHAT_SLUG_REGEX = r'^[a-zA-Z_]{3,32}$'

CHAT_TYPE_PRIVATE = 'private'
CHAT_TYPE_GROUP = 'group'


class BaseMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, models.RESTRICT, related_name='sent_messages')

    class Meta:
        abstract = True


class Chat(models.Model):
    chat_type_choices = (
        (CHAT_TYPE_PRIVATE, _('Private')),
        (CHAT_TYPE_GROUP, _('Group')),
    )
    chat_type = models.CharField(max_length=7, choices=chat_type_choices, default=CHAT_TYPE_PRIVATE)
    public = models.BooleanField(default=False)

    slug = models.SlugField(max_length=32, unique=True, blank=True, null=True, default=None,
                            validators=[MinLengthValidator(3), MaxLengthValidator(32),
                                        RegexValidator(CHAT_SLUG_REGEX, _('Enter a valid slug.'))])
    members = models.ManyToManyField(User, related_name='chats')
    creator = models.ForeignKey(User, models.RESTRICT, related_name='created_chats')

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ('-id', 'slug', 'chat_type')

    def __str__(self):
        return str(self.id)

    @property
    def members_count(self):
        return self.members.count()

    @property
    def last_message(self):
        return self.messages.last()


class Message(BaseMessage):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-timestamp',)

    @property
    def seen(self):
        return self.views.exists()

    # TODO: Add some property to get list of users who have seen the message

    def __str__(self):
        return str(self.id)


class MessageView(models.Model):
    message = models.ForeignKey(Message, models.RESTRICT, related_name='views')
    user = models.ForeignKey(User, models.RESTRICT, related_name='message_views')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Message View')
        verbose_name_plural = _('Message Views')
        ordering = ('-timestamp',)
        unique_together = ('message', 'user')

    def __str__(self):
        return str(self.id)
