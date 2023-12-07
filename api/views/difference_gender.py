import logging

from rest_framework.exceptions import ValidationError

from api.service.user import UserService
from api.serializers.user import MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class DifferenceGenderMessageAPIView(APIView):
    repository = UserService
    @swagger_auto_schema(
        operation_summary='Difference Gender Message',
        operation_description='Reply discount merchandise according user gender',
        request_body=MessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            if "happy birthday" in request.data.get("message", "").lower():
                birthday_user_list = self.repository.get_birthday_user_queryset()
                response = []
                for user in birthday_user_list:
                    single_response = {
                        "status": "success",
                        "message": f'Happy birthday, dear {user.last_name}\n{self.repository.get_gender_discount(user.gender)}',
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


