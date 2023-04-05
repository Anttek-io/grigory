"""
ASGI config for grigory project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from uvicorn.workers import UvicornWorker as BaseUvicornWorker

from core.consumers import AsyncHealthCheckConsumer
from core.routing import root_router

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": URLRouter([
        path('ws/health', AsyncHealthCheckConsumer.as_asgi()),
        path('ws/', AllowedHostsOriginValidator(AuthMiddlewareStack(root_router))),
    ])
})


class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS = {"lifespan": "off"}
