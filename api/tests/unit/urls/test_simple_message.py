import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class SimpleMessageURLTest(TestCase):
    def testCallbackURL(self):
        url = reverse("Simple-Message-API")
        self.assertEqual(url, "/api/simple-message/")
        logger.debug("Complete Simple Message URL Test")
