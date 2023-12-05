import logging
import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.fullname import FullnameAPIView

logger = logging.getLogger(__name__)


class FullnameAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.u1 = User.objects.create(
            first_name="Cat",
            last_name="Tom",
            date_of_birth=datetime.date(1900, 9, 1),
            email="u1@gmail.com"
        )
        self.u2 = User.objects.create(
            first_name="Mouse",
            last_name="Jelly",
            date_of_birth=datetime.date(2023, 8, 24),
            email="u2@gmail.com"
        )

    def test_simple_message(self):
        route = '/api/fullname/'
        data = {
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom,Cat')
        logger.info("Complete Fullname Test")



        data = {
            "username": "",
            "message": ""
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Fullname Test with Invalid Data")