from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = {}
        fields = (i.name for i in User._meta.fields if not i.name.startswith('_'))
        for field in fields:
            user_data[field] = str(getattr(user, field))
        token['user'] = user_data
        return token
