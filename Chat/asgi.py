import os
from django.core.asgi import get_asgi_application

# django channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from main.websocket_urls import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')


application = ProtocolTypeRouter({
	"https": get_asgi_application(),
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				websocket_urlpatterns
			)
		)
	)
})
