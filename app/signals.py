from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.consumers.conversation import get_serializer_data
from app.models import Message


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    channel_layer = get_channel_layer()
    group_name = f'chat_{instance.chat.id}'
    data = {'type': 'message'}
    serializer_data = get_serializer_data(instance)
    data.update(serializer_data)
    async_to_sync(channel_layer.group_send)(group_name, {'type': 'chat_message', 'data': data})
