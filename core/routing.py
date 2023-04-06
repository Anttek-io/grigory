from django.urls import path
from channels.routing import URLRouter

from app.consumers.base import ChatConsumer

root_routing = URLRouter([
    path('chat', ChatConsumer.as_asgi()),
])
