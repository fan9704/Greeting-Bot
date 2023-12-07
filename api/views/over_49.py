import base64
import logging
import datetime
import os

from rest_framework.exceptions import ValidationError

from GreetingBot.settings import BASE_DIR
from api.serializers.user import MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.service.user import UserService

logger = logging.getLogger(__name__)


class Over49APIView(APIView):
    repository = UserService

    @swagger_auto_schema(
        operation_summary='Over 49 Message',
        operation_description='Reply Happy Birthday who is over 49 years old',
        request_body=MessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            if "happy birthday" in request.data.get("message", "").lower():
                birthday_user_list = self.repository.get_birthday_user_queryset()
                response = []
                for user in birthday_user_list:
                    if datetime.datetime.today().year - user.date_of_birth.year >= 49:
                        image_path = os.path.join(BASE_DIR, 'static', 'images', 'greet.jpg')

                        with open(image_path, 'rb') as f:
                            image = f.read()
                        b64_img = base64.b64encode(image)
                        single_response = {
                            "status": "success",
                            "message": f'Happy birthday, dear {user.last_name}',
                            "picture": b64_img
                        }
                        response.append(single_response)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = [{
                    "status": "fail",
                    "message": 'message invalid',
                }]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({
                "status": "fail",
                "message": "data invalid"
            }, status=status.HTTP_400_BAD_REQUEST)
