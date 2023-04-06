from channels.routing import URLRouter
from django.urls import re_path

from app.consumers.base import ChatConsumer

root_routing = URLRouter([
    re_path(r'^chat$', ChatConsumer.as_asgi()),
])
