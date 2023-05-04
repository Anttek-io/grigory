from channels.routing import URLRouter
from django.urls import re_path

from app.consumers.conversation import ConversationConsumer

root_routing = URLRouter([
    re_path(r'^conversation$', ConversationConsumer.as_asgi()),
])
