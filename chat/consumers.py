import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Group, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["uuid"]
        self.room_group_name = "chat_%s" % self.room_name
        self.room_uuid = self.scope["url_route"]["kwargs"]["uuid"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        # Use sync_to_async to query the database
        group = await sync_to_async(self.get_group)(self.room_uuid)

        # Insert the message into the database
        await sync_to_async(self.save_message)(user, message, group)

        # Send message to room group (including the author's name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "author": user.username,  # Add the author's username here
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        author = event["author"]

        await self.send(
            text_data=json.dumps(
                {"message": message, "author": author}  # Send the author to the WebSocket
            )
        )

    # Helper method to get group (synchronously)
    def get_group(self, room_uuid):
        return Group.objects.get(uuid=room_uuid)

    # Helper method to save the message (synchronously)
    def save_message(self, user, message, group):
        db_insert = Message(author=user, content=message, group=group)
        db_insert.save()
