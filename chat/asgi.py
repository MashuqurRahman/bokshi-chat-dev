# chat/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from core import routing as core_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(core_routing.websocket_urlpatterns)),
    }
)
