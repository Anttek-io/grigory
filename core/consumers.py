from channels.generic.websocket import AsyncWebsocketConsumer


class AsyncHealthCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send('ok')
        await self.close()
