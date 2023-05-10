import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

CHAT_SLUG_REGEX = r'^[a-zA-Z_]{3,32}$'

CHAT_TYPE_PRIVATE = 'private'
CHAT_TYPE_GROUP = 'group'

CHAT_ROLE_ADMIN = 'admin'
CHAT_ROLE_MODERATOR = 'moderator'
CHAT_ROLE_MEMBER = 'member'

CHAT_ROLES = (
    (CHAT_ROLE_ADMIN, _('Admin')),
    (CHAT_ROLE_MODERATOR, _('Moderator')),
    (CHAT_ROLE_MEMBER, _('Member')),
)


def validate_chat_member(data, delete=False):
    instance = data['id']
    chat = data['chat']
    user = data['user']
    role = data['role']
    existing_members = chat.members.values_list('user__id', flat=True)
    including_current = set(existing_members) | {user.id}
    if chat.chat_type == CHAT_TYPE_PRIVATE:
        if not instance and len(including_current) > 2:
            raise ValidationError(_('Private chats cannot have more than 2 members.'))
        elif delete and len(including_current) < 2:
            raise ValidationError(_('Private chats cannot be empty.'))
    else:
        if ((instance and instance.role == CHAT_ROLE_ADMIN and role != CHAT_ROLE_ADMIN) or delete) and \
                not chat.members.filter(role=CHAT_ROLE_ADMIN).exclude(user__pk=instance.user.pk).exists():
            raise ValidationError(_('Chat must have at least one admin.'))


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
    creator = models.ForeignKey(User, models.RESTRICT, related_name='created_chats')

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ('-id', 'slug', 'chat_type')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.chat_type == CHAT_TYPE_PRIVATE:
            self.public = False
            self.slug = None
            self.members.update(role=None)
        else:
            if not self.members.filter(role=CHAT_ROLE_ADMIN).exists() and self.members.filter(user=self.creator).exists():
                self.members.filter(user=self.creator).update(role=CHAT_ROLE_ADMIN)
            self.members.filter(role__isnull=True).update(role=CHAT_ROLE_MEMBER)
        super().save(*args, **kwargs)

    @property
    def members_count(self):
        return self.members.count()

    @property
    def last_message(self):
        return self.messages.last()


class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', models.CASCADE, related_name='members')
    user = models.ForeignKey(User, models.CASCADE, related_name='chats')
    role = models.CharField(max_length=9, choices=CHAT_ROLES, default=CHAT_ROLE_MEMBER, blank=True, null=True)

    class Meta:
        unique_together = ('chat', 'user')

    def save(self, *args, **kwargs):
        if self.chat.chat_type == CHAT_TYPE_PRIVATE:
            self.role = None
        elif self.chat.creator == self.user and \
                (not self.role or not self.chat.members.filter(role=CHAT_ROLE_ADMIN).exists()):
            self.role = CHAT_ROLE_ADMIN
        elif not self.role:
            self.role = CHAT_ROLE_MEMBER
        super().save(*args, **kwargs)


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, models.RESTRICT, related_name='sent_messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()

    ready = models.BooleanField(default=True, editable=False)

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


def get_message_upload_path(instance, filename):
    return os.path.join('attachments', f'chat_{instance.message.chat.id}', filename)


class Attachment(models.Model):
    message = models.ForeignKey(Message, models.CASCADE, related_name='attachments', blank=True, null=True)
    file = models.FileField(upload_to=get_message_upload_path, blank=True, null=True)


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
