from django.urls import re_path

from app.consumers.base import ChatConsumer
from core.settings import DJANGO_BASE_PATH

urlpatterns = [
    re_path(DJANGO_BASE_PATH + 'ws/' + r'^chat$', ChatConsumer.as_asgi()),
]
