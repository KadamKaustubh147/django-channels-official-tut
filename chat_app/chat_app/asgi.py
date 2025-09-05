"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter


# this should be at the start
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# asgi applications routing different than django url conf
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
    }
)


application = get_asgi_application()
