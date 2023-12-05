import logging

from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger(__name__)


class DifferenceGenderURLTest(TestCase):
    def testURL(self):
        url = reverse("Over49-API")
        self.assertEqual(url, "/api/over49/")
        logger.debug("Complete Over49 URL Test")
