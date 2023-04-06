from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_slug = None

    async def connect(self):
        self.chat_slug = "qwerty"
        await self.channel_layer.group_add(
            self.chat_slug,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_slug,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.chat_slug, {
                "type": "send_message",
                "message": text_data,
            })

    async def send_message(self, event):
        await self.send(text_data=event["message"])
