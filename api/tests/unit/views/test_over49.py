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
        self.today = datetime.datetime.today().date()

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_over49(self, mock_get_birthday_user_queryset):

        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = [
            User.objects.create(
                last_name="Cat",
                first_name="Tom",
                date_of_birth=datetime.date(
                    1900,
                    self.today.month,
                    self.today.day
                ),
                email="u1@gmail.com"
            ),
            User.objects.create(
                last_name="Mouse",
                first_name="Jelly",
                date_of_birth=datetime.date(
                    2020,
                    self.today.month,
                    self.today.day
                ),
                email="u2@gmail.com"
            ),
        ]

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Over 49 View Test with Happy Birthday over 49")

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_over49_invalid_data(self, mock_get_birthday_user_queryset):
        data = {
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = [
        ]
        view = Over49APIView.as_view()
        response = view(request, mock_get_birthday_user_queryset)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete Difference Gender View Test with Invalid Data")
