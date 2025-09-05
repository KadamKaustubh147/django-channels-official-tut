from django.urls import re_path

from . import consumers
'''
    (?P<room_name>\w+)

    (?P<room_name> ... ) → this is a named capturing group. Whatever matches inside ... will be stored under the name "room_name".

    \w+ → matches one or more "word characters" (a-z, A-Z, 0-9, and _).

    So if the URL is ws/chat/room1/, then "room1" will be captured and passed as room_name="room1" to your consumer.

    /$ → the $ enforces that the string must end with / right after the room name.
'''

websocket_urlpatterns = [
    # We call the as_asgi() classmethod in order to get an ASGI application that will instantiate an instance of our consumer for each user-connection. This is similar to Django’s as_view(), which plays the same role for per-request Django view instances.

    
    # re_path --> more flexible than path able to write regex patterns
    # inside there is a raw string
    
    # basically this is /ws/chat/ROOM_NAME/
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi())
]