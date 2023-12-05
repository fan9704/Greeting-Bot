from django.urls import path
from api.bot import callback
from api.views.message import SimpleMessageAPIView

urlpatterns = [
    # LINE Bot
    path('callback/', callback, name="LINE-Bot-Callback"),
    # API
    path('simple-message/', SimpleMessageAPIView.as_view(), name="Simple-Message-API")
]
