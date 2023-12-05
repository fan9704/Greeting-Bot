from django.urls import path
from api.views import callback

urlpatterns = [
    path('callback/', callback, name="LINE-Bot-Callback"),
]
