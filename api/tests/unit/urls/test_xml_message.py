import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class XMLSimpleMessageURLTest(TestCase):
    def testCallbackURL(self):
        url = reverse("XML-Message-API")
        self.assertEqual(url, "/api/xml-message/")
        logger.debug("Complete XML Simple Message URL Test")
