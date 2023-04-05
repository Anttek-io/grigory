from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class NotificationsViewSet(viewsets.ViewSet):
    @action(['get'], False, url_name='get', url_path='get')
    def get(self, request):
        return Response({'status': 'ok'})

