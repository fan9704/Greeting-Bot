from django.urls import path
from api.bot import callback

urlpatterns = [
    path('callback/', callback, name="LINE-Bot-Callback"),
]
