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
        self.today = datetime.datetime.today().date()
        self.u1 = User.objects.create(
            first_name="Cat",
            last_name="Tom",
            date_of_birth=datetime.date(
                1900,
                self.today.month,
                self.today.day
            ),
            gender="m",
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
            gender="f",
            email="u2@gmail.com"
        )
        self.route = '/api/over49/'

    def test_over_49(self):
        data = {
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Over 49 View Test with Happy Birthday over 49")

    def test_invalid_data(self):
        data = {
            "message": ""
        }
        request = self.factory.post(path=self.route, data=data, format='json')

        view = Over49APIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete Difference Gender View Test with Invalid Data")
