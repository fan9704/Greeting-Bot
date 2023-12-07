import logging
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers.user import MessageSerializer

logger = logging.getLogger(__name__)


class SimpleMessageAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Simple Message',
        operation_description='Bless every user who is birthday boy/girl Happy birthday! dear "username"',
        request_body=MessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            if "happy birthday" in request.data.get("message", "").lower():
                birthday_user_list = User.objects.filter(date_of_birth__day=datetime.today().day,
                                                         date_of_birth__month=datetime.today().month)
                response = []
                for user in birthday_user_list:

                    single_response = {
                        "status": "success",
                        "message": f'Happy birthday, dear {user.last_name}',
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
