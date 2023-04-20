"""
ASGI config for HawkSoar project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import db_connect.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkSoar.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            db_connect.routing.websocket_urlpatterns
        )
    )
})
