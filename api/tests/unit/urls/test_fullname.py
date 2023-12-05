import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class FullnameURLTest(TestCase):
    def testURL(self):
        url = reverse("Fullname-API")
        self.assertEqual(url, "/api/fullname/")
        logger.debug("Complete Fullname URL Test")
