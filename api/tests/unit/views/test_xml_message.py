import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.views.xml_message import XMLSimpleMessageAPIView

logger = logging.getLogger(__name__)


class XMLSimpleMessageAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.route = '/api/xml-message/'

    def test_XML_simple_message(self):
        data = """
        <SimpleMessage>
            <message>Happy Birthday</message>
            <username>Tom</username>
        </SimpleMessage>
        """
        request = self.factory.post(path=self.route, data=data,  content_type='application/xml')

        view = XMLSimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(response.data['message'], 'Happy birthday, dear Tom')
        logger.info("Complete Simple Message View Test with Happy Birthday")

        data = """
        <SimpleMessage>
            <message></message>
            <username></username>
        </SimpleMessage>
        """
        request = self.factory.post(path=self.route, data=data,  content_type='application/xml')

        view = XMLSimpleMessageAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'fail')
        self.assertTrue(response.data['message'], 'message invalid')
        logger.info("Complete Simple Message View Test with invalid data")
