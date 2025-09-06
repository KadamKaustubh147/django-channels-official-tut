import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# $ python3 manage.py shell

# import channels.layers

# channel_layer = channels.layers.get_channel_layer()

# from asgiref.sync import async_to_sync

# async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

# async_to_sync(channel_layer.receive)('test_channel')
# {'type': 'hello'}

# When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. The ChatConsumer will receive that message and forward it to the group corresponding to the room name. Every ChatConsumer in the same group (and thus in the same room) will then receive the message from the group and forward it over WebSocket back to JavaScript, where it will be appended to the chat log.


# sync websocket consumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # room_name comes from the router
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.

        # Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.

        # ! so basically room_name is from the URL route in chat/routing.py that opened
        
        # ! and room_group_name is channel layer group name

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        # adding to channel layer is async operation
        
        # await channel_layer.group_add(group, channel)
        # await channel_layer.group_discard(group, channel)

        # channel --> individual user mail box
        # group --> when send to a group it sends to various channels
        
        #! basically below code means adding user's channel to the group name we got from the scope of the request (url params asli mei dekha jaye toh)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket and brodcast it to the group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group --> sends to consumers
        async_to_sync(self.channel_layer.group_send)(
            # chat.message gets converted to chat_message --> that is the function that will run
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room consumer and send to client
    # event is a user interaction which happens in the lifetime of a scope
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket client side
        self.send(text_data=json.dumps({"message": message}))

        
        # json loads --> converts JSON string to python object
        # json dump --> converts python object to JSON string
        
        
# 👉 So the cycle is:

# Client → Server: receive gets called.

# Server → Group: group_send dispatches to all consumers.

# Server → Client(s): Each consumer’s chat_message sends it out to its socket.