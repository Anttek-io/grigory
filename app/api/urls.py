from rest_framework.routers import DefaultRouter

from app.api.views.chats import ChatsViewSet
from app.api.views.chats__members import ChatMembersViewSet
from app.api.views.chats__messages import MessagesViewSet
from app.api.views.users import UsersViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'chats/(?P<chat_id>\d+)/members', ChatMembersViewSet, basename='chat-members')

router.register(r'chats/(?P<chat_id>\d+)/messages', MessagesViewSet, basename='chat-messages')

router.register('chats', ChatsViewSet, basename='chats')

router.register('users', UsersViewSet, basename='users')

urlpatterns = router.urls
