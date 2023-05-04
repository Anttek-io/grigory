from rest_framework.routers import DefaultRouter

from app.api.views.chats import ChatsViewSet
from app.api.views.messages import MessagesViewSet
from app.api.views.users import UserViewSet

router = DefaultRouter(trailing_slash=False)

router.register('chats', ChatsViewSet, basename='chats')

router.register('messages', MessagesViewSet, basename='messages')

router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
