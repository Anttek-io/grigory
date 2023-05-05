from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from app.consumers.conversation import get_serializer_data
from app.models import Message


def send_message_to_ws(message):
    channel_layer = get_channel_layer()
    group_name = f'chat_{message.chat.id}'
    data = {'type': 'message'}
    serializer_data = get_serializer_data(message)
    data.update(serializer_data)
    async_to_sync(channel_layer.group_send)(group_name, {'type': 'message', 'data': data})


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    if instance.pk:
        current_readiness = instance.ready
        previous_readiness = Message.objects.filter(id=instance.id).values_list('ready', flat=True).first()
        if current_readiness and previous_readiness != current_readiness:
            send_message_to_ws(instance)


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created and instance.ready:
        send_message_to_ws(instance)
