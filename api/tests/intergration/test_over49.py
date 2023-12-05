import logging
import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.over_49 import Over49APIView

logger = logging.getLogger(__name__)


class Over49APIViewTestCase(TestCase):
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
        route = '/api/over49/'
        data = {
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Over 49 View Test with Happy Birthday over 49")

        data = {
            "username": "Jelly",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Jelly')
        logger.info("Complete Over 49 View Test with Happy Birthday below 49")

        data = {
            "username": "",
            "message": ""
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Difference Gender View Test with Invalid Data")