"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routing import websocket_urlpatterns


# this should be at the start
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# asgi applications routing different than django url conf

# protocol type router decides which is the protocol of communication according to it, it gives to websocket or http

# The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.




application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        
        # checks if the request jidhar se aa rahi hai voh proper allowed host hai
        
        # then populate the scope of the request
        
        # like how django middleware populates the request object with user credentials
        
        "websocket": AllowedHostsOriginValidator(
           AuthMiddlewareStack(URLRouter(websocket_urlpatterns)) 
        )
    }
)

# not needed as we made custom application above
# application = get_asgi_application()
