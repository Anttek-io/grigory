from rest_framework import serializers

from app.models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].write_only = True

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.file.url

    class Meta:
        model = Attachment
        exclude = ('message',)
