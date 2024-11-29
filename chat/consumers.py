import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Group, Message


class ChatConsumer(WebsocketConsumer):
    # Connect
    def connect(self):
        self.room_uuid = self.scope["url_route"]["kwargs"]["uuid"]
        self.room_group_name = f"chat_{self.room_uuid}"

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    # Disconnect
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive
    def receive(self, text_data=None):
        text_json = json.loads(text_data)
        message_sent = text_json["message"]

        user = self.scope["user"]
        group = Group.objects.get(uuid=self.room_uuid)

        message = Message(author=user, content=message_sent, group=group)
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "message_sent", "message": f"{user.username}: {message_sent}"},
        )

    def message_sent(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
