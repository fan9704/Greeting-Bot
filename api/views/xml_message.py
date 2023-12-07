import logging

from rest_framework.exceptions import ValidationError
from rest_framework_xml.renderers import XMLRenderer

from api.serializers.user import SimpleMessageSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser

logger = logging.getLogger(__name__)


class XMLSimpleMessageAPIView(APIView):
    parser_classes = (XMLParser,)
    renderer_classes = [XMLRenderer, ]

    @swagger_auto_schema(
        operation_summary='XML Simple Message',
        operation_description='Reply Happy birthday! dear "username" with XML',
        request_body=SimpleMessageSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SimpleMessageSerializer(data=request.data)
            serializer.is_valid()
            if "happy birthday" in str(serializer.data["message"]).lower():
                response = Response({
                    "status": "success",
                    "message": f'Happy birthday, dear {serializer.data["username"]}',
                }, status=status.HTTP_200_OK)
                return response
            else:
                response = Response({
                    "status": "fail",
                    "message": "message invalid"
                }, status=status.HTTP_400_BAD_REQUEST)
                return response
        except ValidationError:
            response = Response({
                "status": "fail",
                "message": "data invalid"
            }, status=status.HTTP_400_BAD_REQUEST)
            return response
