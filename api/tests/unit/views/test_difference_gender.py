import datetime
import logging
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.difference_gender import DifferenceGenderMessageAPIView

logger = logging.getLogger(__name__)


class DifferenceGenderAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.route = '/api/difference-gender/'

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    @patch('api.service.user.UserService.get_gender_discount')
    def test_simple_message_male(self, mock_get_gender_discount, mock_get_birthday_user_queryset):
        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = [
            User.objects.create(
                last_name="Cat",
                first_name="Tom",
                gender="m",
                date_of_birth=datetime.datetime.today(),
                email="u1@gmail.com"
            ),
        ]
        mock_get_gender_discount.return_value = '''
            We offer special discount 50% off for the following items:\n
            Cosmetic, LV Handbags
            '''
        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], '''Happy birthday, dear Tom\n
                        We offer special discount 20% off for the following items:\n
                        White Wine, iPhone X    
                        ''')
        logger.info("Complete Difference Gender Male View Test with Happy Birthday")

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    @patch('api.service.user.UserService.get_gender_discount')
    def test_simple_message_female(self, mock_get_gender_discount, mock_get_birthday_user_queryset):
        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = [
            User.objects.create(
                last_name="Mouse",
                first_name="Jelly",
                gender="f",
                date_of_birth=datetime.datetime.today(),
                email="u2@gmail.com"
            ),
        ]
        mock_get_gender_discount.return_value = '''
            We offer special discount 20% off for the following items:\n
            White Wine, iPhone X
            '''
        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], '''Happy birthday, dear Jelly\n
                        We offer special discount 20% off for the following items:\n
                        White Wine, iPhone X
                        ''')
        logger.info("Complete Difference Gender Female View Test with Happy Birthday")

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_simple_message_invalid_data(self, mock_get_birthday_user_queryset):
        data = {
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')
        mock_get_birthday_user_queryset.return_value = []
        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
