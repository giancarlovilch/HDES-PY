from django.urls import path
from .consumers import ScheduleConsumer

websocket_urlpatterns = [
    path("ws/schedule/", ScheduleConsumer.as_asgi()),
]
