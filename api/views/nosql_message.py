import datetime
from mongoengine import connect

import logging

from rest_framework.exceptions import ValidationError

from api.serializers.user import MessageSerializer
from api.documents import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)
connect('greet')


class NoSQLMessageAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='NoSQL Message',
        operation_description='Reply username whole name use NoSQL',
        request_body=MessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid()

            user = User.objects(last_name=request.data.get("last_name"))
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
    def patch(self,request):
        user = User(
            email=request.data.get("email"),
            last_name=request.data.get("last_name"),
            first_name=request.data.get("first_name"),
            gender=request.data.get("gender"),
            date_of_birth=request.data.get("date_of_birth")
                    )
        user.save()