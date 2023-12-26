from core.middlewares import TokenAuthMiddleware, RouteNotFoundMiddleware, ContractMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from core import routing
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
    AuthMiddlewareStack(
        RouteNotFoundMiddleware(
            TokenAuthMiddleware(
                ContractMiddleware(
                    AllowedHostsOriginValidator(
                        URLRouter(
                            routing.websocket_urlpatterns
                        )
                    )
                )
            )
        )
    ),
})
