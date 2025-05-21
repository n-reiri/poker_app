# game/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://<host>/ws/rooms/<room_id>/
    re_path(r'ws/rooms/(?P<room_id>\d+)/$', consumers.GameConsumer.as_asgi()),
]