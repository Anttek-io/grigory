from rest_framework.routers import DefaultRouter

from app.api.views.notifications import NotificationsViewSet

router = DefaultRouter(trailing_slash=False)

router.register('notifications', NotificationsViewSet, basename='notifications')

urlpatterns = router.urls
