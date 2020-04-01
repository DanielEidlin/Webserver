from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/reverse_shell/connect/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
