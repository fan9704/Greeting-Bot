import logging

from rest_framework.exceptions import ValidationError

from api.serializers.user import DifferenceGenderSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class DifferenceGenderMessageAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='Difference Gender Message',
        operation_description='Reply discount merchandise according user gender',
        request_body=DifferenceGenderSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = DifferenceGenderSerializer(data=request.data)
            serializer.is_valid()
            if "happy birthday" in serializer.data["message"].lower():
                if serializer.data["gender"] == "m":
                    return Response({
                        "status": "success",
                        "message": f'''Happy birthday, dear {serializer.data["username"]}\n
                        We offer special discount 20% off for the following items:\n
                        White Wine, iPhone X                    
                        ''',
                    }, status=status.HTTP_200_OK)
                elif serializer.data["gender"] == "f":
                    return Response({
                        "status": "success",
                        "message": f'''Happy birthday, dear {serializer.data["username"]}\n
                        We offer special discount 50% off for the following items:\n
                        Cosmetic, LV Handbags
                        ''',
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

