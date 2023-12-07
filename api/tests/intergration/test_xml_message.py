import datetime
import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.xml_message import XMLSimpleMessageAPIView

logger = logging.getLogger(__name__)


class XMLSimpleMessageAPIViewTestCase(TestCase):
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
        self.route = '/api/xml-message/'

    def test_XML_simple_message(self):
        data = """
        <SimpleMessage>
            <message>Happy Birthday</message>
        </SimpleMessage>
        """
        request = self.factory.post(path=self.route, data=data,  content_type='application/xml')

        view = XMLSimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom')
        logger.info("Complete XML Message View Test with Happy Birthday")

    def test_XML_message_invalid_data(self):
        data = """
        <SimpleMessage>
            <message></message>
        </SimpleMessage>
        """
        request = self.factory.post(path=self.route, data=data,  content_type='application/xml')

        view = XMLSimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['status'], 'fail')
        self.assertTrue(response.data[0]['message'], 'message invalid')
        logger.info("Complete XML Message View Test with invalid data")
