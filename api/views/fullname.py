import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers.user import SimpleMessageSerializer

logger = logging.getLogger(__name__)


class FullnameAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Fullname Message',
        operation_description='Reply username whole name',
        request_body=SimpleMessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SimpleMessageSerializer(data=request.data)
            serializer.is_valid()
            user, _ = User.objects.get_or_create(
                first_name=serializer.data["username"],
            )
            fullname = f'{user.last_name},{user.first_name}'
            if "happy birthday" in serializer.data["message"].lower():
                return Response({
                    "status": "success",
                    "message": f'Happy birthday, dear {fullname}',
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
