import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.views.message import SimpleMessageAPIView

logger = logging.getLogger(__name__)


class SimpleMessageAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_simple_message(self):
        data = {
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path='/api/simple-message/', data=data, format='json')

        view = SimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Simple Message View Test with Happy Birthday")

        data = {
            "username": "",
            "message": ""
        }
        request = self.factory.post(path='/api/simple-message/', data=data, format='json')

        view = SimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Simple Message View Test with invalid data")
