from rest_framework.routers import DefaultRouter

from app.api.views.chats import ChatsViewSet
from app.api.views.chats__members import ChatMembersViewSet
from app.api.views.messages import MessagesViewSet
from app.api.views.users import UsersViewSet

router = DefaultRouter(trailing_slash=False)

router.register('chats/(?P<chat_id>[^/.]+)/members', ChatMembersViewSet, basename='chats/members')

router.register('chats', ChatsViewSet, basename='chats')

router.register('messages', MessagesViewSet, basename='messages')

router.register('users', UsersViewSet, basename='users')

urlpatterns = router.urls
