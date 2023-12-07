import datetime
import logging
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.models import User
from api.views.xml_message import XMLSimpleMessageAPIView

logger = logging.getLogger(__name__)


class XMLSimpleMessageAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.route = '/api/xml-message/'

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_XML_simple_message(self, mock_get_birthday_user_queryset):
        data = """
        <SimpleMessage>
            <message>Happy Birthday</message>
        </SimpleMessage>
        """
        request = self.factory.post(path=self.route, data=data,  content_type='application/xml')
        mock_get_birthday_user_queryset.return_value = [
            User.objects.create(
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

        view = XMLSimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], 'success')
        self.assertTrue(response.data[0]['message'], 'Happy birthday, dear Tom')
        logger.info("Complete XML Message View Test with Happy Birthday")

    @patch('api.service.user.UserService.get_birthday_user_queryset')
    def test_XML_message_invalid_data(self, mock_get_birthday_user_queryset):
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
