# core/routing.py

from django.urls import path
from . import consumers

websocket_patterns = [
    path('ws/<str:groupname>/', consumers.AsyncDashboardConsumer.as_asgi()),
]
