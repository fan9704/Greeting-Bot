import logging
import datetime

from unittest.mock import patch
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.over_49 import Over49APIView

logger = logging.getLogger(__name__)


class Over49APIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.route = '/api/over49/'

    @patch('api.models.User.objects.get_or_create')
    def test_over49(self, mock_get_or_create):

        data = {
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_or_create.return_value = User.objects.create(
            last_name="Cat",
            first_name="Tom",
            date_of_birth=datetime.date(1900, 9, 1),
            email="u1@gmail.com"
        ), None

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Over 49 View Test with Happy Birthday over 49")

    @patch('api.models.User.objects.get_or_create')
    def test_below49(self, mock_get_or_create):
        data = {
            "username": "Jelly",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = Over49APIView.as_view()
        mock_get_or_create.return_value = User.objects.create(
            last_name="Mouse",
            first_name="Jelly",
            date_of_birth=datetime.date(2023, 8, 24),
            email="u1@gmail.com"
        ), None
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Jelly')
        logger.info("Complete Over 49 View Test with Happy Birthday below 49")

        data = {
            "username": "",
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request, mock_get_or_create)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Difference Gender View Test with Invalid Data")
