from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

class FallbackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.send(text_data="Invalid WebSocket path.")
        await self.close()
        raise DenyConnection("Invalid path")