import logging
import datetime

from unittest.mock import patch
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.fullname import FullnameAPIView

logger = logging.getLogger(__name__)


class FullnameAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.route = '/api/fullname/'
        self.today = datetime.datetime.today().date()

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_fullname(self, mock_get_birthday_user_queryset):
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
                    2023,
                    self.today.month,
                    self.today.day
                ),
                email="u2@gmail.com"
            ),
        ]

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertEqual(response.data[1]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom, Cat!')
        self.assertTrue(response.data[1]['message'], 'Happy birthday, dear Jelly, Mouse!')
        logger.info("Complete Fullname View Test")

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_fullname_with_invalid_data(self, mock_get_birthday_user_queryset):
        data = {
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = []

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete Fullname View Test with Invalid Data")
