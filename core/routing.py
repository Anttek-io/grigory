from channels.routing import URLRouter
from django.urls import re_path

from app.consumers.chats import ChatsConsumer
from app.consumers.conversation import ConversationConsumer

root_routing = URLRouter([
    re_path(r'^conversation$', ConversationConsumer.as_asgi()),
    re_path(r'^chats$', ChatsConsumer.as_asgi()),
])
