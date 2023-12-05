import logging

from rest_framework.exceptions import ValidationError

from api.serializers.user import SimpleMessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser

logger = logging.getLogger(__name__)


class XMLSimpleMessageAPIView(APIView):
    parser_classes = (XMLParser,)
    @swagger_auto_schema(
        operation_summary='XML Simple Message',
        operation_description='Reply Happy birthday! dear "username" with XML',
        request_body=SimpleMessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SimpleMessageSerializer(data=request.data)
            serializer.is_valid()
            if "happy birthday" in serializer.data["message"].lower():
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

