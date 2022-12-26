from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/income_call/<int:user_id>/', consumers.IncomeCallConsumer.as_asgi()),
    path('ws/statistic/', consumers.Statistic.as_asgi()),
    path('ws/socket-server/', consumers.ChatConsumer.as_asgi()),
]
