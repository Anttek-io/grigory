from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.auth import get_user_model


User = get_user_model()


class Token(AuthToken):
    key = models.CharField(_('Key'), max_length=40, primary_key=True)
    user_id = models.PositiveBigIntegerField(_('User'), db_index=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    last_use = models.DateTimeField(_('Last use'), auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')

    def __str__(self):
        return self.key

    @property
    def user(self):
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            self.delete()
            return None
