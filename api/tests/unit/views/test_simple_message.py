import datetime
import logging
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.message import SimpleMessageAPIView

logger = logging.getLogger(__name__)


class SimpleMessageAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('api.models.User.objects.filter')
    def test_simple_message(self, mock_filter):
        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path='/api/simple-message/', data=data, format='json')
        mock_filter.return_value = [User.objects.create(
            last_name="Cat",
            first_name="Tom",
            date_of_birth=datetime.datetime.today(),
            email="u1@gmail.com"
        ),
            User.objects.create(
                last_name="Mouse",
                first_name="Jelly",
                date_of_birth=datetime.datetime.today(),
                email="u2@gmail.com"
            ),
        ]
        view = SimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertEqual(response.data[1]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom')
        self.assertTrue(response.data[1]['message'], 'Happy birthday, dear Jelly')
        logger.info("Complete Simple Message View Test with Happy Birthday")

    @patch('api.models.User.objects.filter')
    def test_simple_message_invalid_data(self, mock_filter):
        data = {
            "message": ""
        }
        request = self.factory.post(path='/api/simple-message/', data=data, format='json')
        mock_filter.return_value = []
        view = SimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete Simple Message View Test with invalid data")
