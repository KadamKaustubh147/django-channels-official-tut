import json

from channels.generic.websocket import WebsocketConsumer

# sync websocket consumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # json loads --> converts JSON string to python object
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # json dump --> converts python object to JSON string
        self.send(text_data=json.dumps({"message": message}))