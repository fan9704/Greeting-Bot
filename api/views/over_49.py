import base64
import logging
import datetime
import os

from rest_framework.exceptions import ValidationError

from GreetingBot.settings import BASE_DIR
from api.models import User
from api.serializers.user import SimpleMessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class Over49APIView(APIView):
    @swagger_auto_schema(
        operation_summary='Over 49 Message',
        operation_description='Reply discount merchandise according user gender',
        request_body=SimpleMessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SimpleMessageSerializer(data=request.data)
            serializer.is_valid()
            user, _ = User.objects.get_or_create(
                first_name=serializer.data["username"],
            )
            age = datetime.date.today().year - user.date_of_birth.year
            if "happy birthday" in serializer.data["message"].lower() and age >= 0:
                if age > 49:
                    image_path = os.path.join(BASE_DIR, 'static', 'images', 'greet.jpg')

                    with open(image_path, 'rb') as f:
                        image = f.read()
                    b64_img = base64.b64encode(image)
                    return Response({
                        "status": "success",
                        "message": f'Happy birthday, dear {serializer.data["username"]}',
                        "picture": b64_img
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "success",
                        "message": f'Happy birthday, dear {serializer.data["username"]}',
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "fail",
                    "message": "message invalid"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({
                "status": "fail",
                "message": "data invalid"
            }, status=status.HTTP_400_BAD_REQUEST)
