from rest_framework.routers import DefaultRouter

from app.api.views.chats import ChatsViewSet
from app.api.views.messages import MessagesViewSet

router = DefaultRouter(trailing_slash=False)

router.register('chats', ChatsViewSet, basename='chats')

router.register('messages', MessagesViewSet, basename='messages')

urlpatterns = router.urls
