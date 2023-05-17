from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
	re_path(r"^chat/(?P<group_id>[a-zA-Z0-9_-]+)/$", ChatConsumer.as_asgi()),
]
