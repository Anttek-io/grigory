from rest_framework import viewsets, mixins
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet

from app.serializers.users import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
