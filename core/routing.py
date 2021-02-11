# core/routing.py
from django.conf.urls import url
from django.urls import path

from core import consumers

websocket_urlpatterns = [
    url(r'^ws$', consumers.ChatConsumer),
    path('ws/group/', consumers.GroupChatConsumer),
]
