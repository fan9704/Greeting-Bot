import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.views.difference_gender import DifferenceGenderMessageAPIView

logger = logging.getLogger(__name__)


class DifferenceGenderAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_simple_message(self):
        route = '/api/difference-gender/'
        data = {
            "gender": "m",
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], '''Happy birthday, dear Tom\n
                        We offer special discount 20% off for the following items:\n
                        White Wine, iPhone X    
                        ''')
        logger.info("Complete Difference Gender Male View Test with Happy Birthday")

        data = {
            "gender": "f",
            "username": "Tom",
            "message": "Happy Birthday!"
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], '''Happy birthday, dear Tom\n
                        We offer special discount 50% off for the following items:\n
                        Cosmetic, LV Handbags
                        ''')
        logger.info("Complete Difference Gender Female View Test with Happy Birthday")

        data = {
            "gender": "",
            "username": "",
            "message": ""
        }
        request = self.factory.post(path=route, data=data, format='json')

        view = DifferenceGenderMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Difference Gender View Test with Invalid Data")