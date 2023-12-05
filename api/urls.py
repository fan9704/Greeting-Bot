from django.urls import path
from api.bot import callback
from api.views.message import SimpleMessageAPIView
from api.views.difference_gender import DifferenceGenderMessageAPIView
from api.views.over_49 import Over49APIView
from api.views.fullname import FullnameAPIView

urlpatterns = [
    # LINE Bot
    path('callback/', callback, name="LINE-Bot-Callback"),
    # API
    path('simple-message/', SimpleMessageAPIView.as_view(), name="Simple-Message-API"),
    path('difference-gender/', DifferenceGenderMessageAPIView.as_view(), name="Difference-Gender-API"),
    path('over49/', Over49APIView.as_view(), name="Over49-API"),
    path('fullname/', FullnameAPIView.as_view(), name="Fullname-API"),

]
