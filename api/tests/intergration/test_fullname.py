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
        self.today = datetime.datetime.today().date()
        self.u1 = User.objects.create(
            first_name="Cat",
            last_name="Tom",
            date_of_birth=datetime.date(
                1900,
                self.today.month,
                self.today.day
            ),
            email="u1@gmail.com"
        )
        self.u2 = User.objects.create(
            first_name="Mouse",
            last_name="Jelly",
            date_of_birth=datetime.date(
                2023,
                self.today.month,
                self.today.day
            ),
            email="u2@gmail.com"
        )
        self.route = '/api/fullname/'

    def test_simple_message(self):
        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertEqual(response.data[1]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom, Cat!')
        self.assertTrue(response.data[1]['message'], 'Happy birthday, dear Jelly, Mouse!')
        logger.info("Complete Fullname Test")

    def test_invalid_data(self):
        data = {
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = FullnameAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete Fullname Test with Invalid Data")
