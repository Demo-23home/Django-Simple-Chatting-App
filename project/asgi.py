"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
import chat.routing
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
        ),
    }
)
