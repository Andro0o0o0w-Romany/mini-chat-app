"""
ASGI config for chat_project.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns
from chat.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})

