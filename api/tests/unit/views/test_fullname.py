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

    @patch('api.models.User.objects.get_or_create')
    def test_fullname(self, mock_get_or_create):
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

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom,Cat')
        logger.info("Complete Fullname View Test")

    def test_fullname_with_invalid_data(self):
        data = {
            "username": "",
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Fullname View Test with Invalid Data")
