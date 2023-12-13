from django.urls import path
from .consumers import *


websocket_urlpatterns = [
    path('ws/awsc/<str:jobGroupId>/',MyAsyncWebsocketConsumer.as_asgi()),
]