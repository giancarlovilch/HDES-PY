from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ScheduleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("schedule", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("schedule", self.channel_name)

    async def receive(self, text_data):
        pass  

    async def seat_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
